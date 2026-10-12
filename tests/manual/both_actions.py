from user_registration import register
from user_recognition import recognize

if __name__ == "__main__":
    user_name = input("User name: ")
    register(employee_name=user_name)
    recognize(employee_name=user_name)
