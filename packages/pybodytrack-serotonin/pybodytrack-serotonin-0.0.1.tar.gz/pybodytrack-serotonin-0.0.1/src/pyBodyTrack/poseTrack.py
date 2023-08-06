import cv2
import mediapipe as mp
from threading import Thread
class posetrack():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.landmark = self.mp_pose.PoseLandmark
    def detect(self,callback):
        cap = cv2.VideoCapture(0)
        with self.mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                self.results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                self.landmarks = self.results.pose_landmarks.landmark
                self.mp_drawing.draw_landmarks(
                    image,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
                cv2.imshow('MediaPipe Pose', image)
                callback()
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()
    def start(self,callback):
        detect = Thread(target=self.detect,args=(callback))
        detect.start()

