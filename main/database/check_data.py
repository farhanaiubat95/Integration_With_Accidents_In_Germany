import pandas as pd
from db_connection_common import get_connection

conn = get_connection()

# =====================================
# 1. Population -> Region Coverage
# =====================================

print("\n==============================")
print("POPULATION -> REGION COVERAGE")
print("==============================")

population_region = pd.read_sql("""
SELECT
    COUNT(*) AS total_rows,
    SUM(region_id <> 0) AS matched_rows,
    SUM(region_id = 0) AS unmatched_rows
FROM population
""", conn)

print(population_region)

# =====================================
# 2. Accident -> Population Coverage
# =====================================

print("\n==============================")
print("ACCIDENT -> POPULATION COVERAGE")
print("==============================")

accident_population = pd.read_sql("""
SELECT
    COUNT(*) AS total_rows,
    SUM(population_id <> 0) AS matched_rows,
    SUM(population_id = 0) AS unmatched_rows
FROM accidents
""", conn)

print(accident_population)

# =====================================
# 3. Join Chain Sample
# =====================================

print("\n==============================")
print("JOIN SAMPLE")
print("==============================")

join_sample = pd.read_sql("""
SELECT

    a.accident_id,
    a.ags AS accident_ags,

    a.population_id,

    p.name AS population_name,
    p.ags AS population_ags,

    p.region_id,

    r.name AS region_name,
    r.level AS region_level

FROM accidents a

LEFT JOIN population p
    ON a.population_id = p.population_id

LEFT JOIN regions r
    ON p.region_id = r.region_id

LIMIT 30
""", conn)

print(join_sample)

# =====================================
# 4. Missing Population Links
# =====================================

print("\n==============================")
print("ACCIDENTS WITHOUT POPULATION")
print("==============================")

missing_population = pd.read_sql("""
SELECT
    accident_id,
    ags,
    population_id
FROM accidents
WHERE population_id = 0
LIMIT 30
""", conn)

print(missing_population)

# =====================================
# 5. Missing Region Links
# =====================================

print("\n==============================")
print("POPULATION WITHOUT REGION")
print("==============================")

missing_region = pd.read_sql("""
SELECT
    population_id,
    ags,
    name
FROM population
WHERE region_id = 0
LIMIT 30
""", conn)

print(missing_region)

conn.close()