import sqlite3

def reset_db():
    conn = sqlite3.connect('../articles.db')
    cursor = conn.cursor()
    
    cursor.execute("drop table if exists articles")
    
    cursor.execute('''create table articles (
                     id integer primary key autoincrement,
                     title text unique not null,
                     content text not null,
                     image text,
                     category text);''')
    
    conn.commit()
    conn.close()
    print("database reset complete.")

if __name__ == "__main__":
    reset_db()