import os
import sqlalchemy
import pymysql
from google.cloud import secretmanager
from flask import Flask, jsonify

app = Flask(__name__)

def access_secret_version(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.environ['GCP_PROJECT']}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def get_connection():
    username = access_secret_version("DATABASE_USER")
    password = access_secret_version("DATABASE_PASSWORD")
    database = access_secret_version("DATABASE_NAME")
    host = access_secret_version("INSTANCE_HOST")
    
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=username,
            password=password,
            database=database,
            host=host
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
