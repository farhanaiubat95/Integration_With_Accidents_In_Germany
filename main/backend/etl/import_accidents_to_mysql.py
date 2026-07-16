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

# Read files
print("=" * 60)
print("First 1 : Reading Accident Files")
print("=" * 60)


all_data = []

for file in files:
    print(f"\nReading -> {file}")
    df = pd.read_csv(file)
    print(f"Rows Loaded : {len(df):,}")

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

print("\n")
print("=" * 60)
print("Second 2 : Mapping Regions")
print("=" * 60)

...

print(f"Region Mapping Finished")

matched = (merged_df["region_id"] != 0).sum()

unmatched = (merged_df["region_id"] == 0).sum()

print(f"Matched : {matched:,}")
print(f"Unmatched : {unmatched:,}")

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

SELECT
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s

FROM DUAL

WHERE NOT EXISTS (

SELECT 1
FROM accidents

WHERE
UJAHR=%s
AND ULAND=%s
AND UREGBEZ=%s
AND UKREIS=%s
AND UGEMEINDE=%s
AND UMONAT=%s
AND USTUNDE=%s
AND UWOCHENTAG=%s
AND UKATEGORIE=%s
AND UART=%s
AND UTYP1=%s

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

records = []

for _, row in merged_df.iterrows():

    records.append([

        row["ULAND"],
        row["UREGBEZ"],
        row["UKREIS"],
        row["UGEMEINDE"],
        row["ags"],
        row["region_id"],
        row["UJAHR"],
        row["UMONAT"],
        row["USTUNDE"],
        row["UWOCHENTAG"],
        row["UKATEGORIE"],
        row["UART"],
        row["UTYP1"],
        row["ULICHTVERH"],
        row["IstStrassenzustand"],
        row["IstRad"],
        row["IstPKW"],
        row["IstFuss"],
        row["IstKrad"],
        row["IstGkfz"],
        row["IstSonstige"],

        # Duplicate check fields
        row["UJAHR"],
        row["ULAND"],
        row["UREGBEZ"],
        row["UKREIS"],
        row["UGEMEINDE"],
        row["UMONAT"],
        row["USTUNDE"],
        row["UWOCHENTAG"],
        row["UKATEGORIE"],
        row["UART"],
        row["UTYP1"]

    ])

batch_size = 5000

inserted = 0
current_year = None
status = "SUCCESS"

# error handling for the import process
try:

    for i in range(0, len(records), batch_size):
        if current_year != row[6]:      # row[6] = UJAHR

            current_year = row[6]

            print(f"\nChecking Year : {current_year}")

        batch = records[i:i + batch_size]

        cursor.executemany(sql, batch)

        connection.commit()

        inserted += cursor.rowcount

        print(f"Inserted {min(i+batch_size, len(records))} / {len(records)}")

    print("Accident import completed.")

except Exception as e:

    connection.rollback()

    status = "FAILED"

    print("Import Failed")
    print(e)


# SAVE IMPORT LOG
cursor.execute("""
SELECT source_id
FROM sources
WHERE source_name = %s
""", ("Unfallatlas",))

source = cursor.fetchone()

if source:

    source_id = source[0]

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
        inserted,
        status
    ))

    connection.commit()

    print("Import log saved.")

cursor.close()
connection.close()

print("Finished.")