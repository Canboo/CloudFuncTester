import functions_framework
import os
import sqlalchemy
from sqlalchemy.sql import text
import pymysql
from flask import Flask, jsonify, make_response

def get_connection():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE_NAME"],
            host=os.environ["INSTANCE_HOST"],
            port=int(os.environ["DATABASE_PORT"]),
            query={}
        )
    )
    return pool

def get_dept():
    try:
        connection = get_connection()
    except Exception as e:
        return make_response(jsonify({"error": "Database connection error"}), 500)
    
    try:
        with connection.connect() as conn:
            result = conn.execute(text("SELECT dept_name, dept_name_eng FROM tbl_dept"))
            departments = [{"dept_name": row.dept_name, "dept_name_eng": row.dept_name_eng} for row in result]
            return jsonify(departments)
    except Exception as e:
        return make_response(jsonify({"error": f"Database query error: {str(e)}"}), 500)

@functions_framework.http
def hello_http(request):
    return get_dept()