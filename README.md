# 🛒 AI-Powered E-Commerce Recommendation Engine

> *Smarter Suggestions, Explainable Results*

---

## 👥 Team Members

* **Monika** – Frontend + backend
* **Vaasvi**– Backend 

---

## 📸 Project Overview

This project is a **DBMS + Big Data capstone project** that builds an intelligent e-commerce recommendation system using:

* Apriori Association Rules
* Apache Spark MLlib (ALS)
* Real-time tracking with MongoDB

---

## 📁 Repository Structure

```
project_eval_tool/
├── backend/        # FastAPI backend (APIs, ML logic)
├── frontend/       # React frontend UI
├── ai_service/     # AI/ML modules
├── bigdata/        # Spark jobs
├── docker-compose.yml
├── README.md
```

---

## 🧠 Tech Stack

* **Frontend:** React + Vite
* **Backend:** FastAPI (Python)
* **Database:** MySQL (OLTP + Data Warehouse)
* **Tracking:** MongoDB
* **Big Data:** Apache Spark (PySpark)

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/Monika202005/BIG-DATA-
cd BIG-DATA-
```

---

### 2. Backend Setup

```
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Frontend Setup

```
cd frontend
npm install
```

---

## ▶️ How to Execute the Project

### Run Backend

```
cd backend
uvicorn main:app --reload
```

👉 Runs on: http://localhost:8000

---

### Run Frontend

```
cd frontend
npm run dev
```

👉 Runs on: http://localhost:5173

---

### Run Spark Job (Optional)

```
python bigdata/spark_jobs/recommend.py
```

---

## 🌐 API Endpoints

* `/recommend` → Product recommendations
* `/analytics` → Analytics data
* `/products` → Product list
* `/api/spark/run` → Run Spark job

---

## 🎥 Demo Video

👉 Add your 2-minute demo video link here:
(YouTube / Google Drive link)

---

## ✨ Features

* Real-time recommendations
* Apriori association rules
* Spark ML collaborative filtering
* Explainable AI results
* Analytics dashboard

---

## 🗄️ Database Used

* MySQL (OLTP + Data Warehouse)
* MongoDB (real-time tracking)

---

## 📌 GitHub Repository

👉 https://github.com/Monika202005/BIG-DATA-

---

