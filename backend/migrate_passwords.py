"""
Migration script to hash existing plain text passwords in the database.
Run this ONCE to convert all plain text passwords to hashed passwords.
"""
import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_passwords():
    """Hash all plain text passwords in the users table."""
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'tic_tac_toe_db')
    )
    cursor = conn.cursor(dictionary=True)
    
    # Get all users
    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users to migrate...")
    
    for user in users:
        user_id = user['id']
        username = user['username']
        plain_password = user['password']
        
        # Check if password is already hashed (starts with pbkdf2:sha256: or scrypt:)
        if plain_password.startswith('pbkdf2:') or plain_password.startswith('scrypt:'):
            print(f"  [{username}] Already hashed, skipping...")
            continue
        
        # Hash the password
        hashed_password = generate_password_hash(plain_password)
        
        # Update database
        update_query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(update_query, (hashed_password, user_id))
        
        print(f"  [{username}] Password hashed successfully!")
    
    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n✅ Migration completed successfully!")
    print("You can now login with your existing passwords.")

if __name__ == "__main__":
    print("=" * 60)
    print("Password Migration Script")
    print("=" * 60)
    print("\nThis script will convert all plain text passwords to hashed passwords.")
    print("WARNING: This is a ONE-TIME operation. Do not run it multiple times!")
    
    confirm = input("\nDo you want to proceed? (yes/no): ")
    
    if confirm.lower() == 'yes':
        migrate_passwords()
    else:
        print("\nMigration cancelled.")
