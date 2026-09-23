from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Version 2 - Deployed using Jenkins!"
    })


@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    name = data.get("name")
    roll_no = data.get("roll_no")
    division = data.get("division")

    if not name or not roll_no or not division:
        return jsonify({
            "error": "name, roll_no and division are required"
        }), 400

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            INSERT INTO students (name, roll_no, division)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql,
                (name, roll_no, division)
            )

        connection.commit()

        return jsonify({
            "message": "Student added successfully"
        }), 201

    finally:
        connection.close()


@app.route("/students", methods=["GET"])
def get_students():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students")

            students = cursor.fetchall()

        return jsonify(students)

    finally:
        connection.close()


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM students WHERE id = %s",
                (student_id,)
            )

            student = cursor.fetchone()

        if student is None:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify(student)

    finally:
        connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
