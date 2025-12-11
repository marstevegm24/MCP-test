import os
import typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2
from psycopg2 import RealDictCursor
from fastmcp import FastMCP

app = FastMCP("sharksia-db-server")

def get_db_connection():    ####funcion que permite conectarme con la DB
    conn = psycopg2.connect(
        host=os.environ("DB_HOST"),
        port=int(os.environ("DB_PORT")),        
        user=os.environ("DB_USER"),
        password=os.environ("DB_PASSWORD"),
        database=os.environ("DB_NAME"),
        cursor_factory=RealDictCursor   ###para que funcione debe tener un listado de herramientas
    )
    return conn

@app.tool
def list_employees(limit: int = 5)-> List[Dict[str, Any]]:
    """Listar empleados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, position, department, salary, hire_dateF
        ROM employees 
        ORDER BY id
        LIMIT %s      ##arumento seguro
        """, (limit,))
        rows = cursor.fetchall()
        employees = []

        for row in rows:
            employees.append({
                "id": row["id"],
                "name": row["name"],
                "position": row["position"],
                "department": row["department"],
                "salary": row["salary"],
                "hire_date": row["hire_date"].strftime("%Y-%m-%d")
            })
        cursor.close()
        conn.close()
        return employees
    exept Exception as e:
    return {
        'error' : f'Error alobtener empleados: {str(e)}'
    }

@app.tool
def app_employee(
    name: str, 
    position: str, 
    department: str, 
    salary: float, 
    hire_date: Optional[str] = None):
    """Agregar un nuevo empleado"""
    try:
        if not name.strip():
            return {"error": "El nombre del empleado es requerido."}

        if salary <= 0:
            return {"error": "El salario no puede ser negativo."}

        if not hire_date:
            hire_date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO employees (name, position, department, salary, hire_date)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, position, department, salary, hire_date
        """, (name.strip(), position.strip(), department.strip(), salary, hire_date))

        new_employee = cursor.fetchone()
        conn.commit()

        cursor.close()
        conn.close()

        return {
            "success": True,
            "employee": {
                "id": new_employee["id"],
                "name": new_employee["name"],
                "position": new_employee["position"],
                "department": new_employee["department"],
                "salary": new_employee["salary"],
                "hire_date": new_employee["hire_date"].strftime("%Y-%m-%d")
            }
        }
    except Exception as e:
        return {
            "error": f"Error al agregar empleado: {str(e)}"
        }

if __name__ == "__main__":
    app.run(transport="sse", host="0.0.0.0", port=3000)
