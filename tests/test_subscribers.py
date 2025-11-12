import pytest
import mysql.connector
import time
import os

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'app_user',
    'password': 'app_password',
    'database': 'subscribers_db',
    'port': 3306,
    'auth_plugin': 'mysql_native_password'
}

def get_db_connection():
    """Create and return database connection"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                print(f"Database connection failed: {err}")
                raise

def cleanup_test_data():
    """Clean up test data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscribers WHERE email LIKE 'test%@example.com'")
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass

@pytest.fixture(autouse=True)
def cleanup_before_tests():
    """Cleanup before each test"""
    cleanup_test_data()
    yield
    cleanup_test_data()

def test_create_subscriber():
    """Test CREATE operation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert a new subscriber
    insert_query = """
    INSERT INTO subscribers (email, first_name, last_name, phone_number, is_premium)
    VALUES (%s, %s, %s, %s, %s)
    """
    subscriber_data = ('test1@example.com', 'John', 'Doe', '+1234567890', True)
    
    cursor.execute(insert_query, subscriber_data)
    conn.commit()
    
    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email = %s", ('test1@example.com',))
    count = cursor.fetchone()[0]
    
    assert count == 1, "Subscriber was not created successfully"
    
    cursor.close()
    conn.close()

def test_read_subscriber():
    """Test READ operation"""
    # First create a subscriber to read
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subscribers (email, first_name, last_name) VALUES (%s, %s, %s)",
        ('test2@example.com', 'Alice', 'Smith')
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    # Now read it
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM subscribers WHERE email = %s", ('test2@example.com',))
    subscriber = cursor.fetchone()
    
    assert subscriber is not None, "Subscriber not found"
    assert subscriber['email'] == 'test2@example.com'
    assert subscriber['first_name'] == 'Alice'
    assert subscriber['last_name'] == 'Smith'
    
    cursor.close()
    conn.close()

def test_update_subscriber():
    """Test UPDATE operation"""
    # First create a subscriber
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subscribers (email, first_name, last_name) VALUES (%s, %s, %s)",
        ('test3@example.com', 'Bob', 'Johnson')
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    # Update the subscriber
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_query = """
    UPDATE subscribers 
    SET first_name = %s, last_name = %s, is_premium = %s 
    WHERE email = %s
    """
    update_data = ('Robert', 'Johnsson', True, 'test3@example.com')
    
    cursor.execute(update_query, update_data)
    conn.commit()
    
    # Verify update
    cursor.execute("SELECT first_name, last_name, is_premium FROM subscribers WHERE email = %s", 
                   ('test3@example.com',))
    result = cursor.fetchone()
    
    assert result[0] == 'Robert', "First name was not updated"
    assert result[1] == 'Johnsson', "Last name was not updated"
    assert result[2] == True, "Premium status was not updated"
    
    cursor.close()
    conn.close()

def test_delete_subscriber():
    """Test DELETE operation"""
    # First create a subscriber
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subscribers (email, first_name, last_name) VALUES (%s, %s, %s)",
        ('test4@example.com', 'Carol', 'Williams')
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    # Delete the subscriber
    conn = get_db_connection()
    cursor = conn.cursor()
    
    delete_query = "DELETE FROM subscribers WHERE email = %s"
    cursor.execute(delete_query, ('test4@example.com',))
    conn.commit()
    
    # Verify deletion
    cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email = %s", ('test4@example.com',))
    count = cursor.fetchone()[0]
    
    assert count == 0, "Subscriber was not deleted successfully"
    
    cursor.close()
    conn.close()