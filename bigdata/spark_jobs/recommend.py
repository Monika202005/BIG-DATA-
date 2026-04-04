# """
# recommend.py — Spark MLlib Recommendation Engine
# Reads order data from MySQL → trains ALS model → writes results to HDFS
# Run this inside the spark-master container (see Step 6)
# """

# from pyspark.sql import SparkSession
# from pyspark.ml.recommendation import ALS
# from pyspark.ml.evaluation import RegressionEvaluator
# from pyspark.sql.functions import col, count, lit
# import sys

# # ── 1. Create Spark Session (connects to HDFS too) ──────────────────────────
# spark = SparkSession.builder \
#     .appName("EcommerceRecommender") \
#     .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
#     .getOrCreate()

# spark.sparkContext.setLogLevel("WARN")
# print("Spark Session started")

# # ── 2. Read Data from MySQL ──────────────────────────────────────────────────
# # Replace with your actual MySQL container name / host if different
# MYSQL_URL = "jdbc:mysql://host.docker.internal:3306/ecommerce_oltp"
# MYSQL_PROPS = {
#     "user": "ecommerce_user",
#     "password": "Ecommerce_pass123!",
#     "driver": "com.mysql.cj.jdbc.Driver"
# }

# # Read the orders table (adjust table name to match yours)
# try:
#     orders_df = spark.read.jdbc(
#         url=MYSQL_URL,
#         table="order_items",   # ← change to your actual table name
#         properties=MYSQL_PROPS
#     )
#     print(f" Loaded {orders_df.count()} order records from MySQL")
#     orders_df.printSchema()
# except Exception as e:
#     print(f" MySQL read failed: {e}")
#     print(" Using synthetic sample data instead...")

#     # Fallback: synthetic data so Spark still runs even if MySQL isn't reachable
#     from pyspark.sql import Row
#     sample_data = [
#         Row(user_id=1, product_id=101, quantity=2),
#         Row(user_id=1, product_id=102, quantity=1),
#         Row(user_id=2, product_id=101, quantity=3),
#         Row(user_id=2, product_id=103, quantity=1),
#         Row(user_id=3, product_id=102, quantity=2),
#         Row(user_id=3, product_id=103, quantity=4),
#         Row(user_id=4, product_id=101, quantity=1),
#         Row(user_id=4, product_id=104, quantity=2),
#         Row(user_id=5, product_id=102, quantity=1),
#         Row(user_id=5, product_id=104, quantity=3),
#     ]
#     orders_df = spark.createDataFrame(sample_data)

# # ── 3. Prepare Data for ALS ──────────────────────────────────────────────────
# # ALS needs: user_id (int), product_id (int), rating (float)
# # We use quantity as implicit rating
# ratings_df = orders_df.select(
#     col("user_id").cast("int"),
#     col("product_id").cast("int"),
#     col("quantity").cast("float").alias("rating")
# ).dropna()

# print(f" Prepared {ratings_df.count()} rating records for ALS")

# # Split into train / test
# train_df, test_df = ratings_df.randomSplit([0.8, 0.2], seed=42)

# # ── 4. Train ALS Model (Collaborative Filtering) ────────────────────────────
# als = ALS(
#     maxIter=10,
#     regParam=0.1,
#     rank=10,
#     userCol="user_id",
#     itemCol="product_id",
#     ratingCol="rating",
#     coldStartStrategy="drop"   # handles users/products not in training
# )

# model = als.fit(train_df)
# print(" ALS model trained!")

# # ── 5. Evaluate the Model ────────────────────────────────────────────────────
# predictions = model.transform(test_df)
# evaluator = RegressionEvaluator(
#     metricName="rmse",
#     labelCol="rating",
#     predictionCol="prediction"
# )
# rmse = evaluator.evaluate(predictions)
# print(f" Model RMSE (lower = better): {rmse:.4f}")

# # ── 6. Generate Top-5 Recommendations for Every User ────────────────────────
# user_recs = model.recommendForAllUsers(5)
# print(" Generated recommendations for all users")
# user_recs.show(10, truncate=False)

# # ── 7. Save Results to HDFS ─────────────────────────────────────────────────
# OUTPUT_PATH = "hdfs://namenode:9000/ecommerce/recommendations"

# user_recs.write \
#     .mode("overwrite") \
#     .parquet(OUTPUT_PATH)

# print(f"Recommendations saved to HDFS at: {OUTPUT_PATH}")

# # Also save model metrics
# metrics_df = spark.createDataFrame([{"rmse": rmse, "model": "ALS", "status": "trained"}])
# metrics_df.write.mode("overwrite").json("hdfs://namenode:9000/ecommerce/metrics")

# print("All done! Check Hadoop UI at http://localhost:9870")
# spark.stop()
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
import json
import os

# ── Spark Session ──────────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("EcommerceRecommender") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark Session started")

# ── Sample Data ────────────────────────────────────────────────────────────────
ratings_data = [
    (1, 101, 5.0), (1, 102, 3.0), (1, 103, 4.0),
    (2, 101, 4.0), (2, 104, 5.0), (2, 105, 3.0),
    (3, 102, 5.0), (3, 103, 4.0), (3, 106, 3.0),
    (4, 101, 3.0), (4, 105, 4.0), (4, 107, 5.0),
    (5, 103, 5.0), (5, 106, 4.0), (5, 108, 3.0),
    (6, 102, 4.0), (6, 104, 3.0), (6, 109, 5.0),
    (7, 101, 5.0), (7, 107, 4.0), (7, 110, 3.0),
    (8, 105, 5.0), (8, 108, 4.0), (8, 110, 3.0),
]

product_names = {
    101: "Laptop", 102: "Phone", 103: "Headphones",
    104: "Tablet", 105: "Smartwatch", 106: "Camera",
    107: "Keyboard", 108: "Mouse", 109: "Monitor", 110: "Speaker"
}

# ── Create Spark DataFrame ─────────────────────────────────────────────────────
columns = ["user_id", "product_id", "rating"]
df = spark.createDataFrame(ratings_data, columns)
print(f"✅ DataFrame created with {df.count()} records")

# ── Train/Test Split ───────────────────────────────────────────────────────────
train, test = df.randomSplit([0.8, 0.2], seed=42)

# ── ALS Model ─────────────────────────────────────────────────────────────────
als = ALS(
    maxIter=10,
    regParam=0.1,
    rank=10,
    userCol="user_id",
    itemCol="product_id",
    ratingCol="rating",
    coldStartStrategy="drop"
)

model = als.fit(train)
print("✅ ALS Model trained")

# ── Evaluate ───────────────────────────────────────────────────────────────────
predictions = model.transform(test)
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)
rmse = evaluator.evaluate(predictions)
print(f"✅ RMSE: {rmse:.4f}")

# ── Generate Recommendations ───────────────────────────────────────────────────
user_recs = model.recommendForAllUsers(5)

recs_list = []
for row in user_recs.collect():
    user_id = row["user_id"]
    recs = []
    for rec in row["recommendations"]:
        pid = rec["product_id"]
        recs.append({
            "product_id": pid,
            "product_name": product_names.get(pid, f"Product {pid}"),
            "predicted_rating": round(float(rec["rating"]), 2)
        })
    recs_list.append({"user_id": user_id, "recommendations": recs})

# ── Save Output ────────────────────────────────────────────────────────────────
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "recommendations.json")

with open(output_path, "w") as f:
    json.dump({"rmse": round(rmse, 4), "recommendations": recs_list}, f, indent=2)

print(f"✅ Recommendations saved to {output_path}")
spark.stop()
print("✅ Spark Session stopped")