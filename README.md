# 🎙 GPT Voice Assistant (Flask)

> Голосовой ассистент на Flask с записью через браузер, распознаванием речи через Deepgram, обработкой через OpenAI GPT-4o и синтезом речи через OpenAI TTS.

---

## 📦 Возможности

- 🎤 Запись голоса прямо в браузере
- 🧠 Распознавание речи: **Deepgram**
- 💬 Ответы от **GPT‑4o** (OpenAI) с сохранением контекста
- 🔊 Озвучка ответов с помощью **OpenAI TTS**
- 🗂 История диалога хранится в `.json` файле на сессии пользователя
- 🐳 Лёгкий запуск через Docker

  ## 🚀 Установка
```bash
git clone https://github.com/valvklik007/gpt-voice-assistant-flask.git
cd gpt-voice-assistant-flask
```
### Создай `.env` файл
В корне проекта создай файл `.env`:

```env
OPENAI_API_KEY=your_openai_key_here
DEEPGRAM_API_KEY=your_deepgram_key_here
```
### Запуск через Docker (рекомендуется)
```bash
docker-compose up --build
```
Приложение будет доступно: http://127.0.0.1:8888
