import cv2
from ultralytics import YOLO

# ✅ YOLO 모델 로드
model = YOLO(r"C:\Users\23011\Downloads\best (3).pt")

# ✅ 웹캠 열기
cap = cv2.VideoCapture(0)  # 기본 카메라

if not cap.isOpened():
    print("📌 웹캠을 열 수 없습니다. 카메라 연결을 확인하세요.")
    exit()

# ✅ 실시간 탐지 루프
while True:
    ret, frame = cap.read()
    if not ret:
        print("📌 프레임을 가져올 수 없습니다. 카메라 상태를 확인하세요.")
        break

    # YOLO 모델로 탐지 수행
    results = model(frame)

    # 탐지된 객체를 프레임에 표시
    annotated_frame = results[0].plot()

    # 실시간 화면 출력
    cv2.imshow("YOLO Real-Time Detection", annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ✅ 자원 해제
cap.release()
cv2.destroyAllWindows()