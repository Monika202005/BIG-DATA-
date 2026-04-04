import json
import re
from pathlib import Path

RULES_PATH = Path("rules_cache.json")
STATS_PATH = Path("stats_cache.json")

def normalize_name(text):
    t = text.lower().strip()
    t = re.sub(r'[^a-z0-9\s]', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t

if not RULES_PATH.exists() or not STATS_PATH.exists():
    print("Missing cache files.")
    exit(1)

with open(RULES_PATH, 'r') as f:
    rules = json.load(f)

with open(STATS_PATH, 'r') as f:
    stats = json.load(f)

# Extract all unique original names from stats and rules
original_names = set()
if "all_products" in stats:
    if len(stats["all_products"]) > 0 and isinstance(stats["all_products"][0], str):
        original_names.update(stats["all_products"])
    
for rule in rules:
    original_names.update(rule["antecedents"])
    original_names.update(rule["consequents"])

# Build all_products dict array
all_products_map = []
normalized_mapping = {}

for idx, name in enumerate(sorted(original_names)):
    norm = normalize_name(name)
    normalized_mapping[name] = norm
    all_products_map.append({
        "id": f"p_{idx+1}",
        "name": name,
        "normalized": norm
    })

stats["all_products"] = all_products_map

# Rewrite rules using normalized names
for rule in rules:
    rule["antecedents"] = [normalized_mapping[item] for item in rule["antecedents"]]
    rule["consequents"] = [normalized_mapping[item] for item in rule["consequents"]]

# Rewrite top_rules in stats
if "top_rules" in stats:
    for tr in stats["top_rules"]:
        # Naive split for stats display update if needed, but not strictly needed for matching
        # However, let's keep original format or normalized format? 
        # The frontend doesn't use top_rules string for matching, so it's fine.
        pass

with open(STATS_PATH, 'w') as f:
    json.dump(stats, f, indent=4)

with open(RULES_PATH, 'w') as f:
    json.dump(rules, f, indent=4)

print(f"Patched cache files with {len(all_products_map)} products.")
