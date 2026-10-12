import cv2
import streamlit as st

from src import EmployeeRegistrar
from src.face_capture.face import FaceCapture

from db import EmployeeDb
from db import AttendanceDb


# ============================================================
# Page
# ============================================================

st.set_page_config(
    page_title="Face Attendance",
    page_icon="📸",
    layout="centered",
)

st.title("📸 Face Attendance System")

employee_db = EmployeeDb()
attendance_db = AttendanceDb()

camera_placeholder = st.empty()


# ============================================================
# Helpers
# ============================================================


def recognize_employee():

    while True:
        frame = FaceCapture.read()

        if frame is None:
            continue

        faces = FaceCapture.detect(frame)

        preview = FaceCapture.draw_faces(frame, faces)

        preview = cv2.cvtColor(
            preview,
            cv2.COLOR_BGR2RGB,
        )

        camera_placeholder.image(
            preview,
            channels="RGB",
            use_container_width=True,
        )

        if len(faces) != 1:
            continue

        embedding = FaceCapture.get_embedding(faces[0])

        if not FaceCapture._embedding_check(embedding):
            continue

        employee = {
            "employee_face": embedding,
        }

        return employee_db.find_employee_by_face(employee)


# ============================================================
# Registration
# ============================================================

st.header("📝 Register Employee")

employee_name = st.text_input(
    "Employee name",
    key="employee_name",
)

register_button = st.button(
    "Register Employee",
    use_container_width=True,
)

if register_button:
    if not employee_name.strip():
        st.error("Please enter employee name.")
        st.stop()

    try:
        with st.spinner("Capturing face..."):
            employee = EmployeeRegistrar.capture(employee_name=employee_name, shots=10, mode="reg")

        employee_db.insert_employee(
            employee.to_dict(),
        )

        st.success(f"{employee_name} registered successfully.")

    except Exception as e:
        st.exception(e)

# ============================================================
# Attendance
# ============================================================

st.divider()

st.header("📸 Attendance")

col1, col2 = st.columns(2)

with col1:
    check_in = st.button(
        "✅ Check In",
        use_container_width=True,
    )

with col2:
    check_out = st.button(
        "🚪 Check Out",
        use_container_width=True,
    )


if check_in:
    try:
        with st.spinner("Recognizing employee..."):
            employee = recognize_employee()

        if employee is None:
            st.error("Unknown employee.")

        else:
            attendance_db.check_in(
                employee["id"],
            )

            st.success(f"Welcome, {employee['name']}!")

            st.write(f"Confidence: {employee['confidence']:.4f}")

    except Exception as e:
        st.exception(e)


if check_out:
    try:
        with st.spinner("Recognizing employee..."):
            employee = recognize_employee()

        if employee is None:
            st.error("Unknown employee.")

        else:
            attendance_db.check_out(
                employee["id"],
            )

            st.success(f"Goodbye, {employee['name']}!")

            st.write(f"Confidence: {employee['confidence']:.4f}")

    except Exception as e:
        st.exception(e)


# ============================================================
# Attendance History
# ============================================================

st.divider()

st.header("📋 Attendance History")

history = attendance_db.get_history()

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# Cleanup
# ============================================================

employee_db.close()
attendance_db.close()
