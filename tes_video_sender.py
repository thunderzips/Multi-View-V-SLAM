import feature_points_extractor
import cv2
import numpy as np
import time

cap = cv2.VideoCapture('test_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    with_features = feature_points_extractor.get_features(frame)

    cv2.imshow('frame', with_features)
    # cv2.imshow('mask',mask)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()