import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        # static_image_mode=True for single image (snapshot)
        self.pose = self.mp_pose.Pose(static_image_mode=True,
                                      model_complexity=1,
                                      enable_segmentation=False,
                                      min_detection_confidence=0.5)

    def detect(self, image_bgr):
        """
        input: image_bgr (numpy array BGR)
        output: landmarks dict (idx -> (x,y,z,visibility)), pose_landmarks object
        """
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        res = self.pose.process(image_rgb)
        landmarks = {}
        h, w = image_bgr.shape[:2]
        if res.pose_landmarks:
            for idx, lm in enumerate(res.pose_landmarks.landmark):
                landmarks[idx] = (int(lm.x * w), int(lm.y * h), float(lm.z), float(lm.visibility))
        return landmarks, res.pose_landmarks

def draw_landmarks(image_bgr, pose_landmarks):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    if pose_landmarks:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mp_drawing.draw_landmarks(image_rgb, pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    return image_bgr

def angle_between(A, B, C):
    """
    A, B, C: tuples with at least (x,y,...)
    returns angle at B in degrees
    """
    a = np.array(A[:2]) - np.array(B[:2])
    c = np.array(C[:2]) - np.array(B[:2])
    num = np.dot(a, c)
    den = np.linalg.norm(a) * np.linalg.norm(c)
    if den == 0:
        return 0.0
    cosv = np.clip(num / den, -1.0, 1.0)
    angle_rad = np.arccos(cosv)
    return np.degrees(angle_rad)
