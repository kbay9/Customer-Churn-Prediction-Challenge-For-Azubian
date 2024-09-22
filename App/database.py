import sqlite3
import bcrypt

DATABASE_NAME = "churn.db"

def get_connection():
    """Create and return a connection to the database."""
    return sqlite3.connect(DATABASE_NAME)

def create_customer_data_table():
    """Create the customer_data table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TENURE TEXT,
            MONTANT REAL,
            FREQUENCE_RECH REAL,
            REVENUE REAL,
            ARPU_SEGMENT REAL,
            FREQUENCE REAL,
            DATA_VOLUME REAL,
            ON_NET REAL,
            ORANGE REAL,
            TIGO REAL,
            ZONE1 REAL,
            ZONE2 REAL,
            MRG TEXT,
            REGULARITY REAL,
            TOP_PACK TEXT,
            FREQ_TOP_PACK REAL,
            CHURN TEXT,
            Probability REAL,
            ModelUsed TEXT
        )
    """)
    conn.commit()
    conn.close()

def authenticate(username, password):
    """Authenticate a user with username and password."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    db_password = cursor.fetchone()
    conn.close()
    if db_password:
        db_password = db_password[0]
        if isinstance(db_password, str):
            db_password = db_password.encode('utf-8')
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, db_password):
            return True
    return False

def save_prediction(data, predictions):
    """Save customer data and predictions."""
    conn = get_connection()
    cursor = conn.cursor()
    for model, probability in predictions.items():
        prediction = 'Yes' if probability > 0.5 else 'No'
        cursor.execute("""
            INSERT INTO customer_data (TENURE, MONTANT, FREQUENCE_RECH, REVENUE, ARPU_SEGMENT, FREQUENCE,
                                       DATA_VOLUME, ON_NET, ORANGE, TIGO, ZONE1, ZONE2, MRG, REGULARITY,
                                       TOP_PACK, FREQ_TOP_PACK, CHURN, Probability, ModelUsed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*data.values(), prediction, probability, model))
    conn.commit()
    conn.close()
