import sqlite3

class UserManager:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        self.conn.commit()

    def insert_user(self, username, password, role='user'):
        # VULNERABLE: String formatting creates SQL injection risk
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        self.cursor.execute(query)
        self.conn.commit()

    def get_user_by_username(self, username):
        # VULNERABLE: Direct string concatenation in query
        query = f"SELECT * FROM users WHERE username = '{username}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

def main():
    user_manager = UserManager()
    
    # Insert some test users
    user_manager.insert_user('admin', 'secret_password', 'admin')
    user_manager.insert_user('alice', 'user_password')
    
    # Demonstrate SQL injection vulnerability
    malicious_username = "' OR role = 'admin' --"
    compromised_users = user_manager.get_user_by_username(malicious_username)
    print("Potentially exposed admin users:", compromised_users)

if __name__ == "__main__":
    main()