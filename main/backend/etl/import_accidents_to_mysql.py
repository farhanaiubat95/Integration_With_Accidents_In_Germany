import pandas as pd
from db_connection_common import get_connection

connection = get_connection()
cursor = connection.cursor()


# Population lookup
cursor.execute("""
SELECT region_id, ags
FROM regions
""")

region_lookup = {}

for region_id, ags in cursor.fetchall():
    region_lookup[str(ags)] = region_id

print("Region loaded:", len(region_lookup))


# Accident files
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


# Create AGS
merged_df["ags"] = (
    merged_df["ULAND"].astype(int).astype(str)
    + merged_df["UREGBEZ"].astype(int).astype(str)
    + merged_df["UKREIS"].astype(int).astype(str).str.zfill(2)
    + merged_df["UGEMEINDE"].astype(int).astype(str).str.zfill(3)
)


# Region Matching
region_ids = []

for ags in merged_df["ags"]:

    ags = str(ags)

    region_id = 0

    if ags in region_lookup:

        region_id = region_lookup[ags]

    elif ags[:5] in region_lookup:

        region_id = region_lookup[ags[:5]]

    elif ags[:4] in region_lookup:

        region_id = region_lookup[ags[:4]]

    elif ags[:1] in region_lookup:

        region_id = region_lookup[ags[:1]]

    region_ids.append(region_id)

merged_df["region_id"] = region_ids

print("Region mapping completed.")


# Insert
sql = """
INSERT INTO accidents
(
ULAND,
UREGBEZ,
UKREIS,
UGEMEINDE,
ags,
region_id,
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
"region_id",
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


# SAVE IMPORT LOG
cursor.execute("""
SELECT source_id
FROM sources
WHERE source_name = %s
""", ("Unfallatlas",))

source_id = cursor.fetchone()[0]

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
    "accidents",
    len(records),
    "SUCCESS"
))

connection.commit()

print("Import log saved.")

cursor.close()
connection.close()