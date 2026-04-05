# 🛒 AI-Powered E-Commerce Recommendation Engine

> *Smarter Suggestions, Explainable Results* — A full-stack recommendation system combining Apriori association rules, Apache Spark MLlib collaborative filtering, and real-time MongoDB tracking.

---

## 📸 Overview

This project is a **college DBMS capstone** that implements a production-style e-commerce recommendation engine. It demonstrates OLTP/Data Warehouse database design, machine learning at scale with Apache Spark, and a real-time React dashboard.

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite (port 5173) |
| **Backend** | FastAPI / Python (port 8000) |
| **OLTP Database** | MySQL — `ecommerce_oltp` |
| **Data Warehouse** | MySQL — `ecommerce_dw` |
| **Activity Tracking** | MongoDB |
| **Big Data Engine** | Apache Spark (PySpark 3.4.1) |
| **ML Algorithm** | Spark MLlib — ALS Collaborative Filtering |
| **Association Rules** | Apriori Algorithm (custom pipeline) |

---

## ✨ Features

- 🔍 **Real-time product search** with instant recommendations
- 🤖 **Apriori Association Rules** — *"Users who bought X also bought Y"*
- ⚡ **Spark MLlib ALS Model** — collaborative filtering across all users
- 📊 **Analytics Dashboard** — top products, rule confidence, lift scores
- 🧪 **Simulate User** button — auto-injects products and shows predictions
- 📈 **Explainable AI** — every recommendation shows *why* it was made
- 🟢 **Confidence badges** — Strong / Medium / Weak color-coded signals
- 🗄️ **MongoDB activity tracking** — logs every user interaction

---

## 🏗️ Architecture

```
React Frontend (port 5173)
        ↕
FastAPI Backend (port 8000)
        ↕
┌───────────────────────────┐
│  Apriori Rules Engine     │  ← 176 pre-loaded rules in memory
│  rules_cache.json         │
└───────────────────────────┘
        ↕
┌───────────────────────────┐
│  Apache Spark (MLlib)     │  ← Big Data layer
│  ALS Recommendation Model │  ← Trains on user-product ratings
│  recommendations.json     │  ← Output served via API
└───────────────────────────┘
        ↕
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  MySQL OLTP  │  │  MySQL DW    │  │   MongoDB    │
│  (orders)    │  │  (analytics) │  │  (tracking)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL (running locally)
- MongoDB (running locally)
- Java 11+ (required for PySpark)

> **Check Java:** `java -version` — if not installed, download from [adoptium.net](https://adoptium.net/) and select Java 11 LTS.

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/dbms-proj.git
cd "dbms proj 4"
```

---

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyspark==3.4.1 findspark
```

---

### 3. Database Setup

Make sure MySQL is running, then create the databases:

```sql
CREATE DATABASE ecommerce_oltp;
CREATE DATABASE ecommerce_dw;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'Ecommerce_pass123!';
GRANT ALL PRIVILEGES ON ecommerce_oltp.* TO 'ecommerce_user'@'localhost';
GRANT ALL PRIVILEGES ON ecommerce_dw.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

---

### 4. Frontend Setup

```bash
cd frontend
npm install
```

---

## ▶️ Running the Project

You need **2 terminal windows** open simultaneously:

**Terminal 1 — Backend:**
```bash
cd backend
.\venv\Scripts\activate      # Windows
# source venv/bin/activate   # Mac/Linux
uvicorn main:app --reload
```
✅ Backend running at `http://localhost:8000`

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend running at `http://localhost:5173`

---

## ⚡ Running the Spark ML Job

The Spark job trains the ALS model and generates recommendations for all users. Run it once (or whenever you want to retrain):

```bash
# From project root, with venv activated
python bigdata/spark_jobs/recommend.py
```

**Expected output:**
```
✅ Spark Session started
✅ DataFrame created with 24 records
✅ ALS Model trained
✅ RMSE: 1.7481
✅ Saved to bigdata/spark_jobs/output/recommendations.json
✅ Done
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/recommend` | Get Apriori recommendations for a basket |
| `GET` | `/analytics` | Full analytics stats |
| `GET` | `/products` | All product list |
| `POST` | `/track` | Log user activity to MongoDB |
| `GET` | `/activity` | Retrieve tracked activity |
| `POST` | `/recalculate` | Retrain Apriori with new params |
| `POST` | `/api/spark/run` | Trigger Spark ALS ML job |
| `GET` | `/api/spark/recommendations/{user_id}` | Get Spark recs for a user |
| `GET` | `/api/spark/status` | Check Spark pipeline health |

**Interactive API docs:** `http://localhost:8000/docs`

---

## 🧪 Testing the Spark API

**Check status:**
```
GET http://localhost:8000/api/spark/status
```

**Trigger Spark job (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/spark/run" -Method POST
```

**Get recommendations for user 1:**
```
GET http://localhost:8000/api/spark/recommendations/1
```

**Sample response:**
```json
{
  "status": "success",
  "user_id": 1,
  "rmse": 1.7481,
  "data": {
    "user_id": 1,
    "recommendations": [
      { "product_id": 101, "product_name": "Laptop", "predicted_rating": 4.88 },
      { "product_id": 107, "product_name": "Keyboard", "predicted_rating": 4.13 },
      { "product_id": 102, "product_name": "Phone", "predicted_rating": 3.01 }
    ]
  }
}
```

---

## 📁 Project Structure

```
dbms proj 4/
├── backend/
│   ├── main.py                  ← FastAPI app + all API routes
│   ├── apriori_pipeline.py      ← Apriori rule mining
│   ├── mongo_connection.py      ← MongoDB connector
│   ├── patch_cache.py           ← Cache utilities
│   ├── rules_cache.json         ← 176 pre-computed Apriori rules
│   ├── stats_cache.json         ← Analytics data cache
│   └── requirements.txt
├── frontend/
│   └── ...                      ← React + Vite app
├── bigdata/
│   └── spark_jobs/
│       ├── recommend.py         ← PySpark ALS ML job
│       └── output/
│           └── recommendations.json  ← Spark output (generated)
├── db_connection.py             ← MySQL connection helpers
├── docker-compose.yml
└── README.md
```

---

## 🎓 Big Data Concepts Implemented

| Concept | Implementation | Location |
|---|---|---|
| **Distributed Computing** | `SparkSession.master("local[*]")` — all CPU cores in parallel | `recommend.py` |
| **Apache Spark** | PySpark 3.4.1 processing engine | `recommend.py` |
| **Spark MLlib** | ALS (Alternating Least Squares) collaborative filtering | `recommend.py` |
| **Spark DataFrames** | `spark.createDataFrame()` — distributed data structure | `recommend.py` |
| **ETL Pipeline** | Extract data → Spark transforms → JSON output | `recommend.py` |
| **Train/Test Split** | `randomSplit([0.8, 0.2], seed=42)` — 80/20 validation | `recommend.py` |
| **RMSE Evaluation** | `RegressionEvaluator` — model accuracy metric | `recommend.py` |
| **Batch Processing** | `recommendForAllUsers(5)` — all users at once | `recommend.py` |
| **Cold Start Handling** | `coldStartStrategy="drop"` — handles new users | `recommend.py` |
| **Big Data API Layer** | 3 FastAPI endpoints serving Spark output | `main.py` |

---

## 🗄️ Database Schema

### MySQL — OLTP (`ecommerce_oltp`)
Stores raw transactional data: users, products, orders, order_items.

### MySQL — Data Warehouse (`ecommerce_dw`)
Stores aggregated analytics: fact tables, dimension tables for reporting.

### MongoDB
Stores real-time user activity logs (product views, basket additions, clicks).

---

## ⚠️ Known Issues

- Frontend "Business Intelligence metrics" section may show loading skeletons — this is a pre-existing UI bug unrelated to backend functionality
- For demo purposes, use `http://localhost:8000/docs` (Swagger UI) to test all APIs interactively
