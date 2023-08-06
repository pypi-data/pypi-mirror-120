import cv2
import mediapipe as mp
from threading import Thread

class handtrack():
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(max_num_hands=1,min_detection_confidence=0.7)
        self.mpdraw = mp.solutions.drawing_utils
        self.drawingstyle = mp.solutions.drawing_styles
        self.handlandmarks = self.mphands.HandLandmark
    def detect(self,callback):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            success, self.image = self.cap.read()
            if not success:
                continue
            self.image = cv2.cvtColor(cv2.flip(self.image,1), cv2.COLOR_BGR2RGB)
            self.image.flags.writeable = False
            self.results = self.hands.process(self.image)
            self.image.flags.writeable = True
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            
            if self.results.multi_hand_landmarks:
                self.landmarks = self.results.multi_hand_landmarks[0].landmark
                for hand_landmarks in self.results.multi_hand_landmarks:
                    self.mpdraw.draw_landmarks(
                        self.image,
                        hand_landmarks,
                        self.mphands.HAND_CONNECTIONS,
                        self.drawingstyle.get_default_hand_landmarks_style(),
                        self.drawingstyle.get_default_hand_connections_style())
            cv2.imshow('MediaPipe Hands', self.image)
            callback()
            if cv2.waitKey(5) & 0xFF == 27:
                break
    def start(self,callback):
        x = Thread(target=self.detect,args=(callback))
        x.start()


