# German Traffic Accident Data Integration Platform

## Project Overview

This project integrates German traffic accident data, regional information, and population statistics into a unified MySQL database. The data is exposed through a FastAPI-based REST API and visualized through a Streamlit dashboard.

The platform supports accident analysis, population-based accident rates, accident density calculations, and other analytical queries.

---

# 1. Technologies Used

| Component               | Technology        |
| ----------------------- | ----------------- |
| Programming Language    | Python            |
| Backend Framework       | FastAPI           |
| Database                | MySQL             |
| Database Administration | phpMyAdmin        |
| Frontend                | Streamlit         |
| API Documentation       | Swagger / OpenAPI |
| Data Processing         | Pandas            |

---

# 2. Database Setup

### Step 1 – Create Database

connect mysql + python :

```bash
pip install mysql-connector-python
```
Create a MySQL database:

-> create file - connect_mysql_database.py
   database -> "accidents_germany"


### Step 2 – Configure Database Connection

Update the connection settings inside:

```python
db_connection_common.py
```

Example:

```python
host="localhost",
user="root",
password="",
database="accidents_germany"
```

---


# 4. Download Source Data

Place the datasets inside the `dataset folder/` folder.

| Dataset            | Purpose                     | Link 
| ------------------ | --------------------------- |------------------------------------------------------------------------------------
| Unfallatlas        | Traffic accident records    | https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/ 
| Regionalatlas      | Region and area information | https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html
| Population Dataset | Population statistics       | https://www.regionalstatistik.de/genesis/online?operation=table&code=12411-01-01-4

---

# 6. Run ETL Process

Execute the ETL scripts in the following order:

```bash
python etl/import_regions_to_mysql.py
```

```bash
python etl/import_population_to_mysql.py
```

```bash
python etl/import_accidents_to_mysql.py
```

```bash
python etl/insert_sources.py
```

---

# 7. Run Backend API

install FastAPI :

```bash
pip install fastapi uvicorn
pip install fastapi uvicorn mysql-connector-python pandas
```

Start FastAPI:

```bash
cd main/backend/OpenAPI
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

---

# 8. Run Frontend Dashboard

Streamlit install :

```bash
pip install streamlit-extras
```

Run Streamlit :
```bash
cd main/frontend
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---


