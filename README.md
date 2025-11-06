# 🤖 AI Agent – On-Device Chat Assistant (React Native + FastAPI + Gemini)

A full-stack AI-powered chat assistant built with **React Native** (client) and **FastAPI** (server), powered by **Google Gemini AI**.  
This project demonstrates how to combine local persistence, tool-based reasoning (weather, AQI, calculator, etc.), and cloud-based AI for an interactive chat experience.

---

## 🚀 Features

- 💬 Real-time chat interface (React Native)
- 🧠 Context-aware AI reasoning using Gemini
- 🌦️ Built-in tools:
  - Weather lookup  
  - Air Quality Index (AQI)  
  - Calculator  
  - Current Time / Date
- 🗂️ Local SQLite memory with message summarization
- 📡 Automatic location detection via IP for weather/air quality
- 🔒 Stateless, open-source friendly design

---

## 🧭 Project Structure

```
ai-agent/
├── MobileApp/            # React Native app
│   ├── src/
│   ├── package.json
│   └── ...
│
├── server/               # FastAPI backend
│   ├── core/
│   │   ├── agent.py
│   │   ├── db.py
│   │   ├── tools.py
│   ├── api.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── README.md             # root README (overview)
```

---

## 🧩 Project Setup

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/<your-username>/ai-agent.git
cd ai-agent
```

---

### 2️⃣ Backend Setup (FastAPI)

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Then update it with your **Gemini API key**.

Run the server:

```bash
uvicorn api:app --reload
```

Server runs on:  
👉 **http://127.0.0.1:8000**

---

### 3️⃣ Frontend Setup (React Native)

```bash
cd ../MobileApp
yarn install
yarn start
```

Then run on your target device:

```bash
yarn ios      # for iOS simulator
yarn android  # for Android device/emulator
```

> 💡 Make sure your FastAPI server is running before launching the app.

---

## ⚙️ Example `.env.example` (Server)

```bash
# --- AI Agent Backend Configuration ---
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=sqlite:///memory.db
```

---

## 🧠 Architecture Overview

| Layer | Description |
|-------|--------------|
| **React Native** | Chat UI + Local storage (AsyncStorage) |
| **FastAPI** | Middleware + conversation logic |
| **SQLite** | Persistent message history |
| **Gemini AI** | Natural language reasoning |
| **Tools** | Weather, AQI, calculator, time |

---

## 🧰 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|--------------|
| `POST` | `/chat` | Send message & get AI reply |
| `POST` | `/clear` | Clear chat history for a user |
| `GET`  | `/` | Health check |

---

## 📦 Example cURL

```bash
curl -X POST http://127.0.0.1:8000/chat      -H "Content-Type: application/json"      -d '{"user_id": "123", "message": "What’s the weather in Paris?"}'
```

---

## 🧾 License

This project is open-source under the **MIT License**.  
Feel free to fork, modify, and contribute!

---

## 🌟 Acknowledgements

- [Google Gemini AI](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React Native](https://reactnative.dev/)
