class EmployeeData:
    def __init__(self, name, face):
        self.face = face
        self.name = name

    def to_dict(self):
        return {"employee_face": self.face, "employee_name": self.name}
