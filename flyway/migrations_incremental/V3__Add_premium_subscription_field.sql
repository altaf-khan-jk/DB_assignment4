ALTER TABLE subscribers 
ADD COLUMN is_premium BOOLEAN DEFAULT FALSE AFTER is_active;

CREATE INDEX idx_subscribers_premium ON subscribers(is_premium);