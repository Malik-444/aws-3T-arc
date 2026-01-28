# 3-Tier Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/eb743f19-3b24-4e45-a041-ad7d22cffed2" />


## Overview

This project demonstrates a production-style 3-tier web application architecture on AWS, designed using cloud best practices for network isolation, security, and scalability.

The application is built with FastAPI and deployed on an EC2 instance in a private subnet, fronted by an Application Load Balancer (ALB) in a public subnet. A PostgreSQL database hosted on Amazon RDS resides in private subnets and is securely accessed using security group–to–security group rules.

Outbound internet access for private resources is enabled via a NAT Gateway, and AWS Systems Manager (SSM) is used for secure, keyless instance access—eliminating the need for a bastion host or public SSH access.

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


# Create todo
curl -X POST http://<ALB_DNS>/todos -H "Content-Type: application/json" -d '{"title":"Learn AWS"}'


# List todos
curl http://<ALB_DNS>/todos


```
<img width="1369" height="234" alt="Screenshot from 2026-01-27 22-12-43" src="https://github.com/user-attachments/assets/946fe388-548c-408a-a692-cf6003041c02" />

<img width="915" height="490" alt="Screenshot from 2026-01-28 00-05-26" src="https://github.com/user-attachments/assets/2a16ae46-0846-48a8-8bbd-088c58708dbb" />

---

## Production Tips

* Run Uvicorn via **systemd** or **supervisor** for persistent deployment
* Use **HTTPS** via ACM on ALB
* Enable **CloudWatch logging** for monitoring
* Backup RDS using snapshots
* For concurrency, use `gunicorn` with Uvicorn workers
* Since you need access to the server you can use serial console or SSM + NAT Gateway since you need this to pull a repro

---


