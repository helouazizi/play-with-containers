# Play With Containers: Microservices Architecture

A production-ready microservices orchestration project utilizing Docker and Docker Compose. This architecture demonstrates service isolation, asynchronous messaging with RabbitMQ, persistent storage with PostgreSQL, and a centralized API Gateway.

## 🏗 Architecture Overview

The project consists of six interconnected containers organized within a private Docker network. To ensure security, only the API Gateway is exposed to the host machine.

*   **API Gateway (Port 3000):** The single entry point. Routes requests to internal services and handles RabbitMQ message publishing.
*   **Inventory Service (Port 8080 - Internal):** Manages movie data.
*   **Billing Service (Port 8080 - Internal):** Asynchronously processes billing tasks via RabbitMQ.
*   **Database Cluster:** Two isolated PostgreSQL instances for Inventory and Billing data.
*   **Message Broker:** RabbitMQ instance for inter-service communication.

![Architecture Diagram](./resources/play-with-containers-py.png)

## 📁 Project Structure

```text
.
├── srcs/
│   ├── api-gateway-app/   # Flask Gateway & Proxy logic
│   ├── inventory-app/     # Inventory CRUD logic
│   └── billing-app/       # Billing consumer & logic
├── docker-compose.yml     # Orchestration manifest
├── .env.example           # Template for environment secrets
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

*   **Docker Engine:** version 20.10.0+
*   **Docker Compose:** version 2.0.0+
*   **Linux/Unix environment** (Recommended)

### 1. Configuration

The project uses environment variables for sensitive data. Copy the example file and configure your credentials:

```bash
cp .env.example .env
```

**Important:** Ensure the `.env` file is never committed to version control (already handled in `.gitignore`).

### 2. Deployment

Build and launch the entire infrastructure in detached mode:

```bash
docker-compose up -d --build
```

This command will:
1.  Build custom images for the Gateway, Inventory, and Billing services.
2.  Pull stable Alpine/Debian-based images for PostgreSQL and RabbitMQ.
3.  Setup the `backend-network`.
4.  Initialize persistent volumes for databases and logs.

### 3. Verification

Check the status of the containers:

```bash
docker-compose ps
```

## 🛠 API Usage

All requests must be sent to the **API Gateway** on port `3000`.

### Inventory Management (`/api/movies`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/movies` | List all movies |
| `POST` | `/api/movies` | Create a movie (JSON: title, description) |
| `GET` | `/api/movies/<id>` | Get movie details |
| `PUT` | `/api/movies/<id>` | Update a movie |
| `DELETE` | `/api/movies/<id>` | Delete a specific movie |
| `DELETE` | `/api/movies` | Wipe all movies |

### Billing Management (`/api/billing`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/billing` | Submit order to queue (JSON: user_id, number_of_items, total_amount) |
| `GET` | `/api/billing` | Fetch processed billing records |

## 🔒 Security & Performance

*   **Isolation:** Only the `api-gateway-app` maps ports to the host. Databases and brokers are invisible to external scans.
*   **Persistence:** Data survives container restarts via named Docker volumes (`inventory-db-data`, `billing-db-data`).
*   **Resilience:** Containers use `restart: always` to ensure high availability during crashes.
*   **Logging:** API Gateway logs are persisted to a host-mounted volume for audit purposes.
*   **Base Images:** Built on stable `alpine` variants to reduce attack surface and image size.

## 🧪 Automated Testing

A test script is provided to validate the Inventory CRUD cycle through the Gateway:

```bash
# Install dependencies
pip install requests python-dotenv

# Run tests
python3 srcs/inventory-app/test_api.py
```

*Note: Ensure `API_GATEWAY_HOST=localhost` is set in your `.env` when running tests from the host machine.*

## 📈 Troubleshooting

**View Logs:**
```bash
docker-compose logs -f [service_name]
```

**Restart a specific service:**
```bash
docker-compose restart inventory-app
```

**Clean Slate (Warning: Deletes all data):**
```bash
docker-compose down -v
```

---
*Developed as part of the play-with-containers project.*