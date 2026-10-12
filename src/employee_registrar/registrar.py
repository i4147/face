import numpy as np
from src.face_capture import FaceCapture
from utils import EmployeeData


class EmployeeRegistrar:
    @classmethod
    def capture(
        cls,
        mode: str,
        employee_name: str = None,
        shots: int = None,
    ):
        """

        :param mode: "rec" for recognition (no employee name needed), "reg" for registration
        :param employee_name:
        :param shots:
        :return:
        """
        if mode == "reg" and employee_name.strip() is None:
            employee_name = "Unknown from `registrar.py`"

        shots = 10 if shots is None else shots

        employee_face_average_embedding: np.ndarray = FaceCapture.capture(shots)

        return EmployeeData(name=employee_name, face=employee_face_average_embedding)
