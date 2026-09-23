from pathlib import Path
from db.database import Database
from models.portfolio import Portfolio

def main():
    db_dir = Path(__file__).parent
    db_path = db_dir / "user_data.db"
    user_db = Database(db_path)
    user_portfolio = Portfolio(user_db)

if __name__ == "__main__":
    main()
