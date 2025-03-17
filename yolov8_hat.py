import cv2
import numpy as np
import requests
import time
from ultralytics import YOLO

# ✅ 모델 경로 설정
model_path = r"C:\Users\현희섭\Downloads\yolo_for_hat.pt"
model = YOLO(model_path)  # 커스텀 YOLO 모델

# ✅ IP 카메라 스냅샷 URL
photo_url = "http://172.16.57.4:8080/photo.jpg"

cv2.namedWindow("YOLOv8 - IP Camera", cv2.WINDOW_NORMAL)  # 단일 창 사용

frame_interval = 1.0 / 120  # 초당 120프레임 (8.3ms)
print("📌 실시간 YOLO 탐지 시작... (종료: 'q' 키)")

fps_counter = 0
start_fps_time = time.time()

while True:
    start_time = time.time()  # 프레임 시작 시간

    try:
        # ✅ 최신 사진 요청 (스냅샷)
        response = requests.get(photo_url, timeout=0.5)  # Timeout 단축
        if response.status_code != 200:
            print("📌 사진을 가져올 수 없습니다. 상태 코드:", response.status_code)
            continue

        # ✅ OpenCV에서 사용할 수 있도록 변환
        img_array = np.frombuffer(response.content, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is None:
            print("📌 이미지 디코딩 실패")
            continue

        # ✅ YOLO 실행
        yolo_start = time.time()
        results = model(frame, imgsz=640, conf=0.3)  # 해상도 증가 & 신뢰도 조정
        annotated_frame = results[0].plot()  # 탐지 결과 표시
        yolo_time = time.time() - yolo_start

        # ✅ 단일 창에서 결과 업데이트
        cv2.imshow("YOLOv8 - IP Camera", annotated_frame)

        # ✅ FPS 계산
        fps_counter += 1
        elapsed_fps_time = time.time() - start_fps_time
        if elapsed_fps_time >= 1.0:  # 1초마다 FPS 출력
            print(f"📌 현재 FPS: {fps_counter} (YOLO 처리 속도: {yolo_time:.3f}초)")
            fps_counter = 0
            start_fps_time = time.time()

        # 'q' 키를 누르면 종료
        if cv2.waitKey(10) & 0xFF == ord('q'):  # `cv2.waitKey(1)` → `cv2.waitKey(10)`로 변경
            break

    except Exception as e:
        print("📌 오류 발생:", e)
        continue

    # ✅ 초당 120프레임 유지 (8.3ms 간격)
    elapsed_time = time.time() - start_time
    sleep_time = max(0, frame_interval - elapsed_time)
    time.sleep(sleep_time)

cv2.destroyAllWindows()
print("📌 YOLO 탐지 종료.")
