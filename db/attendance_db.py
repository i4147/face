from db.database import Database
from config import ATTENDANCE_DB_PATH


class AttendanceDb(Database):
    def __init__(self):
        super().__init__(ATTENDANCE_DB_PATH)

    def check_in(self, employee_id: int) -> int:
        self.cursor.execute(
            """
            INSERT INTO attendance (employee_id, action)
            VALUES (?, 'IN')
            """,
            (employee_id,),
        )

        self.connection.commit()

        return self.cursor.lastrowid

    def check_out(self, employee_id: int) -> int:
        self.cursor.execute(
            """
            INSERT INTO attendance (employee_id, action)
            VALUES (?, 'OUT')
            """,
            (employee_id,),
        )

        self.connection.commit()

        return self.cursor.lastrowid

    def get_history(self, limit: int = 100) -> list[dict]:
        self.cursor.execute(
            """
            SELECT
                attendance.id,
                attendance.employee_id,
                employees.name,
                attendance.timestamp,
                attendance.action,
                attendance.confidence
            FROM attendance
            INNER JOIN employees
                ON employees.id = attendance.employee_id
            ORDER BY attendance.timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )

        history = []

        for row in self.cursor.fetchall():
            history.append(dict(row))

        return history

    def get_today(self) -> list[dict]:
        self.cursor.execute(
            """
            SELECT
                attendance.id,
                attendance.employee_id,
                employees.name,
                attendance.timestamp,
                attendance.action,
                attendance.confidence
            FROM attendance
            INNER JOIN employees
                ON employees.id = attendance.employee_id
            WHERE DATE(attendance.timestamp) = DATE('now', 'localtime')
            ORDER BY attendance.timestamp DESC
            """
        )

        history = []

        for row in self.cursor.fetchall():
            history.append(dict(row))

        return history
