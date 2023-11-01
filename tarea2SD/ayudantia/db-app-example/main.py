from connection import init_db

def serve():
    cursor.execute('SELECT * FROM items')
    users = cursor.fetchall()
    print(users)

if __name__ == '__main__':
    conn = init_db()
    cursor = conn.cursor()
    serve()