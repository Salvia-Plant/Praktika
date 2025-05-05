from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO('yolov8n.pt')  # Убедись, что файл модели есть в папке проекта

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'Нет файла'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    video_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f'{video_id}.mp4')

    file.save(input_path)

    # Обработка видео нейронкой (YOLO)
    results = model.predict(
        input_path,
        save=True,
        save_txt=False,
        project=RESULT_FOLDER,
        name=video_id,
        exist_ok=True
    )
    # Найти обработанное видео
    result_dir = os.path.join(RESULT_FOLDER, video_id)
    print("YOLO result dir:", result_dir)
    print("Содержимое:", os.listdir(result_dir))
    processed_video = None
    for fname in os.listdir(result_dir):
        if fname.endswith('.mp4'):
            processed_video = fname
            break
    if not processed_video:
        return jsonify({'error': 'Ошибка обработки'}), 500

    return jsonify({'result_url': f'/result/{video_id}/{processed_video}'})


@app.route('/result/<video_id>/<filename>')
def result(video_id, filename):
    return send_from_directory(os.path.join(RESULT_FOLDER, video_id), filename)



if __name__ == '__main__':
    app.run(debug=True)
