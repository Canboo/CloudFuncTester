import os
import sqlalchemy
import pymysql
from flask import Flask, jsonify

# # 設定資料庫連接資訊
# def get_connection():
#     pool = sqlalchemy.create_engine(
#         sqlalchemy.engine.url.URL(
#             drivername="mysql+pymysql",
#             username=os.environ["DATABASE_USER"],
#             password=os.environ["DATABASE_PASSWORD"],
#             database=os.environ["DATABASE_NAME"],
#             host=os.environ["INSTANCE_HOST"]
#         )
#     )
#     return pool

# @app.route('/')
# def get_dept():
#     connection = get_connection()
#     with connection.connect() as conn:
#         result = conn.execute("SELECT dept_name, dept_name_eng FROM tbl_dept")
#         departments = [{"dept_name": row["dept_name"], "dept_name_eng": row["dept_name_eng"]} for row in result]
#         return jsonify(departments)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host='0.0.0.0', port=port)

import os

import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    db_host = os.environ["INSTANCE_HOST"]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = os.environ["DATABASE_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DATABASE_PASSWORD"]  # e.g. 'my-db-password'
    db_name = os.environ["DATABASE_NAME"]  # e.g. 'my-database'
    db_port = os.environ["DATABASE_PORT"]  # e.g. 3306

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        )
    )
    return pool
