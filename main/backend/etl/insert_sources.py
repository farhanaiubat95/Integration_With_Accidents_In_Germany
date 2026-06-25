from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO sources
(source_name, provider, license, source_url)
VALUES
(
'Unfallatlas',
'-',
'dl-de/by-2-0',
'https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/'
)
""")

cursor.execute("""
INSERT INTO sources
(source_name, provider, license, source_url)
VALUES
(
'Regionalatlas',
'-',
'dl-de/by-2-0',
'https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/'
)
""")

cursor.execute("""
INSERT INTO sources
(source_name, provider, license, source_url)
VALUES
(
'Population Dataset',
'-',
'dl-de/by-2-0',
'https://www.regionalstatistik.de/genesis/online?operation=table&code=12411-01-01-4'
)
""")

conn.commit()

print("sources inserted")

cursor.close()
conn.close()