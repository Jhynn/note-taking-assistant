from app.core.database import db
from app.models.notes import Note

def reset_database():
    try:
        db.connect()
        print("Connecting to MariaDB...")
        
        print("Dropping 'notes' table...")
        db.drop_tables([Note], safe=True)
        
        print("Creating 'notes' table...")
        db.create_tables([Note], safe=True)
        
        print("Sucess! The DB was rebuilt.")
        
    except Exception as e:
        print(f"Something went wrong: {e}")

    finally:
        if not db.is_closed():
            db.close()

if __name__ == "__main__":
    reset_database()
