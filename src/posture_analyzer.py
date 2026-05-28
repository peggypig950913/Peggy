from src.pose_detector import angle_between

class PostureAnalyzer:
    def __init__(self, thresholds=None):
        # thresholds 可依需求調整
        self.thresholds = thresholds or {
            "back_angle_min": 160,   # example: 大角度接近 180 表示較直
            "knee_angle_min": 160
        }

    def analyze(self, landmarks):
        """
        landmarks: dict idx -> (x,y,z,visibility)
        returns dict: {score, messages, angles}
        """
        results = {"score": 100, "messages": [], "angles": {}}
        try:
            # Mediapipe indices: 11 left shoulder, 23 left hip, 25 left knee, 27 left ankle
            l_sh = landmarks[11]; l_hip = landmarks[23]; l_knee = landmarks[25]; l_ankle = landmarks[27]
            back_angle = angle_between(l_sh, l_hip, l_knee)
            results["angles"]["left_back_angle"] = back_angle
            if back_angle < self.thresholds["back_angle_min"]:
                results["score"] -= 20
                results["messages"].append("偵測到前傾/駝背，請抬胸縮肩。")

            knee_angle = angle_between(l_hip, l_knee, l_ankle)
            results["angles"]["left_knee_angle"] = knee_angle
            if knee_angle < self.thresholds["knee_angle_min"]:
                results["score"] -= 10
                results["messages"].append("膝蓋未完全伸直。")
        except KeyError:
            results["messages"].append("偵測不到完整關節，請重拍或調整距離。")
            results["score"] = 0
        return results
