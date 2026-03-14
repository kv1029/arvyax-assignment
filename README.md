# AI-Assisted Journal System

## Overview

The AI-Assisted Journal System allows users to write journal entries after completing immersive nature sessions (forest, ocean, mountain).
The system stores these entries, analyzes emotional tone using a Large Language Model (LLM), and provides insights into the user’s mental state over time.

This project demonstrates full-stack development, API design, LLM integration, and data analysis.

---

## Features

### 1. Journal Entry Storage

Users can write and save journal entries associated with a nature ambience.

### 2. Emotion Analysis (LLM)

Journal text is analyzed using an LLM to extract:

* Primary emotion
* Key themes/keywords
* A short summary

### 3. Insights Dashboard

Aggregated insights about a user’s mental patterns including:

* Total journal entries
* Most frequent emotion
* Most used ambience
* Recent keywords

### 4. Minimal Frontend

A simple UI where users can:

* Write journal entries
* View previous entries
* Run emotion analysis
* View insights

---

## Tech Stack

Backend

* Python FastAPI
* MongoDB (Atlas)
* Gemini LLM API

Frontend

* React

Other Tools

* Uvicorn
* Axios

---

## Project Structure

arvyax-assignment
│
├── backend
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   └── package.json
│
├── README.md
└── ARCHITECTURE.md

---

## Setup Instructions

### 1. Clone Repository

git clone <repository_url>
cd arvyax-assignment

---

### 2. Backend Setup

Navigate to backend folder

cd backend

Create virtual environment

python -m venv venv

Activate environment

Windows
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Run FastAPI server

uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

---

### 3. Frontend Setup

Open new terminal

cd frontend

Install dependencies

npm install

Run React app

npm start

Frontend will run at:

http://localhost:3000

---

## API Endpoints

### Create Journal Entry

POST /api/journal

Example Request

{
"userId": "123",
"ambience": "forest",
"text": "I felt calm today after listening to the rain."
}

---

### Get User Journal Entries

GET /api/journal/{userId}

Example

GET /api/journal/123

---

### Analyze Journal Emotion

POST /api/journal/analyze

Example Request

{
"text": "I felt calm today after listening to the rain"
}

Example Response

{
"emotion": "calm",
"keywords": ["rain","nature","peace"],
"summary": "User experienced relaxation during the forest session"
}

---

### Get User Insights

GET /api/journal/insights/{userId}

Example Response

{
"totalEntries": 8,
"topEmotion": "calm",
"mostUsedAmbience": "forest",
"recentKeywords": ["focus","nature","rain"]
}

---

## Example Usage Flow

1. User writes a journal entry after a session
2. Entry is stored in MongoDB
3. User clicks Analyze
4. LLM analyzes the text and returns emotion insights
5. Insights API aggregates historical patterns

---

## Future Improvements

* User authentication
* Emotion trend graphs
* Redis caching for LLM responses
* Docker deployment
* Rate limiting
* Background job queue for LLM tasks

---

## Author

Ashu Gupta
B.Tech Computer Science Student
