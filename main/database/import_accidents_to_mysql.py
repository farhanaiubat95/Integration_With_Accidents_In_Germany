import pandas as pd
from db_connection_common import get_connection

connection = get_connection()
cursor = connection.cursor()

# -------------------------
# Population lookup
# -------------------------

cursor.execute("""
SELECT population_id, ags
FROM population
""")

population_lookup = {}

for population_id, ags in cursor.fetchall():
    population_lookup[str(ags)] = population_id

print("Population loaded:", len(population_lookup))

# -------------------------
# Accident files
# -------------------------

files = [
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte_2016_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2017_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2018_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2019_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2020_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2021_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2022_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2023_LinRef.csv",
    r"G:\Integration_With_Accidents_In_Germany\dataset folder\Unfallorte CSV File\Unfallorte2024_LinRef.csv"
]

all_data = []

for file in files:

    print("Reading:", file)

    df = pd.read_csv(file)

    df.rename(columns={
        "IstSonstig": "IstSonstige",
        "LICHT": "ULICHTVERH",
        "STRZUSTAND": "IstStrassenzustand",
        "IstStrasse": "IstStrassenzustand"
    }, inplace=True)

    all_data.append(df)

merged_df = pd.concat(all_data, ignore_index=True)

merged_df = merged_df.fillna(0)

# -------------------------
# Create AGS
# -------------------------

merged_df["ags"] = (
    merged_df["ULAND"].astype(int).astype(str)
    + merged_df["UREGBEZ"].astype(int).astype(str)
    + merged_df["UKREIS"].astype(int).astype(str).str.zfill(2)
    + merged_df["UGEMEINDE"].astype(int).astype(str).str.zfill(3)
)

# -------------------------
# Population Matching
# -------------------------

population_ids = []

for ags in merged_df["ags"]:

    ags = str(ags)

    population_id = 0

    if ags in population_lookup:

        population_id = population_lookup[ags]

    elif ags[:5] in population_lookup:

        population_id = population_lookup[ags[:5]]

    elif ags[:4] in population_lookup:

        population_id = population_lookup[ags[:4]]

    elif ags[:1] in population_lookup:

        population_id = population_lookup[ags[:1]]

    population_ids.append(population_id)

merged_df["population_id"] = population_ids

print("Population mapping completed.")

# -------------------------
# Insert
# -------------------------

sql = """
INSERT INTO accidents
(
ULAND,
UREGBEZ,
UKREIS,
UGEMEINDE,
ags,
population_id,
UJAHR,
UMONAT,
USTUNDE,
UWOCHENTAG,
UKATEGORIE,
UART,
UTYP1,
ULICHTVERH,
IstStrassenzustand,
IstRad,
IstPKW,
IstFuss,
IstKrad,
IstGkfz,
IstSonstige
)
VALUES
(
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s
)
"""

records = merged_df[
[
"ULAND",
"UREGBEZ",
"UKREIS",
"UGEMEINDE",
"ags",
"population_id",
"UJAHR",
"UMONAT",
"USTUNDE",
"UWOCHENTAG",
"UKATEGORIE",
"UART",
"UTYP1",
"ULICHTVERH",
"IstStrassenzustand",
"IstRad",
"IstPKW",
"IstFuss",
"IstKrad",
"IstGkfz",
"IstSonstige"
]
].values.tolist()

batch_size = 5000

for i in range(0, len(records), batch_size):

    batch = records[i:i+batch_size]

    cursor.executemany(sql, batch)

    connection.commit()

    print(
        f"Inserted {min(i+batch_size, len(records))} / {len(records)}"
    )

print("Import completed.")

cursor.close()
connection.close()