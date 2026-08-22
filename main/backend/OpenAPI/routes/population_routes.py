from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/population")
def get_population():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM population
        LIMIT 30
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data