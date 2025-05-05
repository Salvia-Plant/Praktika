from flask import Flask, request, jsonify, send_from_directory, render_template
from ultralytics import YOLO
import os
import uuid  #для генерации уникальных имён файлов (опционально)

app = Flask(__name__,
            template_folder='../frontend/templates',  
            static_folder='../frontend/static')       

#загружаем модель YOLO 
model = YOLO("yolov8n.pt")  

#папки для загрузки и результатов
UPLOAD_FOLDER = "runs"
RESULT_FOLDER = "runs/detect"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_video", methods=["POST"])
def process_video():
    #проверяем, что файл есть в запросе
    if "video" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    video_file = request.files["video"]
    
    #генерируем уникальное имя для файла
    #это необязательная функция, нужна чтобы не было конфликта если разные пользоввтели загрузят видео с одинаковым именем
    video_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    output_path = os.path.join(RESULT_FOLDER, f"{video_id}.mp4")

    # Сохраняем загруженное видео
    video_file.save(input_path)

    # Обрабатываем видео через YOLO
    try:
        results = model.predict(
            input_path,
            save=True,
            save_txt=False,
            project=RESULT_FOLDER,
            name="",
            exist_ok=True,
            classes=[15, 16],  #15=cat, 16=dog (COCO)
            conf=0.5
        )
        
        #путь к обработанному видео (YOLO сохраняет его в папке results)
        processed_video = os.path.join(RESULT_FOLDER, "predict", f"{video_id}.mp4")

        #возвращаем ссылку на результат
        return jsonify({
            "status": "success",
            "video_id": video_id,
            "result_url": f"/result/{video_id}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/result/<video_id>", methods=["GET"])
def get_result(video_id):
    # Отдаём обработанное видео
    return send_from_directory(
        os.path.join(RESULT_FOLDER, "predict"),
        f"{video_id}.mp4",
        as_attachment=False
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)