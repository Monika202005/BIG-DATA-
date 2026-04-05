# AI-Powered E-commerce Recommendation Engine
*Setup and Run Guide*

Welcome to your new Advanced E-commerce Recommendation Engine! Follow these step-by-step instructions to get the application running locally on your computer.

---

## 🔷 1. ENVIRONMENT SETUP

Before you begin, make sure your computer has the following tools installed:

1. **Python (v3.8 or newer)**: Required to run the FastAPI backend and Machine Learning algorithms.
   - *Check*: Open your terminal and type `python3 --version`.
2. **Node.js (v18 or newer)**: Required to run the React frontend.
   - *Check*: Open your terminal and type `node -v` and `npm -v`.

---

## 🔷 2. BACKEND SETUP (FastAPI)

The backend powers the Apriori algorithms and serves the data. We need to run it in its own terminal window.

### Step-by-Step Commands:
1. **Open a new Terminal window** and navigate to your `backend` folder:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** to keep dependencies isolated:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Mac/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

4. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

> **Expected Output:** You should see `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`. Leave this terminal **open & running**.

---

## 🔷 3. FRONTEND SETUP (React + Vite)

The frontend is the visual dashboard you interact with. We need to run it in a **second, separate terminal window**.

### Step-by-Step Commands:
1. **Open a second Terminal window** and navigate to your `frontend` folder:
   ```bash
   cd frontend
   ```

2. **Install the required Node packages (if you haven't already)**:
   ```bash
   npm install
   ```

3. **Start the Vite Development server**:
   ```bash
   npm run dev
   ```

> **Expected Output:** You should see `➜  Local:   http://localhost:5173/`. Leave this terminal **open & running**.

---

## 🔷 4. HOW TO VERIFY EVERYTHING IS WORKING

1. Open your web browser (Chrome, Safari, Firefox, etc.).
2. Go to: **http://localhost:5173**
3. **What you should see**: A premium dashboard titled "Smarter Suggestions, Explainable Results". 

**Test the Recommendation Engine:**
1. Click the **"Simulate User"** button at the top right to watch the AI automatically inject products and spit out predictions dynamically!
2. **Alternatively (Manual mode)**: Click the Search bar and type `Laptop`. Add it to your active basket.
3. You should instantly see a card like `Mouse` appear with a **Green (Strong)** Confidence badge and an explanation citing *"Recommended because X% of users who bought Laptop also bought this."*

---

## 🔷 5. COMMON ERRORS & FIXES

Here’s how to troubleshoot if something goes wrong:

| Issue | How to Fix It |
| :--- | :--- |
| **Port already in use (`error: [Errno 98] Address already in use`)** | Another app is using port 8000 or 5173. Stop other servers or change the port (e.g. `uvicorn main:app --port 8001`) |
| **ModuleNotFoundError (e.g., 'No module named fastapi')** | You forgot to activate your virtual environment. Run `source venv/bin/activate` in the backend folder, then `pip install -r requirements.txt` again. |
| **Cross-Origin / Network Error in Browser** | The React app can't talk to the backend. Ensure your backend terminal is actually running and there are no crash errors. |
| **"npm: command not found"** | You do not have Node.js installed. Download it from `nodejs.org`. |

---

## 🔷 6. OPTIONAL: RUN WITH DOCKER (EASIEST WAY)

If you have **Docker Desktop** installed, you can skip steps 2 and 3 completely! Docker packages the whole stack and runs it for you in one command.

1. Open your terminal and navigate to the **root** folder:
   ```bash
   cd dbms_proj_6
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```

3. Go to `http://localhost:5173` in your browser.
*(To stop the server later, type `docker-compose down`).*
