import time
import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import defaultdict

# ✅ MongoDB 연결
client = MongoClient("mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority&authSource=admin")
db = client["yolo_database"]

# ✅ 데이터베이스 컬렉션
collection_detections = db["detections"]  # 전체 탐지 기록 (누적)
collection_detection = db["detection"]  # 가장 최근 탐지 기록

# ✅ 실시간 그래프 설정 (왼쪽: 실시간 탐지, 오른쪽: 누적 탐지)
plt.ion()
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 왼쪽(실시간), 오른쪽(누적)
ax1, ax2 = axes  # 두 개의 그래프

while True:
    try:
        # ✅ MongoDB에서 최신 데이터 가져오기
        latest_detection = collection_detection.find_one(sort=[("timestamp", -1)])  # 가장 최근 탐지된 데이터
        detections_all = list(collection_detections.find().sort("timestamp", -1).limit(100))  # 최근 100개 데이터

        # ✅ 실시간 탐지 데이터 가공
        latest_counts = defaultdict(int)
        if latest_detection and "detections" in latest_detection:
            latest_counts.update(latest_detection["detections"])  # 최신 탐지 데이터 저장

        # ✅ 누적 탐지 데이터 가공 (매 루프마다 초기화 후 업데이트)
        cumulative_counts = defaultdict(int)
        for doc in detections_all:
            if "detections" in doc:
                for class_name, count in doc["detections"].items():
                    cumulative_counts[class_name] += count  # 누적 데이터 업데이트

        # ✅ 1️⃣ 왼쪽 실시간 그래프 (최근 탐지)
        ax1.clear()
        if latest_counts:
            ax1.bar(latest_counts.keys(), latest_counts.values(), color="skyblue")
            ax1.set_title("실시간 탐지 (Latest Detection)")
            ax1.set_ylabel("탐지된 개수")
            ax1.tick_params(axis="x", rotation=45)
        else:
            ax1.text(0.5, 0.5, "No Data", fontsize=16, ha="center", va="center")

        # ✅ 2️⃣ 오른쪽 누적 그래프
        ax2.clear()
        if cumulative_counts:
            ax2.bar(cumulative_counts.keys(), cumulative_counts.values(), color="orange")
            ax2.set_title("누적 탐지 (Cumulative Detection)")
            ax2.set_ylabel("탐지된 개수")
            ax2.tick_params(axis="x", rotation=45)
        else:
            ax2.text(0.5, 0.5, "No Data", fontsize=16, ha="center", va="center")

        plt.draw()
        plt.pause(0.1)  # 🔥 그래프가 실시간으로 업데이트되도록 추가

        time.sleep(1)

    except Exception as e:
        print("📌 오류 발생:", e)
        time.sleep(5)
        continue  # 오류 발생 시 루프 유지

plt.ioff()
plt.show()
