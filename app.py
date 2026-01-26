from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import uuid

app = Flask(__name__)
#  Flask – это класс; мы создаём экземпляр → объект с dunder‑методом __call__,
#  поэтому веб‑сервер может «звать» app(request_environ) как функцию.

UPLOAD_FOLDER = 'uploads' # куда кладём оригинальные ролики
RESULT_FOLDER = 'results' # куда YOLO сохранит готовые видео
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO('yolov8n.pt')  #считываются веса, строится вычислительный граф (PyTorch)
# объект реализует __call__/predict, поэтому можно вызвать model(...)

@app.route('/') # декоратор регистрирует URL "/" → функцию index
def index():
    return render_template('index.html') # Jinja2 → HTML → Response

@app.route('/upload', methods=['POST'])  # POST, т.к. клиент отправляет файл
def upload():
     #Проверка, что в multipart‑form пришёл файл с ключом "video"
    if 'video' not in request.files: # request.files – ImmutableMultiDict, dunder __getitem__
        return jsonify({'error': 'Нет файла'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    video_id = str(uuid.uuid4())  # Генерируем уникальный id ролика (UUID4 → строка), чтобы не столкнуть имена
    input_path = os.path.join(UPLOAD_FOLDER, f'{video_id}.mp4') # Формируем путь, куда сохранить оригинал

    file.save(input_path)

    # Обработка видео нейронкой (YOLO)
    results = model.predict(     # high‑level вызов Ultralytics
        input_path,
        save=True,
        save_txt=False,
        project=RESULT_FOLDER,
        name=video_id,    # подпапка = UUID → isolation
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

    return jsonify({'result_url': f'/result/{video_id}/{processed_video}'}) #Преобразует Python-словарь в JSON-строку:
#Упаковывает это в HTTP-ответ с заголовком Content-Type: application/json.Отправляет результат на фронт.
#Таким образом, сервер отвечает браузеру в формате JSON.

@app.route('/result/<video_id>/<filename>')  # динамические сегменты URL
def result(video_id, filename):   
    # send_from_directory → готовый Response с заголовками,
    # поддерживает X‑Sendfile для nginx, range‑запросы и т.д.
    return send_from_directory(os.path.join(RESULT_FOLDER, video_id), filename)



if __name__ == '__main__':
    app.run(debug=True)

# Это web-приложение на Flask, которое позволяет пользователю загрузить видео, автоматически определить на нём животных 
# с помощью модели YOLOv8, и получить обработанное видео с выделенными объектами.Все данные между frontend и backend 
# передаются через JSON, а JavaScript обрабатывает загрузку и показ результата прямо в браузере, без перезагрузки.
#Я реализовала backend, подключила модель, написала логику загрузки/отправки, и оформила базовый frontend с валидацией 
# и предпросмотром видео.

#В проекте я использую JSON для общения между frontend и backend.
#Flask-часть возвращает jsonify(...) — это Python-словарь, превращённый в JSON-ответ.
#На frontend-е в JS я вызываю fetch(...).then(resp => resp.json()) — и получаю данные обратно в объекте.
#Это простой способ передавать информацию между сервером и браузером, без перезагрузки страницы.
