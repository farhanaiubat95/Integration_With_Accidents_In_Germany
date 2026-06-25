from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS accidents
""")

cursor.execute("""
CREATE TABLE accidents (

    accident_id INT AUTO_INCREMENT PRIMARY KEY,

    ULAND INT,
    UREGBEZ INT,
    UKREIS INT,
    UGEMEINDE INT,

    ags VARCHAR(8),

    region_id INT DEFAULT 0,

    UJAHR INT,
    UMONAT INT,
    USTUNDE INT,
    UWOCHENTAG INT,

    UKATEGORIE INT,
    UART INT,
    UTYP1 INT,

    ULICHTVERH INT,
    IstStrassenzustand INT,

    IstRad INT,
    IstPKW INT,
    IstFuss INT,
    IstKrad INT,
    IstGkfz INT,
    IstSonstige INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("Accidents table created.")

cursor.close()
conn.close()