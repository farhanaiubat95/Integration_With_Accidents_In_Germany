from db_connection_common import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    ags VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    level VARCHAR(50),
    population BIGINT,
    area_km2 FLOAT,
    nuts3 VARCHAR(50)
)
""")

connection.commit()

print("regions table created successfully")

cursor.close()
connection.close()