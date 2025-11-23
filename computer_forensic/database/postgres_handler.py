import psycopg2

def insert_postgres(features):
    conn = psycopg2.connect(
        dbname="forensics",
        user="postgres",
        password="yourpassword",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cases (space, file_system, hash, total_files, keys) VALUES (%s, %s, %s, %s, %s)",
        (features.get("space"), features.get("file_system"), features.get("hash"),
         features.get("total_files"), str(features.get("keys")))
    )
    conn.commit()
    cur.close()
    conn.close()
