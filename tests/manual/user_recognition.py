from src import EmployeeRegistrar
from db import EmployeeDb

# ----
ed = EmployeeDb()


def recognize(employee_name):
    # ---
    employee_data = EmployeeRegistrar.capture(employee_name=employee_name, shots=10, mode="rec")
    employee_data = employee_data.to_dict()

    # ---
    employee = ed.find_employee_by_face(employee_data)
    if employee is None:
        print("Unknown employee")
    else:
        print(f"User ID: {employee['id']}")
        print(f"User Name:{employee['name']}")
        print(f"Face Match Confidence:{employee['confidence']}")


if __name__ == "__main__":
    e_name = input("Enter name: ")
    recognize(e_name)
