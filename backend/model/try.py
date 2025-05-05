from ultralytics import YOLO
import os

# проверка, что файл существует
video_path = os.path.join(os.path.dirname(__file__), "fight.mp4")

if not os.path.exists(video_path):
    print(f"Файл не найден по пути: {video_path}")
    print("Доступные файлы в директории:")
    print(os.listdir(os.path.dirname(__file__)))
    exit()

# загрузка модели и обработка видео
model = YOLO("yolov8n.pt") 

results = model.predict(
    source=video_path,  #используем путь
    save=True,
    classes=[15, 16], #классы 15-кошки, 16-собаки
    conf=0.5,
    show=True
)
