import pandas as pd
from db_connection_common import get_connection

# ==========================
# READ CSV
# ==========================

df = pd.read_csv(
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\AGS Region\kreise_area .csv",
    encoding="latin1"
)

# ==========================
# MYSQL CONNECTION
# ==========================

connection = get_connection()
cursor = connection.cursor()

insert_sql = """
INSERT INTO regions (
    ags,
    name,
    level,
    region_type,
    nuts3,
    area_km2
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

insert_data = []

# ==========================
# PROCESS ROWS
# ==========================

for _, row in df.iterrows():

    # --------------------------
    # AGS
    # --------------------------

    ags = row["Amtlicher Regionalschlüssel"]

    if pd.isna(ags):
        continue

    ags = str(int(float(ags)))

    # --------------------------
    # NAME + REGION TYPE
    # --------------------------

    csv_name = row["Kreisfreie Städte und Landkreise"]
    csv_region_type = row["Regionale Bezeichnung"]

    csv_name = "" if pd.isna(csv_name) else str(csv_name).strip()
    csv_region_type = "" if pd.isna(csv_region_type) else str(csv_region_type).strip()

    # State rows
    if len(ags) == 1:

        name = csv_region_type
        region_type = "State"

    # Region rows
    elif len(ags) == 2:

        name = csv_region_type
        region_type = "Region"

    # District / Municipality rows
    else:

        name = csv_name
        region_type = csv_region_type

    # --------------------------
    # LEVEL
    # --------------------------

    if len(ags) == 1:
        level = "state"

    elif len(ags) == 2:
        level = "region"

    elif len(ags) in [4, 5]:
        level = "district"

    elif len(ags) in [7, 8]:
        level = "municipality"

    else:
        level = "unknown"

    # --------------------------
    # NUTS3
    # --------------------------

    nuts3 = row["NUTS3"]

    if pd.isna(nuts3):
        nuts3 = None
    else:
        nuts3 = str(nuts3).strip()

    # --------------------------
    # AREA
    # --------------------------

    area = row[" Fläche km² ¹?"]

    if pd.isna(area):

        area_km2 = 0

    else:

        area = str(area).strip()

        # FIX FOR VALUES LIKE:
        # 1 428,17
        # 2 083,56

        area = area.replace(" ", "")
        area = area.replace(".", "")
        area = area.replace(",", ".")

        try:
            area_km2 = float(area)
        except:
            area_km2 = 0

    # --------------------------
    # SAVE
    # --------------------------

    insert_data.append(
        (
            ags,
            name,
            level,
            region_type,
            nuts3,
            area_km2
        )
    )

# ==========================
# INSERT INTO MYSQL
# ==========================

cursor.executemany(insert_sql, insert_data)

connection.commit()

print("Region import completed.")
print("Rows inserted:", len(insert_data))

cursor.close()
connection.close()