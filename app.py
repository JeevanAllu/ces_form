from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "secret123"  # For flash messages

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="ces_database",
            user="postgres",
            password="Jeeva@2512"  # Replace with your PostgreSQL password
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Render the form
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Fetching form data
            name = request.form.get('name')
            college = request.form.get('college')
            phone = request.form.get('phone')
            email = request.form.get('email')
            username = request.form.get('username')
            semester = request.form.get('semester')
            course_types = request.form.getlist('course_types')
            course_types_str = ', '.join(course_types)
            evaluation_type = request.form.get('evaluation_type')
            survey_start_date = request.form.get('survey_start_date')
            survey_end_date = request.form.get('survey_end_date')
            course_list = request.form.get('course_list')
            messaging_designee_name = request.form.get('messaging_designee_name')
            messaging_designee_email = request.form.get('messaging_designee_email')
            custom_message = request.form.get('custom_message', '')
            additional_information = request.form.get('additional_information', '')
            canvas_users_email = 'on' if request.form.get('canvas_users_email') else 'off'

            # Database connection
            conn = get_db_connection()
            if conn is None:
                flash('Failed to connect to the database', 'error')
                return redirect(url_for('index'))
            cur = conn.cursor()

            # Insert data into table
            cur.execute("""
                INSERT INTO ces_evaluations (
                    name, college, phone, email, username, semester,
                    course_types, evaluation_type, survey_start_date,
                    survey_end_date, course_list, messaging_designee_name,
                    messaging_designee_email, custom_message,
                    additional_information, canvas_users_email
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                name, college, phone, email, username, semester,
                course_types_str, evaluation_type, survey_start_date,
                survey_end_date, course_list, messaging_designee_name,
                messaging_designee_email, custom_message,
                additional_information, canvas_users_email
            ))

            conn.commit()
            cur.close()
            conn.close()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
            return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
