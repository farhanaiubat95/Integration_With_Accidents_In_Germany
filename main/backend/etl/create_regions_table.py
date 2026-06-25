from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    ags VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    level VARCHAR(50),
    region_type VARCHAR(100),
    nuts3 VARCHAR(50),
    area_km2 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
)
""")

conn.commit()

print("regions table created successfully")

cursor.close()
conn.close()