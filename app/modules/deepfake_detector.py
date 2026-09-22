"""
Task 7: Deepfake / digital impersonation detection.

Plan (per architecture doc):
    - Use a pretrained HuggingFace model as-is — do NOT fine-tune
      (saves time under deadline; spend saved time on explanation quality)
    - CV model for image/video, separate model for voice/audio clips
    - Keep demo clips short — CPU inference is slower than GPU

Must return a schemas.detection_result.DetectionResult with scenario="deepfake".
"""

from app.schemas.detection_result import DetectionResult


def detect_deepfake(event_id: str, media_path: str, media_type: str) -> DetectionResult:
    """
    Run the pretrained manipulation-detection model on the given media file
    and return a DetectionResult. media_type: "image" | "video" | "audio".
    Owner: fill in model loading + inference below.
    """
    raise NotImplementedError("Task 7 owner: implement deepfake_detector.detect_deepfake")
