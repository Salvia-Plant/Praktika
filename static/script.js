document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('upload-btn');
    const videoInput = document.getElementById('video-upload');
    const resultContainer = document.getElementById('result-container');
    const resultVideo = document.getElementById('result-video');

    uploadBtn.addEventListener('click', function () {
        if (videoInput.files.length === 0) {
            alert('Выберите видео!');
            return;
        }
        const formData = new FormData();
        formData.append('video', videoInput.files[0]);
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Загрузка...';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(resp => resp.json())
        .then(data => {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Загрузить и обработать';
            if (data.result_url) {
                resultVideo.src = data.result_url;
                resultContainer.classList.remove('hidden');
            } else {
                alert(data.error || 'Ошибка обработки');
            }
        })
        .catch(err => {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Загрузить и обработать';
            alert('Ошибка загрузки/обработки');
        });
    });
});
