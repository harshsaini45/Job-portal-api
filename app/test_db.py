from app.database import engine

try:
    with engine.connect() as connection:
        print("database connection successfully")
        
except Exception as e:
    print("database connection failed")
    print(e)