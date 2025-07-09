let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const audioPlayer = document.getElementById("audioPlayer");
const aiText = document.getElementById("aiText");
let stopLimit = 0;
let fileId = null;

startBtn.addEventListener("click", async () => {
    audioChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm; codecs=opus" });

    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
            console.log("Получено данных:", event.data.size, "байт");
        }
    };

    mediaRecorder.onstop = async () => {
        if (audioChunks.length === 0) {
            console.error("Нет записанных данных!");
            return;
        }

        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "test.webm");

        aiText.textContent = "⏳ Обрабатываем...";

        try {
            // Отправляем аудио на сервер
            const uploadResp = await fetch("/upload_audio", {
                method: "POST",
                body: formData
            });

            const uploadData = await uploadResp.json();
            console.log(uploadData)
            fileId = uploadData.audio_url; // сервер должен вернуть уникальный ID
            textOu = uploadData.text;

            // Ждём готовности ответа
            await pollForResult(fileId, textOu);
        } catch (err) {
            aiText.textContent = "❌ Ошибка при загрузке: " + err.message;
        }
    };

    mediaRecorder.start(500);
    startBtn.disabled = true;
    stopBtn.disabled = false;
});

stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }

    startBtn.disabled = false;
    stopBtn.disabled = true;
});

async function pollForResult(id, textOu) {
    try {
        const interval = 2000;

        const poll = async () => {
            const response = await fetch(`/get_audio/${id}`);
            const data = await response.json();

            if (data.status === "ready") {
                setTimeout(()=>{}, 3000)
                aiText.textContent = textOu;
                audioPlayer.src = data.audio_url;
                audioPlayer.play();
            } else if (data.status === "processing") {
                if (stopLimit === 30){
                    aiText.textContent = "❌ Ошибка при обработке на сервере.";
                }else{
                    stopLimit ++;
                    setTimeout(poll, interval); // Пробуем снова через 2 сек
                }
            }
        };

        await poll();
    } catch (err) {
        aiText.textContent = "❌ Ошибка при получении ответа: " + err.message;
    }
}