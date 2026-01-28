# FastAPI 3-Tier Architecture

## Overview

The FastAPI application allows creating and listing todo items via JSON endpoints.

---

## Architecture

```
Client
  |
  v
[ALB] → [EC2 + FastAPI] → [RDS PostgreSQL]
```

* ALB in public subnets handles incoming HTTP requests
* EC2 hosts the FastAPI app
* RDS stores todo items

---

## Features

* `GET /` → Health check endpoint
* `POST /todos` → Create a new todo item
* `GET /todos` → List all todo items

---

## Setup Instructions

### EC2

1. Launch an Amazon Linux 2 EC2 instance
2. Install dependencies:

   ```bash
   sudo yum install python3 git -y
   pip3 install fastapi uvicorn sqlalchemy psycopg2-binary
   ```
3. Upload your FastAPI project code

### RDS

1. Launch a PostgreSQL RDS instance in a private subnet
2. Note the **DB user, password, endpoint, and database name**
3. Security group: allow inbound 5432 from EC2 SG

### FastAPI Configuration

Update `main.py` with your DB settings:

```python
DB_USER = 'postgres'
DB_PASS = 'YourPassword'
DB_NAME = 'postgres'
DB_HOST = '<rds-endpoint>'
DB_PORT = '5432'
```

### Running FastAPI

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### ALB Setup

* Create ALB in public subnets
* Target Group: HTTP 8000, health check path `/`
* Security Groups:

  * ALB: inbound 80 from 0.0.0.0/0
  * EC2: inbound 8000 from ALB SG

---

## Testing

```bash
# Health check
curl http://<ALB_DNS>/
<img width="1369" height="234" alt="Screenshot from 2026-01-27 22-12-43" src="https://github.com/user-attachments/assets/91740da3-838f-44a8-8c89-dffc7031ffbc" />

# Create todo
curl -X POST http://<ALB_DNS>/todos -H "Content-Type: application/json" -d '{"title":"Learn AWS"}'


# List todos
curl http://<ALB_DNS>/todos
<img width="915" height="490" alt="Screenshot from 2026-01-28 00-05-26" src="https://github.com/user-attachments/assets/d480fc7f-6d71-4367-b62d-63df311bf481" />

```

---

## Production Tips

* Run Uvicorn via **systemd** or **supervisor** for persistent deployment
* Use **HTTPS** via ACM on ALB
* Enable **CloudWatch logging** for monitoring
* Backup RDS using snapshots
* For concurrency, use `gunicorn` with Uvicorn workers
* Since you need access to the server you can use serial console or SSM + NAT Gateway since you need this to pull a repro

---


