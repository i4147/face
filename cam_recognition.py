from src import LiveCamera
from src import FaceRecognizer
import cv2

camera = LiveCamera()
recognizer = FaceRecognizer()

while True:
    frame = camera.read()

    if frame is None:
        print("Failed to read frame.")
        break

    faces = recognizer.detect(frame)

    if len(faces) == 0:
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == 27:
            break

        continue

    print(f"Detected {len(faces)} face(s).")

    face = faces[0]

    print("Bounding Box:")
    print(face.bbox)

    print("\nEmbedding shape:")
    print(face.embedding.shape)

    print("\nEmbedding:")
    print(face.embedding)

    break

camera.release()
cv2.destroyAllWindows()
