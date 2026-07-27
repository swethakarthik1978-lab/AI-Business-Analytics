from config import PROJECT_NAME, VERSION
from database.database import engine, Base
import database.models

def main():
    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)
    print("Welcome to the AI Business Analytics Platform")

    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__": 
    main() 