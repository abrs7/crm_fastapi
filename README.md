# FastAPI CRM

FastAPI CRM is a backend service built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL** to manage customer relationships efficiently.

## 🚀 Features
- User authentication and authorization
- Customer management
- API documentation with Swagger & Redoc
- Asynchronous database operations with SQLAlchemy
- Containerized using Docker & Docker Compose

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python
- **Database:** PostgreSQL, SQLAlchemy
- **Containerization:** Docker, Docker Compose

---

## 🏗️ Installation & Setup

### 1️⃣ Prerequisites
Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/fastapi-crm.git
cd fastapi-crm
```

### 3️⃣ Environment Variables
Create a `.env` file with the following content:
```ini
DATABASE_URL=postgresql://postgres:yourpassword@crm_db:5432/your_database
```

### 4️⃣ Start the Application
```sh
docker-compose up --build
```
This will start the FastAPI application and PostgreSQL database in containers.

### 5️⃣ Access API Docs
Once the service is running, open the browser and go to:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐞 Troubleshooting

### ❌ FastAPI Cannot Connect to Database
Run inside the FastAPI container:
```sh
docker exec -it fastapi_crm_web ping crm_db
```
If it fails, check if both services are in the same network:
```sh
docker network ls
```

### ❌ PostgreSQL Not Starting
Check logs:
```sh
docker logs crm_db
```

### ❌ Debugging Inside Containers
```sh
docker exec -it fastapi_crm_web /bin/sh
```

---

## 📜 License
This project is open-source under the MIT License.

