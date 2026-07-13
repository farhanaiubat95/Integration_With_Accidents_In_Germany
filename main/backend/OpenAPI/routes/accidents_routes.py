from fastapi import APIRouter
from database import get_connection

router = APIRouter()

STATE_MAP = {
        "sh": 1,
        "hh": 2,
        "ni": 3,
        "hb": 4,
        "nw": 5,
        "he": 6,
        "rp": 7,
        "bw": 8,
        "by": 9,
        "sl": 10,
        "be": 11,
        "bb": 12,
        "mv": 13,
        "sn": 14,
        "st": 15,
        "th": 16,

        "schleswig-holstein": 1,
        "hamburg": 2,
        "niedersachsen": 3,
        "bremen": 4,
        "nordrhein-westfalen": 5,
        "hessen": 6,
        "rheinland-pfalz": 7,
        "baden-württemberg": 8,
        "bayern": 9,
        "saarland": 10,
        "berlin": 11,
        "brandenburg": 12,
        "mecklenburg-vorpommern": 13,
        "sachsen": 14,
        "sachsen-anhalt": 15,
        "thüringen": 16,
}

CATEGORY_MAP = {
        "persons killed": 1,
        "killed": 1,
        "fatality": 1,
        "death": 1,
        
        "seriously injured": 2,
        "serious": 2,

        "slightly injured": 3,
        "slight": 3,
        "minor": 3
}   

# Get accidents with optional filters
@router.get("/accidents")
def get_accidents(
    year: int | None = None,
    month: int | None = None,
    state: str | None = None,
    category: str | None = None
):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM accidents
        WHERE 1=1
    """

    count_query = """
        SELECT COUNT(*) AS total
        FROM accidents
        WHERE 1=1
    """

    params = []

    # YEAR
    if year is not None:
        query += " AND UJAHR = %s"
        count_query += " AND UJAHR = %s"
        params.append(year)

    # MONTH
    if month is not None:
        query += " AND UMONAT = %s"
        count_query += " AND UMONAT = %s"
        params.append(month)

    # STATE
    if state:

        try:
            state_id = int(state)

        except ValueError:
            state_id = STATE_MAP.get(state.lower().strip())

        if state_id is None:

            cursor.close()
            conn.close()

            return {
                "error": "Invalid state"
            }

        query += " AND ULAND = %s"
        count_query += " AND ULAND = %s"

        params.append(state_id)

    # CATEGORY
    if category:

        category_id = CATEGORY_MAP.get(category.lower().strip())
        if category_id is None:

            cursor.close()
            conn.close()

            return {
                "error": "Invalid category"
            }

        query += " AND UKATEGORIE = %s"
        count_query += " AND UKATEGORIE = %s"

        params.append(category_id)

    # TOTAL RECORDS
    cursor.execute(count_query, tuple(params))
    total_records = cursor.fetchone()["total"]

    # DATA
    query += " LIMIT 100"

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_records": total_records,
        "returned_records": len(data),
        "filters": {
            "year": year,
            "month": month,
            "state": state,
            "category": category
        },
        "data": data
    }

# Q1 : What is the earliest accident year in the complete dataset?
@router.get("/accidents/earliest-year")
def earliest_year():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT MIN(UJAHR) AS earliest_year
        FROM accidents
    """)

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data

# Q3 From which year onwards is data available for Nordrhein-Westfalen?
# Q4 From which year onwards is data available for Mecklenburg-Vorpommern?
@router.get("/accidents/data-availability/")
def data_availability(state: str):

    state_id = STATE_MAP.get(state.lower().strip())

    if state_id is None:
        return {"error": "Invalid state"}

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT MIN(UJAHR) AS first_year
        FROM accidents
        WHERE ULAND = %s
    """, (state_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "state": state,
        "first_year": data["first_year"],
        "received": state,
        "normalized": state.lower().strip(),
        "lookup": STATE_MAP.get(state.lower().strip())
    }


# Get latest accident year in the complete dataset


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT MAX(UJAHR) AS latest_year
        FROM accidents
    """)

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data