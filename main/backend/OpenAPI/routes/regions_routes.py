from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/regions")
def get_regions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM regions
        LIMIT 30
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data