#!/bin/bash

set -e

echo "🚀 PROG8850 Assignment 4 - Complete Workflow"
echo "============================================="

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker stop mysql_db 2>/dev/null || true
    docker rm mysql_db 2>/dev/null || true
}

# Set trap for cleanup
trap cleanup EXIT

# Step 1: Start MySQL
echo "📦 Step 1: Starting MySQL container..."
docker run --name mysql_db \
    -e MYSQL_ROOT_PASSWORD=rootpassword \
    -e MYSQL_DATABASE=subscribers_db \
    -e MYSQL_USER=app_user \
    -e MYSQL_PASSWORD=app_password \
    -p 3306:3306 \
    -d mysql:8.0 \
    --default-authentication-plugin=mysql_native_password

# Step 2: Wait for MySQL
echo "⏳ Step 2: Waiting for MySQL to be ready..."
for i in {1..30}; do
    if docker exec mysql_db mysqladmin ping -uroot -prootpassword --silent 2>/dev/null; then
        echo "✅ MySQL is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ MySQL failed to start"
        docker logs mysql_db
        exit 1
    fi
    sleep 2
done

# Step 3: Create Flyway user
echo "👤 Step 3: Creating Flyway user..."
docker exec mysql_db mysql -uroot -prootpassword -e "
CREATE USER IF NOT EXISTS 'flyway_user'@'%' IDENTIFIED BY 'flyway_password';
GRANT ALL PRIVILEGES ON subscribers_db.* TO 'flyway_user'@'%';
FLUSH PRIVILEGES;"

# Step 4: Run initial migrations
echo "🔄 Step 4: Running initial migrations..."
flyway -url="jdbc:mysql://127.0.0.1:3306/subscribers_db" \
    -user="flyway_user" \
    -password="flyway_password" \
    -locations="filesystem:flyway/migrations_initial" \
    migrate

# Step 5: Run incremental migrations
echo "🔄 Step 5: Running incremental migrations..."
flyway -url="jdbc:mysql://127.0.0.1:3306/subscribers_db" \
    -user="flyway_user" \
    -password="flyway_password" \
    -locations="filesystem:flyway/migrations_incremental" \
    migrate

# Step 6: Run tests
echo "🧪 Step 6: Running automated tests..."
python -m pytest tests/ -v

# Step 7: Final verification
echo "📊 Step 7: Final verification..."
echo "Database schema:"
docker exec mysql_db mysql -uapp_user -papp_password -e "USE subscribers_db; SHOW TABLES; DESCRIBE subscribers;"

echo "Migration history:"
flyway -url="jdbc:mysql://127.0.0.1:3306/subscribers_db" \
    -user="flyway_user" \
    -password="flyway_password" \
    info

echo ""
echo "🎉 ALL STEPS COMPLETED SUCCESSFULLY!"
echo "📝 Assignment requirements checked:"
echo "   ✅ MySQL Environment Provisioned"
echo "   ✅ Flyway Migrations Executed"
echo "   ✅ Automated CRUD Tests Passed"
echo "   ✅ Database Schema Verified"