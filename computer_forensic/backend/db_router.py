from database.mongo_handler import insert_mongodb
from database.postgres_handler import insert_postgres
from database.neo4j_handler import insert_neo4j
from database.vector_handler import insert_vector

def insert_to_db(db_type, features):
    if db_type == 'mongodb':
        insert_mongodb(features)
    elif db_type == 'postgres':
        insert_postgres(features)
    elif db_type == 'neo4j':
        insert_neo4j(features)
    elif db_type == 'vector':
        insert_vector(features)
    else:
        print(f"Unknown DB type: {db_type}")
