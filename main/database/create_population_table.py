from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS population
""")

cursor.execute("""
CREATE TABLE population (
    population_id INT AUTO_INCREMENT PRIMARY KEY,

    ags VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,

    level VARCHAR(50) NOT NULL,

    population INT NOT NULL,

    region_id INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("Population table created successfully.")

cursor.close()
conn.close()