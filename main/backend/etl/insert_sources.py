from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

sources = [
    (
        "Unfallatlas",
        "-",
        "dl-de/by-2-0",
        "https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/"
    ),
    (
        "Regionalatlas",
        "-",
        "dl-de/by-2-0",
        "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/"
    ),
    (
        "Population Dataset",
        "-",
        "dl-de/by-2-0",
        "https://www.regionalstatistik.de/genesis/online?operation=table&code=12411-01-01-4"
    )
]

for source_name, provider, license_name, source_url in sources:

    # Check if already exists
    cursor.execute("""
        SELECT source_id
        FROM sources
        WHERE source_name = %s
           OR source_url = %s
    """, (source_name, source_url))

    exists = cursor.fetchone()

    if exists:
        print(f"Skipped: {source_name} already exists.")
    else:
        cursor.execute("""
            INSERT INTO sources
            (source_name, provider, license, source_url)
            VALUES (%s, %s, %s, %s)
        """, (source_name, provider, license_name, source_url))

        print(f"Inserted: {source_name}")

conn.commit()

cursor.close()
conn.close()

print("Done.")