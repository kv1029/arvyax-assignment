# System Architecture

## Overview

The AI-Assisted Journal System is designed as a full-stack application consisting of:

Frontend (React)
Backend API (FastAPI)
Database (MongoDB)
LLM Service (Gemini)

Users interact with the React frontend which communicates with the FastAPI backend via REST APIs.
The backend stores journal entries in MongoDB and uses an LLM API to analyze emotional content.

---

## System Components

### 1. Frontend

The frontend is built with React and provides a simple interface where users can:

* Write journal entries
* View previous entries
* Trigger emotion analysis
* View personal insights

The frontend communicates with backend APIs using HTTP requests.

---

### 2. Backend

The backend is implemented using FastAPI.

Responsibilities include:

* Handling API requests
* Storing and retrieving journal entries
* Calling the LLM for emotion analysis
* Aggregating insights from stored data

FastAPI was chosen due to its performance, async support, and automatic API documentation.

---

### 3. Database

MongoDB is used to store journal entries.

Example schema:

{
"userId": "123",
"ambience": "forest",
"text": "I felt calm today after listening to the rain",
"createdAt": "timestamp"
}

MongoDB allows flexible storage and horizontal scaling.

---

### 4. LLM Integration

The system uses a Large Language Model (Gemini) to analyze journal text.

The model extracts:

* Emotion classification
* Key themes or keywords
* A short summary

The backend sends the journal text to the LLM API and parses the structured response.

---

# Scaling to 100k Users

To scale the system to support 100k users:

1. Deploy backend services using containerized environments such as Docker.
2. Use a load balancer to distribute traffic across multiple FastAPI instances.
3. Use MongoDB Atlas with sharding for horizontal database scaling.
4. Offload LLM analysis to background workers using a queue system such as Redis + Celery.

This architecture ensures the system can handle high concurrency and large data volumes.

---

# Reducing LLM Cost

LLM usage can become expensive at scale. Several strategies can reduce cost:

1. Cache previously analyzed journal texts.
2. Use smaller and faster models when possible.
3. Limit analysis to meaningful journal entries.
4. Batch multiple analysis tasks when feasible.

These strategies significantly reduce the number of LLM calls.

---

# Caching Repeated Analysis

To avoid repeated LLM calls for identical text:

1. Store analyzed results in a cache layer.
2. When a new analysis request arrives, check if the text already exists in the cache.
3. If a match is found, return the cached result instead of calling the LLM.

Redis or a dedicated MongoDB collection can be used for caching.

This approach reduces latency and cost.

---

# Protecting Sensitive Journal Data

Journal entries may contain highly personal information. To protect user data:

1. Use HTTPS for secure communication.
2. Encrypt sensitive data at rest in the database.
3. Implement authentication and authorization using JWT.
4. Restrict access so users can only read their own journal entries.
5. Avoid storing sensitive information in logs.

These measures ensure privacy and data security.

---

# Future Improvements

Possible enhancements include:

* User authentication system
* Emotion trend visualization
* Redis caching layer
* Rate limiting for API protection
* Docker based deployment
* CI/CD pipeline
