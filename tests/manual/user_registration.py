from src import EmployeeRegistrar
from db import EmployeeDb

# ----
ed = EmployeeDb()


def register(employee_name):
    e_data = EmployeeRegistrar.capture(employee_name=employee_name, shots=10, mode="reg")
    e_data = e_data.to_dict()
    ed.insert_employee(employee_dict=e_data)


if __name__ == "__main__":
    e_name = "new_user"  # input("Enter name: ")
    register(e_name)
