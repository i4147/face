import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face BLOB NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                confidence REAL,
                FOREIGN KEY(employee_id) REFERENCES employees(id)
            )
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_attendance_employee
            ON attendance(employee_id)
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_attendance_timestamp
            ON attendance(timestamp)
        """)

        self.connection.commit()

    def close(self):
        self.connection.close()
