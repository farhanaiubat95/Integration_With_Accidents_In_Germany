from fastapi import APIRouter
from database import get_connection

router = APIRouter(
    tags=["Import Runs"]
)

@router.get("/import-runs")
def get_import_runs():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM import_runs
    ORDER BY run_id DESC
    """)

    data = cursor.fetchall()

    total_runs = len(data)

    cursor.close()
    conn.close()

    return {
        "total_import_runs": total_runs,
        "results": data
    }