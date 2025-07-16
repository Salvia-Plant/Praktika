document.addEventListener('DOMContentLoaded', function() {
    const videoInput = document.getElementById('video-upload');
    const preview = document.getElementById('video-preview');
    const uploadBtn = document.getElementById('upload-btn'); // кнопка «Отправить»
    const resultContainer = document.getElementById('result-container');
    const resultVideo = document.getElementById('result-video'); // <video> с отмеченными животными
    let selectedFile = null; // будет хранить выбранный объект File

    //В JavaScript-части я использую обычные функции, обработчики событий и встроенные API браузера 
    //Когда пользователь выбирает видео, срабатывает событие change и запускается функция предпросмотра.
    //При клике на кнопку — срабатывает событие click, формируется объект FormData, и файл отправляется через fetch() на backend.
    //Мы также используем URL.createObjectURL — это встроенный способ показать видео до отправки.

    // Предпросмотр видео до отправки на сервер
    videoInput.addEventListener('change', function() { 
        if (videoInput.files && videoInput.files[0]) {
            selectedFile = videoInput.files[0];
            const url = URL.createObjectURL(selectedFile);
            preview.src = url;
            preview.style.display = 'block';
            resultContainer.style.display = 'none'; // скрываем обработанное видео при выборе нового
        } else {
            preview.src = '';
            preview.style.display = 'none';
        }
    });

    // Отправка видео на сервер и показ обработанного видео
    uploadBtn.addEventListener('click', function () {
        if (!selectedFile) {
            alert('Сначала выберите видео!');
            return;
        }
        const formData = new FormData();  // Формируем тело запроса: multipart/form-data
        formData.append('video', selectedFile);  // ключ 'video' — совпадает с backend‑кодом

         // Деактивируем кнопку, чтобы пользователь не нажимал повторно
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Обработка...';

        fetch('/upload', {   // fetch API (Promise‑базовый) — POST на маршрут /upload (Flask)
            method: 'POST',
            body: formData
        }) 
    //ответ от сервера обрабатывается через промисы (then, catch), и результат вставляется в HTML-страницу.
        .then(resp => resp.json())  // парсим JSON‑ответ backend’а
        .then(data => {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Отправить на обработку';
            if (data.result_url) {   // фласк вернул ссылку вида /result/<uuid>/file.mp4
                resultVideo.src = data.result_url;
                resultContainer.style.display = 'block';
                resultVideo.load();
                resultVideo.play();
            } else {
                alert(data.error || 'Ошибка обработки');
            }
        })
        .catch(err => {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Отправить на обработку';
            alert('Ошибка загрузки/обработки');
        });
    });
});
