import feature_points_extractor
import cv2

cap = cv2.VideoCapture('test_video.mp4')
# cap = cv2.VideoCapture(-1)

size = (int(cap.get(3)),int(cap.get(4)))

result = cv2.VideoWriter('result.avi',cv2.VideoWriter_fourcc(*'MJPG'),10,size)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("exiting....")
        break

    with_features, direction = feature_points_extractor.get_features(frame)

    print(direction)

    result.write(with_features)

    cv2.imshow('frame', with_features)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
result.release()
cv2.destroyAllWindows()