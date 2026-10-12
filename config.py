import os

DEBUG = True


def debugging_method(*args, **kwargs):
    print(*args, **kwargs)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ATTENDANCE_DB_PATH = os.path.join(BASE_DIR, "data", "attendance.db")

print(ATTENDANCE_DB_PATH)
