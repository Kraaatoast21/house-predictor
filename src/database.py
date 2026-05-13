import mysql.connector
from mysql.connector import Error
import hashlib

from src.config import DB_CONFIG
from src.utils.cache import GLOBAL_CACHE


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    """Self-healing initialization: Creates DB and Tables if they don't exist."""
    try:
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop('database')
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                bedrooms INT,
                bathrooms INT,
                floor_area DECIMAL(10,2),
                land_size DECIMAL(10,2),
                subdivision VARCHAR(100),
                build_year INT,
                predicted_price DECIMAL(15,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            h_admin = hash_password('admin123')
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', %s, 'admin')", (h_admin,))
        
        # 3. Migration: Hash existing plain-text passwords
        cursor.execute("SELECT id, password FROM users")
        all_users = cursor.fetchall()
        for uid, pwd in all_users:
            # If length is not 64 (SHA-256 hex), it's likely plain text
            if len(pwd) != 64 or not all(c in '0123456789abcdefABCDEF' for c in pwd):
                cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hash_password(pwd), uid))
                
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Critical Database Failure: {e}")
        return False

def authenticate_user(username, password):
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        h_pass = hash_password(password)
        query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, h_pass))
        user = cursor.fetchone()
        conn.close()
        return user
    except:
        return None

@GLOBAL_CACHE.memoize(ttl=300)
def get_user_predictions(user_id):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM predictions WHERE user_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        conn.close()
        return records
    except:
        return []

@GLOBAL_CACHE.memoize(ttl=600)
def get_all_users():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password, role FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except:
        return []

@GLOBAL_CACHE.memoize(ttl=300)
def get_all_predictions():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.id, u.username, p.subdivision, p.floor_area, p.land_size, p.bedrooms, p.bathrooms, p.build_year, p.predicted_price, p.created_at
            FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()
        conn.close()
        return records
    except:
        return []

def save_prediction(user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO predictions (user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price))
        conn.commit()
        conn.close()
        
        # Invalidate cache
        get_all_predictions.invalidate()
        get_user_predictions.invalidate()
        
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def register_user(username, password, role='user'):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            conn.close()
            return "EXISTS"
        
        h_pass = hash_password(password)
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, h_pass, role))
        conn.commit()
        conn.close()
        
        # Invalidate cache
        get_all_users.invalidate()
        
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def delete_user(user_id):
    if user_id == 1: return False
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        # Cascading delete should handle predictions if setup correctly in MySQL
        conn.commit()
        conn.close()
        
        # Invalidate caches
        get_all_users.invalidate()
        get_all_predictions.invalidate()
        get_user_predictions.invalidate()
        
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def update_user_credentials(user_id, new_username, new_password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        hashed_p = hash_password(new_password)
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", 
                      (new_username, hashed_p, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def update_user_role(user_id, role):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def update_user(user_id, new_username, new_password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s AND id != %s", (new_username, user_id))
        if cursor.fetchone():
            conn.close()
            return "EXISTS"
        
        query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
        cursor.execute(query, (new_username, new_password, user_id))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"DATABASE ERROR: {e}")
        return False

def delete_prediction(user_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def backup_database(output_path):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor(dictionary=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("-- EstateWise Intelligence Database Backup\n")
            f.write(f"-- Generated: {import_datetime()}\n\n")
            
            for table in ["users", "predictions"]:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                if not rows: continue
                
                f.write(f"-- Table: {table}\n")
                for row in rows:
                    cols = ", ".join(row.keys())
                    vals = []
                    for v in row.values():
                        if v is None: vals.append("NULL")
                        elif isinstance(v, (int, float)): vals.append(str(v))
                        else:
                            clean_v = str(v).replace("'", "''")
                            vals.append(f"'{clean_v}'")
                    vals_str = ", ".join(vals)
                    f.write(f"INSERT INTO {table} ({cols}) VALUES ({vals_str});\n")
                f.write("\n")
        conn.close()
        return True
    except Exception as e:
        print(f"BACKUP ERROR: {e}")
        return False

def import_datetime():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
