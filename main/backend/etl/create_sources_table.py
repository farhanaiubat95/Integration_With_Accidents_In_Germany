from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sources (

    source_id INT AUTO_INCREMENT PRIMARY KEY,

    source_name VARCHAR(100) NOT NULL,

    provider VARCHAR(200),

    license VARCHAR(200),

    source_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("sources table created")

cursor.close()
conn.close()