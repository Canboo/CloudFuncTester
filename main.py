import os
import sqlalchemy
import pymysql
from flask import Flask, jsonify

# 設定資料庫連接資訊
def get_connection():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE_NAME"],
            host=os.environ["INSTANCE_HOST"]
        )
    )
    return pool

@app.route('/')
def get_dept():
    connection = get_connection()
    with connection.connect() as conn:
        result = conn.execute("SELECT dept_name, dept_name_eng FROM tbl_dept")
        departments = [{"dept_name": row["dept_name"], "dept_name_eng": row["dept_name_eng"]} for row in result]
        return jsonify(departments)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

