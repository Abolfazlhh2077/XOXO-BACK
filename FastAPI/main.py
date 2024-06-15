from fastapi import FastAPI
import uvicorn
import sqlite3



app = FastAPI()


conn = sqlite3.connect('DB.db')
cursor = conn.cursor()

conn.commit()


@app.post('/score')
async def update_score(name: str, status: str):
    if status.lower() == 'win':
        cursor.execute('''
            UPDATE Players
            SET points = points + 1
            WHERE name = ?
        ''', (name,))
    elif status.lower() == 'lose':
        cursor.execute('''
            UPDATE Players
            SET points = points - 1
            WHERE name = ?
        ''', (name,))
    conn.commit()
    return {"message": "Score updated successfully."}


@app.get('/score/{name}')
async def get_score(name: str):
    cursor.execute('''
        SELECT points
        FROM Players
        WHERE name = ?
    ''', (name,))
    result = cursor.fetchone()
    if result:
        return {"name": name, "points": result[0]}
    else:
        return {"message": "Player not found."}
