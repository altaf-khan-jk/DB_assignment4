#!/bin/bash

echo "🧪 Individual Component Testing"

# Test MySQL connection
echo "1. Testing MySQL connection..."
docker exec mysql_db mysql -uapp_user -papp_password -e "SELECT 'MySQL connection successful' as status;"

# Test Flyway
echo "2. Testing Flyway..."
flyway -version

# Test Python environment
echo "3. Testing Python environment..."
python -c "import mysql.connector; print('MySQL connector OK')"
python -c "import pytest; print('Pytest OK')"

# Test database schema
echo "4. Testing database schema..."
docker exec mysql_db mysql -uapp_user -papp_password -e "
USE subscribers_db;
SHOW TABLES;
DESCRIBE subscribers;
"

echo "✅ All individual tests completed"