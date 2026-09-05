from fastapi import APIRouter
from database import get_connection

router = APIRouter(
    prefix="/metadata",
    tags=["Metadata"]
)

@router.get("/sources")
def get_sources():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM sources
    """)

    data = cursor.fetchall()

    total_sources = len(data)

    cursor.close()
    conn.close()

    return {
        "total_sources": total_sources,
        "results": data
    }