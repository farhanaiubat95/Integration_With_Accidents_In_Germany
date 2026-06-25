from db_connection_common import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS import_runs (

    run_id INT AUTO_INCREMENT PRIMARY KEY,

    source_id INT,

    table_name VARCHAR(100),

    records_imported INT,

    import_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status VARCHAR(50),

    FOREIGN KEY (source_id)
    REFERENCES sources(source_id)
)
""")

conn.commit()

print("import_runs table created")

cursor.close()
conn.close()