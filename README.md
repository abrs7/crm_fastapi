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
# CRM API Documentation

## Leads

### Search Leads
**GET** `/api/leads/search`
Search for leads based on query parameters.

### Create Lead
**POST** `/api/leads/`
Create a new lead.

### Get Leads
**GET** `/api/leads/`
Retrieve a list of leads.

### Get Lead by ID
**GET** `/api/leads/{lead_id}`
Retrieve details of a specific lead by ID.

### Update Lead Status
**PATCH** `/api/leads/{lead_id}/status`
Update the status of a lead.

---

## Quotations

### Create Quotation
**POST** `/api/quotations/`
Create a new quotation.

### Get Quotations
**GET** `/api/quotations/`
Retrieve a list of quotations.

### Get Quotation by ID
**GET** `/api/quotations/{quotation_id}`
Retrieve details of a specific quotation by ID.

### Update Quotation Status
**PATCH** `/api/quotations/{quotation_id}/status`
Update the status of a quotation.

### Approve Quote
**POST** `/api/quotations/{quote_id}/approve`
Approve a quotation.

### Reject Quote
**POST** `/api/quotations/{quote_id}/reject`
Reject a quotation.

---

## Default Endpoints

### Register
**POST** `/register`
Register a new user.

### Login
**POST** `/token`
Authenticate a user and obtain an access token.

### Read Root
**GET** `/`
Default API root endpoint.

### Get Audit Log by ID
**GET** `/audit_logs/{log_id}`
Retrieve a specific audit log by ID.

### Get All Audit Logs
**GET** `/audit_logs`
Retrieve all audit logs.



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

