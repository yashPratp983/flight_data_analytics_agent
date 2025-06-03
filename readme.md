# 🚀 Full Stack App with FastAPI (Backend) & Streamlit (Frontend)

This project contains:
- A **FastAPI** backend located in the `app/` directory
- A **Streamlit** frontend located in the `client/` directory

Both components are containerized using Docker.

---

## ⚙️ Prerequisites

- Docker installed on your machine

---

## 🚀 Running the Backend (FastAPI)

```
cd app
docker build -t fastapi-backend .
docker run -d -p 8000:8000 fastapi-backend
```

Access the API documentation at: `http://localhost:8000/docs`

---

## 🖼️ Running the Frontend (Streamlit)

```
cd client
docker build -t streamlit-frontend .
docker run -d -p 8501:8501 streamlit-frontend
```

Access the Streamlit app at: `http://localhost:8501`

---

## 🔁 Connecting Streamlit to FastAPI

### Option 1: Localhost (Windows/Mac)

Use the following URL in your Streamlit app to call the FastAPI backend:

```
http://host.docker.internal:8000
```

### Option 2: Docker network

```
docker network create fullstack-net
docker run -d --network fullstack-net --name backend -p 8000:8000 fastapi-backend
docker run -d --network fullstack-net --name frontend -p 8501:8501 streamlit-frontend
```

Use the following URL in your Streamlit app:

```
http://backend:8000
```

---

## 🧹 Cleaning Up

```
docker ps -a
docker stop <container_id>
docker rm <container_id>
docker rmi fastapi-backend streamlit-frontend
```

---

## 📜 License

MIT License
