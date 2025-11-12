ALTER TABLE subscribers 
ADD COLUMN phone_number VARCHAR(20) NULL AFTER last_name;

CREATE INDEX idx_subscribers_phone ON subscribers(phone_number);