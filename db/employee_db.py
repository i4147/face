import numpy as np
from db.database import Database
from config import ATTENDANCE_DB_PATH
from typing import Union


class EmployeeDb(Database):
    def __init__(self):
        super().__init__(ATTENDANCE_DB_PATH)

    def insert_employee(self, employee_dict: dict) -> int:
        face_blob = employee_dict["employee_face"].astype(np.float32).tobytes()

        self.cursor.execute(
            """
            INSERT INTO employees(name, face)
            VALUES (?, ?)
            """,
            (
                employee_dict["employee_name"],
                face_blob,
            ),
        )

        self.connection.commit()

        return self.cursor.lastrowid

    def find_employee_by_face(
        self,
        face_embedding: Union[np.ndarray, dict],
        threshold: float = 0.6,
    ) -> dict | None:

        if isinstance(face_embedding, dict):
            face_embedding = face_embedding["employee_face"]

        face_embedding = face_embedding.astype(np.float32)
        face_embedding /= np.linalg.norm(face_embedding)

        employees = self.get_employees()

        best_employee = None
        best_score = -1.0

        for employee in employees:
            stored_embedding = employee["face"]
            stored_embedding /= np.linalg.norm(stored_embedding)

            score = np.dot(face_embedding, stored_embedding)

            if score > best_score:
                best_score = score
                best_employee = employee

        if best_employee is None or best_score < threshold:
            return None

        best_employee["confidence"] = float(best_score)

        return best_employee

    def get_employees(self) -> list[dict]:
        self.cursor.execute(
            """
            SELECT id, name, face
            FROM employees
            """
        )

        employees = []

        for row in self.cursor.fetchall():
            employees.append({
                "id": row["id"],
                "name": row["name"],
                "face": np.frombuffer(
                    row["face"],
                    dtype=np.float32,
                ).copy(),
            })

        return employees
