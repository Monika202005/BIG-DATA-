"""
apriori_pipeline.py  —  Backend version
Pulls rules & stats directly from ecommerce_dw (MySQL).
No CSV file needed — data already lives in the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path

# ── Try to import db_connection from the etl folder ──────────
# Adjust this path if your db_connection.py lives elsewhere
sys.path.append(str(Path(__file__).parent.parent / "etl"))
sys.path.append(str(Path(__file__).parent.parent))

from db_connection import get_dw_connection, get_oltp_connection

RULES_CACHE_PATH = Path(__file__).parent / "rules_cache.json"
STATS_CACHE_PATH = Path(__file__).parent / "stats_cache.json"


# ─────────────────────────────────────────────────────────────
# MAIN: Pull everything from MySQL and write JSON cache files
# Called by main.py on /recalculate, and can be run standalone
# ─────────────────────────────────────────────────────────────

def calculate_rules(min_support=0.02, min_confidence=0.6):
    print(f"📡 Pulling rules from ecommerce_dw (support≥{min_support}, conf≥{min_confidence})...")

    # ── 1. Pull association rules from fact_product_affinity ──
    conn_dw = get_dw_connection()
    if not conn_dw:
        print("❌ Cannot connect to ecommerce_dw")
        return

    cursor = conn_dw.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p1.description  AS antecedent,
            p2.description  AS consequent,
            a.support,
            a.confidence,
            a.lift
        FROM fact_product_affinity a
        JOIN dim_product p1 ON a.product_key_a = p1.product_key
        JOIN dim_product p2 ON a.product_key_b = p2.product_key
        WHERE a.support    >= %s
          AND a.confidence >= %s
        ORDER BY a.lift DESC
    """, (min_support, min_confidence))

    rows = cursor.fetchall()
    print(f"✅ Found {len(rows)} rules in fact_product_affinity")

    # Format for main.py  (antecedents / consequents are lists)
    formatted_rules = []
    for r in rows:
        formatted_rules.append({
            "antecedents": [r["antecedent"]],
            "consequents": [r["consequent"]],
            "support":     round(float(r["support"]),     4),
            "confidence":  round(float(r["confidence"]),  4),
            "lift":        round(float(r["lift"]),         4),
        })

    with open(RULES_CACHE_PATH, "w") as f:
        json.dump(formatted_rules, f, indent=2)
    print(f"💾 Saved {len(formatted_rules)} rules → rules_cache.json")

    # ── 2. Top products by total quantity sold ────────────────
    cursor.execute("""
        SELECT p.description, SUM(f.quantity) AS total_qty
        FROM fact_sales f
        JOIN dim_product p ON f.product_key = p.product_key
        GROUP BY p.description
        ORDER BY total_qty DESC
        LIMIT 10
    """)
    top_items = {r["description"]: int(r["total_qty"]) for r in cursor.fetchall()}

    # ── 3. Country distribution ───────────────────────────────
    cursor.execute("""
        SELECT cu.country, COUNT(DISTINCT f.invoice_no) AS invoice_count
        FROM fact_sales f
        JOIN dim_customer cu ON f.customer_key = cu.customer_key
        GROUP BY cu.country
        ORDER BY invoice_count DESC
        LIMIT 10
    """)
    country_distribution = {r["country"]: int(r["invoice_count"]) for r in cursor.fetchall()}

    # ── 4. Summary numbers ────────────────────────────────────
    cursor.execute("SELECT COUNT(DISTINCT invoice_no) AS cnt FROM fact_sales")
    total_transactions = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM dim_product")
    unique_products = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM fact_product_affinity")
    total_rules = cursor.fetchone()["cnt"]

    # Avg basket size = avg products per invoice
    cursor.execute("""
        SELECT AVG(item_count) AS avg_size FROM (
            SELECT invoice_no, COUNT(*) AS item_count
            FROM fact_sales
            GROUP BY invoice_no
        ) t
    """)
    avg_basket = cursor.fetchone()["avg_size"] or 0

    # ── 5. All products list (for search dropdown) ────────────
    cursor.execute("""
        SELECT product_key, description
        FROM dim_product
        ORDER BY description
    """)
    all_products = [
        {"id": f"p_{r['product_key']}", "name": r["description"], "normalized": r["description"].lower()}
        for r in cursor.fetchall()
    ]

    # ── 6. Top rules for display ──────────────────────────────
    top_rules_formatted = []
    for r in formatted_rules[:10]:
        top_rules_formatted.append({
            "rule": f"{r['antecedents'][0]} → {r['consequents'][0]}",
            "lift": r["lift"],
            "confidence": r["confidence"]
        })

    cursor.close()
    conn_dw.close()

    # ── 7. Write stats_cache.json ─────────────────────────────
    stats = {
        "total_transactions":   int(total_transactions),
        "unique_products":      int(unique_products),
        "total_rules":          int(total_rules),
        "avg_basket_size":      round(float(avg_basket), 2),
        "top_items":            top_items,
        "country_distribution": country_distribution,
        "top_rules":            top_rules_formatted,
        "all_products":         all_products,
    }

    with open(STATS_CACHE_PATH, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"💾 Stats saved → stats_cache.json")
    print("✅ Pipeline complete.")


if __name__ == "__main__":
    calculate_rules()
