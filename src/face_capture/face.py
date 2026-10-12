import time

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from config import DEBUG, debugging_method


class FaceRecognizer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open webcam.")

        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640),
        )

    # ==========================================================
    # Camera
    # ==========================================================

    def read(self):
        success, frame = self.cap.read()

        if not success:
            return None

        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        self.release()

    # ==========================================================
    # Face recognition
    # ==========================================================

    def detect(self, frame):
        return self.app.get(frame)

    def draw_faces(self, frame, faces):
        image = frame.copy()

        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

        return image

    def get_embedding(self, face):
        return face.embedding

    @staticmethod
    def cosine_similarity(emb1, emb2):
        emb1 = emb1 / np.linalg.norm(emb1)
        emb2 = emb2 / np.linalg.norm(emb2)

        return float(np.dot(emb1, emb2))

    # ==========================================================
    # Capture
    # ==========================================================

    @staticmethod
    def _embedding_check(embedding) -> bool:
        if embedding is None:
            if DEBUG:
                debugging_method("Embedding is None")
            return False

        embedding = np.asarray(embedding)

        if embedding.shape != (512,):
            if DEBUG:
                debugging_method(f"Invalid embedding shape: {embedding.shape}")
            return False

        return True

    def snap(self, tries: int = 3):
        while tries > 0:
            frame = self.read()

            if frame is None:
                tries -= 1
                continue

            faces = self.detect(frame)

            if len(faces) != 1:
                tries -= 1
                continue

            embedding = self.get_embedding(faces[0])

            if not self._embedding_check(embedding):
                tries -= 1
                continue

            return embedding

        return None

    def capture(self, shots: int = 10):
        embeddings = []

        print("=" * 50)
        print("Face Detection")
        print("Look at the camera and slowly move your head.")
        print(f"Collecting {shots} samples...")
        print("=" * 50)

        while len(embeddings) < shots:
            embedding = self.snap()

            if embedding is None:
                continue

            embeddings.append(embedding)

            print(f"Captured {len(embeddings)}/{shots}")

            time.sleep(0.25)

        embeddings = np.vstack(embeddings)

        average_embedding = np.mean(embeddings, axis=0)
        average_embedding /= np.linalg.norm(average_embedding)

        print("\nCapturing complete.")

        return average_embedding


FaceCapture = FaceRecognizer()
