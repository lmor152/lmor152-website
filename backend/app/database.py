import os
from datetime import datetime
import sqlite3
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    def init_db(self):
        print(f"Initializing database at {self.db_path}")
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    meal TEXT NOT NULL,
                    meal_description TEXT,
                    reviewer TEXT NOT NULL,
                    price REAL,
                    quantity_score INTEGER,
                    taste_score INTEGER,
                    atmosphere_score INTEGER,
                    overall_score INTEGER,
                    comments TEXT
                );

                CREATE TABLE IF NOT EXISTS pending_reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    meal TEXT NOT NULL,
                    meal_description TEXT,
                    reviewer TEXT NOT NULL,
                    price REAL,
                    quantity_score INTEGER,
                    taste_score INTEGER,
                    atmosphere_score INTEGER,
                    overall_score INTEGER,
                    comments TEXT
                );
            """)
            # Add a test review if the reviews table is empty
            cursor = conn.execute("SELECT COUNT(*) FROM reviews")
            if cursor.fetchone()[0] == 0:
                conn.execute("""
                    INSERT INTO reviews (
                        name, meal, meal_description, reviewer, price,
                        quantity_score, taste_score, atmosphere_score, overall_score, comments
                    ) VALUES (
                        'Test Restaurant',
                        'Loaded Nachos',
                        'Classic nachos with all the toppings',
                        'System',
                        15.99,
                        8,
                        9,
                        7,
                        8,
                        'Initial test review'
                    )
                """)

    async def add_pending_review(self, review_data: Dict[str, Any]) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO pending_reviews (
                    name, meal, meal_description, reviewer, price,
                    quantity_score, taste_score, atmosphere_score, overall_score, comments
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review_data['name'],
                review_data['meal'],
                review_data['meal_description'],
                review_data['reviewer'],
                review_data['price'],
                review_data['quantity_score'],
                review_data['taste_score'],
                review_data['atmosphere_score'],
                review_data['overall_score'],
                review_data['comments']
            ))
            return cursor.lastrowid

    async def approve_review(self, review_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            review = conn.execute(
                "SELECT * FROM pending_reviews WHERE review_id = ?",
                (review_id,)
            ).fetchone()

            if not review:
                return False

            conn.execute("""
                INSERT INTO reviews (
                    name, meal, meal_description, reviewer, price,
                    quantity_score, taste_score, atmosphere_score, overall_score, comments
                ) SELECT 
                    name, meal, meal_description, reviewer, price,
                    quantity_score, taste_score, atmosphere_score, overall_score, comments
                FROM pending_reviews WHERE review_id = ?
            """, (review_id,))

            conn.execute("DELETE FROM pending_reviews WHERE review_id = ?", (review_id,))
            return True

    async def get_reviews(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM reviews ORDER BY date DESC")
            return [dict(row) for row in cursor.fetchall()]

    async def get_pending_reviews(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM pending_reviews ORDER BY date DESC")
            return [dict(row) for row in cursor.fetchall()]

    async def get_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get average scores
            scores = conn.execute("""
                SELECT 
                    AVG(quantity_score) as avg_quantity,
                    AVG(taste_score) as avg_taste,
                    AVG(atmosphere_score) as avg_atmosphere,
                    AVG(overall_score) as avg_overall,
                    AVG(price) as avg_price
                FROM reviews
            """).fetchone()
            
            # Get price distribution
            price_dist = conn.execute("""
                SELECT 
                    CASE 
                        WHEN price < 10 THEN '$'
                        WHEN price < 15 THEN '$$'
                        WHEN price < 20 THEN '$$$'
                        ELSE '$$$$'
                    END as price_range,
                    COUNT(*) as count
                FROM reviews
                GROUP BY price_range
            """).fetchall()
            
            # Get monthly averages
            monthly_avg = conn.execute("""
                SELECT 
                    strftime('%Y-%m', date) as month,
                    AVG(overall_score) as avg_score
                FROM reviews
                GROUP BY month
                ORDER BY month DESC
                LIMIT 6
            """).fetchall()
            
            return {
                "scores": dict(scores),
                "price_distribution": [dict(row) for row in price_dist],
                "monthly_averages": [dict(row) for row in monthly_avg]
            } 