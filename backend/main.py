# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List
# import json
# from pathlib import Path
# from apriori_pipeline import calculate_rules
# import subprocess
# import json
# from fastapi import APIRouter
# router = APIRouter()
# import subprocess, json, os
# from fastapi import APIRouter

# RECS_PATH = os.path.join(os.path.dirname(__file__), 
#             "../bigdata/spark_jobs/output/recommendations.json")
# SPARK_SCRIPT = os.path.join(os.path.dirname(__file__),
#             "../bigdata/spark_jobs/recommend.py")

# @app.post("/api/spark/run")
# def run_spark_job():
#     """Triggers the Spark ML job"""
#     try:
#         result = subprocess.run(
#             ["python", SPARK_SCRIPT],
#             capture_output=True, text=True, timeout=120
#         )
#         if result.returncode == 0:
#             return {"status": "success", "log": result.stdout}
#         else:
#             return {"status": "error", "log": result.stderr}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.get("/api/spark/recommendations/{user_id}")
# def get_recommendations(user_id: int):
#     """Returns Spark-generated recommendations for a user"""
#     try:
#         with open(RECS_PATH) as f:
#             all_recs = json.load(f)
#         user_recs = next((r for r in all_recs if r["user_id"] == user_id), None)
#         if user_recs:
#             return {"status": "success", "data": user_recs}
#         return {"status": "no_data", "message": f"No recs for user {user_id}. Run /api/spark/run first."}
#     except FileNotFoundError:
#         return {"status": "no_data", "message": "Run POST /api/spark/run first"}

# @app.get("/api/spark/status")
# def spark_status():
#     """Check if Spark output exists"""
#     exists = os.path.exists(RECS_PATH)
#     return {
#         "spark_output_exists": exists,
#         "engine": "PySpark 3.4.1 (local mode)",
#         "model": "ALS Collaborative Filtering (MLlib)"
#     }

# # ── Route 1: Trigger Spark Job ────────────────────────────────────────────────
# @app.post("/api/spark/run")
# def run_spark_job():
#     """
#     Triggers the Spark recommendation job inside the spark-master container.
#     Call this from your React dashboard with a 'Run Spark Job' button.
#     """
#     try:
#         result = subprocess.run([
#             "docker", "exec", "spark-master",
#             "spark-submit",
#             "--master", "spark://spark-master:7077",
#             "--packages", "mysql:mysql-connector-java:8.0.33",
#             "/opt/spark-jobs/recommend.py"
#         ], capture_output=True, text=True, timeout=300)

#         if result.returncode == 0:
#             return {"status": "success", "message": "Spark job completed!", "log": result.stdout[-2000:]}
#         else:
#             return {"status": "error", "message": result.stderr[-2000:]}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


# # ── Route 2: Read Recommendations from HDFS via Spark ────────────────────────
# @app.get("/api/spark/recommendations/{user_id}")
# def get_spark_recommendations(user_id: int):
#     """
#     Reads the recommendation parquet file from HDFS and returns
#     top-5 products for a given user.
#     """
#     try:
#         result = subprocess.run([
#             "docker", "exec", "spark-master",
#             "python3", "-c", f"""
# from pyspark.sql import SparkSession
# spark = SparkSession.builder.appName('ReadRecs').config('spark.hadoop.fs.defaultFS','hdfs://namenode:9000').getOrCreate()
# spark.sparkContext.setLogLevel('ERROR')
# df = spark.read.parquet('hdfs://namenode:9000/ecommerce/recommendations')
# user_df = df.filter(df.user_id == {user_id})
# import json
# rows = user_df.toJSON().collect()
# print('RESULT:' + json.dumps(rows))
# spark.stop()
# """
#         ], capture_output=True, text=True, timeout=60)

#         # Parse the result
#         output = result.stdout
#         if "RESULT:" in output:
#             json_str = output.split("RESULT:")[1].strip()
#             return {"status": "success", "user_id": user_id, "recommendations": json.loads(json_str)}
#         else:
#             return {"status": "no_data", "message": "Run the Spark job first via POST /api/spark/run"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


# # ── Route 3: HDFS Health Check ────────────────────────────────────────────────
# @app.get("/api/hdfs/status")
# def hdfs_status():
#     """Check if HDFS is up and list stored files."""
#     try:
#         result = subprocess.run([
#             "docker", "exec", "namenode",
#             "hdfs", "dfs", "-ls", "-R", "/ecommerce"
#         ], capture_output=True, text=True, timeout=15)
#         return {
#             "status": "connected",
#             "files": result.stdout,
#             "hdfs_ui": "http://localhost:9870"
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# app = FastAPI(title="Apriori Recommendation Engine API")

# # Setup CORS for React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# RULES_CACHE_PATH = Path(__file__).parent / "rules_cache.json"
# STATS_CACHE_PATH = Path(__file__).parent / "stats_cache.json"

# # In-memory storage for fast lookup (<100ms)
# apriori_rules = []
# apriori_stats = {}

# @app.on_event("startup")
# async def startup_event():
#     load_rules()

# def load_rules():
#     global apriori_rules, apriori_stats
#     try:
#         if RULES_CACHE_PATH.exists():
#             with open(RULES_CACHE_PATH, 'r') as f:
#                 apriori_rules = json.load(f)
#             print(f"Loaded {len(apriori_rules)} rules into memory.")
#         else:
#             print("Warning: rules_cache.json not found.")
            
#         if STATS_CACHE_PATH.exists():
#             with open(STATS_CACHE_PATH, 'r') as f:
#                 apriori_stats = json.load(f)
#             print("Loaded analytics stats into memory.")
#     except Exception as e:
#         print(f"Error loading cache: {e}")

# class RecommendRequest(BaseModel):
#     products: List[str]
# @app.get("/")
# def home():
#     return {"message": "Backend running"}

# @app.post("/recommend")
# async def get_recommendations(req: RecommendRequest):
#     print(f"DEBUG: Received recommendation POST request: {req.products}")
    
#     # FALLBACK / SMART DEFAULTS: If no product is selected, return trending products
#     if not req.products:
#         if not apriori_stats or "top_items" not in apriori_stats:
#             return {"recommendations": [], "is_fallback": True}
            
#         trending = []
#         # Get top 5 items from stats
#         top_items = list(apriori_stats["top_items"].items())[:5]
#         for item, count in top_items:
#             trending.append({
#                 "item": item,
#                 "confidence": 1.0, # Dummy for trending
#                 "lift": 1.0,
#                 "support": 1.0,
#                 "based_on": [],
#                 "explanation": f"Trending Product! Purchased {int(count)} times recently.",
#                 "is_trending": True
#             })
#         return {"recommendations": trending, "is_fallback": True}
        
#     input_set = set(req.products)
#     recommendations_map = {}
    
#     # Iterate through all precomputed rules to find matching itemsets
#     for rule in apriori_rules:
#         antecedents = set(rule["antecedents"])
        
#         # If the rule's antecedents are explicitly a subset of the user's cart
#         if antecedents.issubset(input_set):
#             consequents = rule["consequents"]
            
#             for item in consequents:
#                 if item not in input_set:
#                     # Multi-Product Aggregation logic: Keep rule with highest confidence for each target item
#                     if item not in recommendations_map or recommendations_map[item]["confidence"] < rule["confidence"]:
                        
#                         # Generate Explanation String
#                         conf_pct = int(rule["confidence"] * 100)
#                         ante_str = ' and '.join(antecedents)
#                         explanation = f"Recommended because {conf_pct}% of users who bought {ante_str} also bought this."
                        
#                         recommendations_map[item] = {
#                             "item": item,
#                             "confidence": round(rule["confidence"], 2),
#                             "lift": round(rule["lift"], 2),
#                             "support": round(rule["support"], 2),
#                             "based_on": list(antecedents),
#                             "explanation": explanation,
#                             "is_trending": False
#                         }
                        
#     # --- SIMILARITY FALLBACK ---
#     # If not enough recommendations, find similar items based on name words overlap
#     if len(recommendations_map) < 6 and apriori_stats and "all_products" in apriori_stats:
#         all_prods = apriori_stats["all_products"]
        
#         # Extract meaningful tokens (words > 2 chars) from input products
#         input_tokens = set()
#         for prod in req.products:
#             for word in prod.lower().split():
#                 if len(word) > 2:
#                     input_tokens.add(word)
                    
#         if input_tokens:
#             similarity_scores = {}
#             for p in all_prods:
#                 p_name = p["name"]
#                 if p_name in input_set or p_name in recommendations_map:
#                     continue
                
#                 p_tokens = set(word for word in p_name.lower().split() if len(word) > 2)
#                 if not p_tokens:
#                     continue
                    
#                 intersection = input_tokens.intersection(p_tokens)
#                 if intersection:
#                     # Jaccard similarity
#                     similarity = len(intersection) / len(input_tokens.union(p_tokens))
#                     if similarity > 0.05: # At least some overlap
#                         similarity_scores[p_name] = similarity
            
#             # Sort by highest similarity score
#             sorted_similar = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
#             needed = 6 - len(recommendations_map)
            
#             for sim_item, score in sorted_similar[:needed]:
#                 recommendations_map[sim_item] = {
#                     "item": sim_item,
#                     "confidence": round(score, 2),
#                     "lift": 1.0,
#                     "support": 0.0,
#                     "based_on": list(req.products),
#                     "explanation": f"Recommended because it is similar to items in your cart (Similarity score: {int(score * 100)}%).",
#                     "is_trending": False
#                 }
                
#     # --- TRENDING FALLBACK ---
#     # If STILL not enough recommendations, fill remaining slots with trending items
#     if len(recommendations_map) < 6 and apriori_stats and "top_items" in apriori_stats:
#         needed = 6 - len(recommendations_map)
#         trending_added = 0
#         for item, count in list(apriori_stats["top_items"].items()):
#             if trending_added >= needed:
#                 break
#             if item not in input_set and item not in recommendations_map:
#                 recommendations_map[item] = {
#                     "item": item,
#                     "confidence": 1.0,
#                     "lift": 1.0,
#                     "support": 1.0,
#                     "based_on": [],
#                     "explanation": f"Trending Product! Purchased {int(count)} times recently.",
#                     "is_trending": True
#                 }
#                 trending_added += 1

#     # Convert map to list and rank recommendations by highest confidence, then lift
#     sorted_recs = sorted(list(recommendations_map.values()), key=lambda x: (x["confidence"], x["lift"]), reverse=True)
    
#     # is_fallback flag if no association rules were found at all
#     is_fallback = all(r.get("is_trending", False) or "Similarity score" in r.get("explanation", "") for r in sorted_recs)
    
#     return {"recommendations": sorted_recs[:6], "is_fallback": is_fallback}

# # 👇 ADD THIS HERE
# from mongo_connection import get_mongo_db

# @app.post("/track")
# def track_user(data: dict):
#     db = get_mongo_db()
#     db.user_activity.insert_one(data)
#     return {"message": "tracked"}

# @app.get("/activity")
# def get_activity():
#     db = get_mongo_db()
#     data = list(db.user_activity.find({}, {"_id": 0}))
#     return data

# @app.get("/analytics")
# async def get_analytics():
#     if not apriori_stats:
#         raise HTTPException(status_code=404, detail="Analytics data not found or not generated yet.")
#     return apriori_stats

# @app.get("/products")
# async def get_products():
#     if apriori_stats and "all_products" in apriori_stats:
#         # Expecting a list of {"id": "...", "name": "...", "normalized": "..."}
#         return apriori_stats["all_products"]
    
#     # Fallback to stats top items if all_products is missing for some reason
#     if apriori_stats and "top_items" in apriori_stats:
#         return [{"id": f"fallback_{k}", "name": k, "normalized": k} for k in apriori_stats["top_items"].keys()]
        
#     return []

# class RecalculateRequest(BaseModel):
#     min_support: float
#     min_confidence: float

# @app.post("/recalculate")
# async def recalculate_model(req: RecalculateRequest):
#     try:
#         # Note: If raw_transactions.csv is unavailable, we just reload rules instead of rebuilding them.
#         DATA_PATH = Path("raw_transactions.csv")
#         if DATA_PATH.exists():
#             calculate_rules(min_support=req.min_support, min_confidence=req.min_confidence)
        
#         # Reload global memory instances across API
#         load_rules()
#         return {"status": "success", "message": "Model updated and re-cached into API memory."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# ─────────────────────────────────────────────────────────────────────────────
# main.py — Apriori + Spark Recommendation Engine API
# ─────────────────────────────────────────────────────────────────────────────
import subprocess
import sys
import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from apriori_pipeline import calculate_rules
from mongo_connection import get_mongo_db

# ── 1. App defined FIRST (everything else depends on this) ────────────────────
app = FastAPI(title="Apriori + Spark Recommendation Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 2. File Paths ─────────────────────────────────────────────────────────────
RULES_CACHE_PATH = Path(__file__).parent / "rules_cache.json"
STATS_CACHE_PATH = Path(__file__).parent / "stats_cache.json"

SPARK_SCRIPT = Path(__file__).parent.parent / "bigdata" / "spark_jobs" / "recommend.py"
RECS_FILE    = Path(__file__).parent.parent / "bigdata" / "spark_jobs" / "output" / "recommendations.json"

# ── 3. In-memory storage ──────────────────────────────────────────────────────
apriori_rules = []
apriori_stats = {}

# ── 4. Startup ────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    load_rules()

def load_rules():
    global apriori_rules, apriori_stats
    try:
        if RULES_CACHE_PATH.exists():
            with open(RULES_CACHE_PATH, 'r') as f:
                apriori_rules = json.load(f)
            print(f"Loaded {len(apriori_rules)} rules into memory.")
        else:
            print("Warning: rules_cache.json not found.")

        if STATS_CACHE_PATH.exists():
            with open(STATS_CACHE_PATH, 'r') as f:
                apriori_stats = json.load(f)
            print("Loaded analytics stats into memory.")
    except Exception as e:
        print(f"Error loading cache: {e}")

# ── 5. Basic Routes ───────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "Backend running"}

# ── 6. Apriori Recommendation Routes ─────────────────────────────────────────
class RecommendRequest(BaseModel):
    products: List[str]

@app.post("/recommend")
async def get_recommendations(req: RecommendRequest):
    print(f"DEBUG: Received recommendation POST request: {req.products}")

    if not req.products:
        if not apriori_stats or "top_items" not in apriori_stats:
            return {"recommendations": [], "is_fallback": True}
        trending = []
        top_items = list(apriori_stats["top_items"].items())[:5]
        for item, count in top_items:
            trending.append({
                "item": item,
                "confidence": 1.0,
                "lift": 1.0,
                "support": 1.0,
                "based_on": [],
                "explanation": f"Trending Product! Purchased {int(count)} times recently.",
                "is_trending": True
            })
        return {"recommendations": trending, "is_fallback": True}

    input_set = set(req.products)
    recommendations_map = {}

    for rule in apriori_rules:
        antecedents = set(rule["antecedents"])
        if antecedents.issubset(input_set):
            consequents = rule["consequents"]
            for item in consequents:
                if item not in input_set:
                    if item not in recommendations_map or recommendations_map[item]["confidence"] < rule["confidence"]:
                        conf_pct = int(rule["confidence"] * 100)
                        ante_str = ' and '.join(antecedents)
                        explanation = f"Recommended because {conf_pct}% of users who bought {ante_str} also bought this."
                        recommendations_map[item] = {
                            "item": item,
                            "confidence": round(rule["confidence"], 2),
                            "lift": round(rule["lift"], 2),
                            "support": round(rule["support"], 2),
                            "based_on": list(antecedents),
                            "explanation": explanation,
                            "is_trending": False
                        }

    if len(recommendations_map) < 6 and apriori_stats and "all_products" in apriori_stats:
        all_prods = apriori_stats["all_products"]
        input_tokens = set()
        for prod in req.products:
            for word in prod.lower().split():
                if len(word) > 2:
                    input_tokens.add(word)
        if input_tokens:
            similarity_scores = {}
            for p in all_prods:
                p_name = p["name"]
                if p_name in input_set or p_name in recommendations_map:
                    continue
                p_tokens = set(word for word in p_name.lower().split() if len(word) > 2)
                if not p_tokens:
                    continue
                intersection = input_tokens.intersection(p_tokens)
                if intersection:
                    similarity = len(intersection) / len(input_tokens.union(p_tokens))
                    if similarity > 0.05:
                        similarity_scores[p_name] = similarity
            sorted_similar = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
            needed = 6 - len(recommendations_map)
            for sim_item, score in sorted_similar[:needed]:
                recommendations_map[sim_item] = {
                    "item": sim_item,
                    "confidence": round(score, 2),
                    "lift": 1.0,
                    "support": 0.0,
                    "based_on": list(req.products),
                    "explanation": f"Recommended because it is similar to items in your cart (Similarity score: {int(score * 100)}%).",
                    "is_trending": False
                }

    if len(recommendations_map) < 6 and apriori_stats and "top_items" in apriori_stats:
        needed = 6 - len(recommendations_map)
        trending_added = 0
        for item, count in list(apriori_stats["top_items"].items()):
            if trending_added >= needed:
                break
            if item not in input_set and item not in recommendations_map:
                recommendations_map[item] = {
                    "item": item,
                    "confidence": 1.0,
                    "lift": 1.0,
                    "support": 1.0,
                    "based_on": [],
                    "explanation": f"Trending Product! Purchased {int(count)} times recently.",
                    "is_trending": True
                }
                trending_added += 1

    sorted_recs = sorted(list(recommendations_map.values()), key=lambda x: (x["confidence"], x["lift"]), reverse=True)
    is_fallback = all(r.get("is_trending", False) or "Similarity score" in r.get("explanation", "") for r in sorted_recs)
    return {"recommendations": sorted_recs[:6], "is_fallback": is_fallback}

# ── 7. MongoDB Tracking Routes ────────────────────────────────────────────────
@app.post("/track")
def track_user(data: dict):
    db = get_mongo_db()
    db.user_activity.insert_one(data)
    return {"message": "tracked"}

@app.get("/activity")
def get_activity():
    db = get_mongo_db()
    data = list(db.user_activity.find({}, {"_id": 0}))
    return data

# ── 8. Analytics & Products Routes ───────────────────────────────────────────
@app.get("/analytics")
async def get_analytics():
    if not apriori_stats:
        raise HTTPException(status_code=404, detail="Analytics data not found or not generated yet.")
    return apriori_stats

@app.get("/products")
async def get_products():
    if apriori_stats and "all_products" in apriori_stats:
        return apriori_stats["all_products"]
    if apriori_stats and "top_items" in apriori_stats:
        return [{"id": f"fallback_{k}", "name": k, "normalized": k} for k in apriori_stats["top_items"].keys()]
    return []

class RecalculateRequest(BaseModel):
    min_support: float
    min_confidence: float

@app.post("/recalculate")
async def recalculate_model(req: RecalculateRequest):
    try:
        DATA_PATH = Path("raw_transactions.csv")
        if DATA_PATH.exists():
            calculate_rules(min_support=req.min_support, min_confidence=req.min_confidence)
        load_rules()
        return {"status": "success", "message": "Model updated and re-cached into API memory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── 9. Spark Routes (PySpark local mode — no Docker) ─────────────────────────
@app.post("/api/spark/run")
def run_spark_job():
    """Triggers the PySpark ALS recommendation job locally"""
    if not SPARK_SCRIPT.exists():
        raise HTTPException(status_code=404, detail=f"Spark script not found at {SPARK_SCRIPT}")
    try:
        result = subprocess.run(
            [sys.executable, str(SPARK_SCRIPT)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return {"status": "success", "message": "Spark job completed!", "log": result.stdout[-1000:]}
        else:
            return {"status": "error", "log": result.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Spark job timed out after 120s")
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/spark/recommendations/{user_id}")
def get_spark_recommendations(user_id: int):
    """Returns Spark ALS-generated top-5 recommendations for a user"""
    if not RECS_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="No Spark output found. Run POST /api/spark/run first."
        )
    with open(RECS_FILE) as f:
        data = json.load(f)
    user_recs = next((r for r in data["recommendations"] if r["user_id"] == user_id), None)
    if not user_recs:
        raise HTTPException(status_code=404, detail=f"No recommendations found for user {user_id}")
    return {"status": "success", "user_id": user_id, "rmse": data["rmse"], "data": user_recs}

@app.get("/api/spark/status")
def spark_status():
    """Check if PySpark output file exists"""
    return {
        "spark_script_exists": SPARK_SCRIPT.exists(),
        "spark_output_exists": RECS_FILE.exists(),
        "engine": "PySpark 3.4.1 (local[*] mode)",
        "model": "ALS Collaborative Filtering (MLlib)",
        "output_path": str(RECS_FILE)
    }

# ── 10. Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)