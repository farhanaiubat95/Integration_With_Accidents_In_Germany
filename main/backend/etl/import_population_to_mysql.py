import pandas as pd
from db_connection_common import get_connection

# READ CSV
df = pd.read_csv(
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Population dataset\population_districts.csv",
    encoding="latin1"
)


# MYSQL CONNECTION
conn = get_connection()
cursor = conn.cursor()


# DELETE OLD DATA
cursor.execute("TRUNCATE TABLE population")
conn.commit()

print("Old population data deleted.")


# LOAD REGIONS
cursor.execute("""
SELECT region_id, ags
FROM regions
""")

region_lookup = {}

for region_id, ags in cursor.fetchall():
    region_lookup[str(ags)] = region_id

print("Region lookup loaded:", len(region_lookup))


# INSERT
insert_sql = """
INSERT INTO population
(
    ags,
    name,
    level,
    population,
    population_year,
    region_id
)
VALUES
(
    %s,%s,%s,%s,%s,%s
)
"""

insert_data = []

for _, row in df.iterrows():

    ags = str(row["DG"]).strip()
    name = str(row["Deutschland"]).strip()

    ags_len = len(ags)

    # LEVEL

    if ags_len == 1:
        level = "state"

    elif ags_len == 2:
        level = "region"

    elif ags_len in [4, 5]:
        level = "district"

    elif ags_len in [7, 8]:
        level = "municipality"

    else:
        level = "unknown"

    # POPULATION
    population_value = str(row["Insgesamt"]).strip()

    if population_value == "-":
        population = 0
    else:
        population = int(
            population_value.replace(".", "")
        )


    # REGION ID
    region_id = region_lookup.get(
        ags,
        0
    )

    insert_data.append(
        (
            ags,
            name,
            level,
            population,
            2024,
            region_id
        )
    )

cursor.executemany(
    insert_sql,
    insert_data
)

conn.commit()

print("Population import completed.")
print("Rows inserted:", len(insert_data))


# CHECK MATCHES
cursor.execute("""
SELECT COUNT(*)
FROM population
WHERE region_id > 0
""")

matched = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM population
WHERE region_id = 0
""")

unmatched = cursor.fetchone()[0]

print("Matched region_id :", matched)
print("Unmatched region_id :", unmatched)


# SAVE IMPORT LOG
cursor.execute("""
SELECT source_id
FROM sources
WHERE source_name = %s
""", ("Population Dataset",))

source_row = cursor.fetchone()

if source_row:

    source_id = source_row[0]

    cursor.execute("""
    INSERT INTO import_runs
    (
        source_id,
        table_name,
        records_imported,
        status
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    """,
    (
        source_id,
        "population",
        len(insert_data),
        "SUCCESS"
    ))

    conn.commit()

    print("Import log saved.")

cursor.close()
conn.close()