import functions_framework
import os
import sqlalchemy
from sqlalchemy.sql import text
import pymysql
from flask import Flask, jsonify

def get_connection():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE_NAME"],
            host=os.environ["INSTANCE_HOST"],
            port=os.environ["DATABASE_PORT"],
            query={}
        )
    )
    return pool

def get_dept():
    connection = get_connection()
    with connection.connect() as conn:
        result = conn.execute(text("SELECT dept_name, dept_name_eng FROM tbl_dept"))
        departments = [{"dept_name": row.dept_name, "dept_name_eng": row.dept_name_eng} for row in result]
        return jsonify(departments)

@functions_framework.http
def hello_http(request):
    return get_dept()