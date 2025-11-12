import pytest
import mysql.connector
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'app_user',
    'password': 'app_password',
    'database': 'subscribers_db',
    'port': 3306
}

def get_db_connection():
    """Create and return database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def test_create_subscriber():
    """Test CREATE operation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert a new subscriber
    insert_query = """
    INSERT INTO subscribers (email, first_name, last_name, phone_number, is_premium)
    VALUES (%s, %s, %s, %s, %s)
    """
    subscriber_data = ('test@example.com', 'John', 'Doe', '+1234567890', True)
    
    cursor.execute(insert_query, subscriber_data)
    conn.commit()
    
    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email = %s", ('test@example.com',))
    count = cursor.fetchone()[0]
    
    assert count == 1, "Subscriber was not created successfully"
    
    cursor.close()
    conn.close()

def test_read_subscriber():
    """Test READ operation"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Retrieve the subscriber
    cursor.execute("SELECT * FROM subscribers WHERE email = %s", ('test@example.com',))
    subscriber = cursor.fetchone()
    
    assert subscriber is not None, "Subscriber not found"
    assert subscriber['email'] == 'test@example.com'
    assert subscriber['first_name'] == 'John'
    assert subscriber['last_name'] == 'Doe'
    assert subscriber['phone_number'] == '+1234567890'
    assert subscriber['is_premium'] == True
    
    cursor.close()
    conn.close()

def test_update_subscriber():
    """Test UPDATE operation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update subscriber information
    update_query = """
    UPDATE subscribers 
    SET first_name = %s, last_name = %s, is_premium = %s 
    WHERE email = %s
    """
    update_data = ('Jane', 'Smith', False, 'test@example.com')
    
    cursor.execute(update_query, update_data)
    conn.commit()
    
    # Verify update
    cursor.execute("SELECT first_name, last_name, is_premium FROM subscribers WHERE email = %s", 
                   ('test@example.com',))
    result = cursor.fetchone()
    
    assert result[0] == 'Jane', "First name was not updated"
    assert result[1] == 'Smith', "Last name was not updated"
    assert result[2] == False, "Premium status was not updated"
    
    cursor.close()
    conn.close()

def test_delete_subscriber():
    """Test DELETE operation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete the subscriber
    delete_query = "DELETE FROM subscribers WHERE email = %s"
    cursor.execute(delete_query, ('test@example.com',))
    conn.commit()
    
    # Verify deletion
    cursor.execute("SELECT COUNT(*) FROM subscribers WHERE email = %s", ('test@example.com',))
    count = cursor.fetchone()[0]
    
    assert count == 0, "Subscriber was not deleted successfully"
    
    cursor.close()
    conn.close()

@pytest.fixture(autouse=True)
def cleanup_after_tests():
    """Cleanup fixture to ensure test isolation"""
    yield
    # Clean up any test data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE email = 'test@example.com'")
    conn.commit()
    cursor.close()
    conn.close()