import logging
from typing import List

from fastapi import UploadFile

from fastserve import FastServe

logging.getLogger(__name__)

try:
    import face_recognition
except ModuleNotFoundError:
    face_recognition = None


class FaceDetection(FastServe):
    def __init__(self, batch_size=1, timeout=0):
        super().__init__(
            batch_size=batch_size, timeout=timeout, input_schema=UploadFile
        )
        if not face_recognition:
            raise ModuleNotFoundError(
                "face_recognition is not installed. "
                "Please run 'pip install face-recognition' first."
            )

    def handle(self, batch: List[UploadFile]) -> List[List[float]]:
        results = []
        for file in batch:
            image = face_recognition.load_image_file(file.file)
            face_locations = face_recognition.face_locations(image)
            results.append(face_locations)
        return results
