import feature_points_extractor
import cv2

cap = cv2.VideoCapture('test_video3.mp4')

while cap.isOpened():
    if True:
        ret, frame = cap.read()
        if not ret:
            print("exiting....")
            break

        with_features, direction = feature_points_extractor.get_features(frame)

        print(direction)

        cv2.imshow('frame', with_features)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()