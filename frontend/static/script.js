document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('upload-btn');
    const videoUpload = document.getElementById('video-upload');
    const resultContainer = document.querySelector('.result-container');
    const resultVideo = document.getElementById('result-video');
    const animalsCount = document.getElementById('animals-count');
    const confidence = document.getElementById('confidence');

    // Обработка клика по кнопке
    uploadBtn.addEventListener('click', function() {
        if (videoUpload.files.length === 0) {
            alert('Пожалуйста, выберите видео файл!');
            return;
        }

        uploadVideo(videoUpload.files[0]);
    });

    // Функция загрузки видео
    async function uploadVideo(file) {
        const formData = new FormData();
        formData.append('video', file);

        try {
            uploadBtn.disabled = true;
            uploadBtn.textContent = 'Обработка...';

            const response = await fetch('http://192.168.62.197:5000/process_video', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Ошибка сервера');
            }

            const data = await response.json();
            
            // Показываем результат
            resultVideo.src = data.result_url;
            resultContainer.classList.remove('hidden');
            
            // В реальном проекте здесь бы был запрос к API для получения статистики
            animalsCount.textContent = '2'; // Пример данных
            confidence.textContent = '87'; // Пример данных
            
            // Прокрутка к результатам
            resultContainer.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при обработке видео: ' + error.message);
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Анализировать видео';
        }
    }
});