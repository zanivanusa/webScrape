CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    locality TEXT,
    name TEXT,
    price TEXT,
    image_urls TEXT
);
