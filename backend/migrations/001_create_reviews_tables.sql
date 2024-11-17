-- Reviews table for approved reviews
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meal TEXT NOT NULL,
    meal_description TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity_score INTEGER NOT NULL,
    taste_score INTEGER NOT NULL,
    atmosphere_score INTEGER NOT NULL,
    overall_score INTEGER NOT NULL,
    comments TEXT
);

-- Pending reviews table
CREATE TABLE IF NOT EXISTS pending_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    meal TEXT NOT NULL,
    meal_description TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity_score INTEGER NOT NULL,
    taste_score INTEGER NOT NULL,
    atmosphere_score INTEGER NOT NULL,
    overall_score INTEGER NOT NULL,
    comments TEXT
);

-- Create indexes for better performance
CREATE INDEX idx_reviews_date ON reviews(date);
CREATE INDEX idx_pending_reviews_date ON pending_reviews(date); 