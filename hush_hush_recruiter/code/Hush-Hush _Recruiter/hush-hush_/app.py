


# Importing all necessary packages

import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
# Configure multiple database connections using SQLAlchemy binds.

app.config['SQLALCHEMY_BINDS'] = {
    'hiring': 'postgresql://postgres:1234@localhost/Hiring_Demands',
    'data': 'sqlite:///C:/Users/patna/Downloads/developers_for_all.db'
}

# Set a secret key for the Flask application to enable session security.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/SPEED FORCE/Downloads/developers_for_all.db'
db = SQLAlchemy(app)

# Giving static credentials
static_credentials = {
    "d.m@gmail.com": "password@dm",
    "h.m@gmail.com": "password@hm",
    "candidate@gmail.com": "password@candidate"
}

# Define 'developer_g' table in the 'data' database. Specify the database bind key for this model. Define the table name.

class DeveloperG(db.Model):
    __bind_key__ = 'data'
    __tablename__ = 'developer_g'

# Define columns for the table.
    username = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255))
    followers = db.Column(db.Integer)
    number_of_repos = db.Column(db.Integer)
    stars = db.Column(db.Integer)
    forks = db.Column(db.Integer)
    pull_number = db.Column(db.Integer)
    unique_id = db.Column(db.String(255))
    predicted_probability = db.Column(db.Float)


# Define 'developer_s' table in the 'data' database. Specify the database bind key for this model. Define the table name.
class DeveloperS(db.Model):
    __bind_key__ = 'data'
    __tablename__ = 'developer_s'

# Define columns for the table.
    display_name = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255))
    reputation = db.Column(db.Integer)
    gold_badges = db.Column(db.Integer)
    silver_badges = db.Column(db.Integer)
    id_number = db.Column(db.String(255))
    predicted_category = db.Column(db.String(255))
    probability_good = db.Column(db.Float)

with app.app_context():
    db.create_all()

# Login Page
@app.route('/')
def login():
    return render_template('login.html')


# Giving static input for login of the dm and hm
@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if request.method == 'POST':
        if username in static_credentials and static_credentials[username] == password:
            session['username'] = username
            if username == 'd.m@gmail.com':
                return redirect(url_for('decision_maker'))
            elif username == 'h.m@gmail.com':
                return redirect(url_for('hiring_manager'))
            else:
                return redirect(url_for('candidate_coding_platform'))
        else:
            return render_template('login.html', error=True)


# Decision maker page for giving requirements
@app.route('/decision_maker', methods=['GET', 'POST'])
def decision_maker():
    if request.method == 'POST':
        developer_count = request.form.get('developer_count', type=int)
        
        connection = db.engines['hiring'].connect()
        
        connection.execute(text("INSERT INTO requirements(number_of_developers) VALUES (:developer_count)"), {"developer_count": developer_count})
        connection.commit()
        
        connection.close()
    return render_template('decision_maker.html')


# Hiring manager page fetches candidates from the database
@app.route('/hiring_manager')
def hiring_manager():
    connection = db.engines['hiring'].connect()
    result = connection.execute(text("SELECT number_of_developers FROM requirements ORDER BY id DESC LIMIT 1"))
    developer_count = result.fetchone()[0] if result else 0
    connection.close()

    developer_g = DeveloperG.query.all()
    developer_s = DeveloperS.query.all()

    return render_template('hiring_manager.html', developer_count=developer_count, developer_g=developer_g, developer_s=developer_s)


# Candidates coding platform  
@app.route('/candidate_coding_platform', methods=['GET', 'POST'])
def candidate_coding_platform():
    if request.method == 'POST':
        name = request.form.get('name', type=str)
        email = request.form.get('email', type=str)
        solution1 = request.form.get('textarea1', type=str)
        solution2 = request.form.get('textarea2', type=str)
        solution3 = request.form.get('textarea3', type=str)
        
        
        connection = db.engines['hiring'].connect()
        
        connection.execute(text("INSERT INTO solution(name, email, solution1, solution2, solution3) VALUES (:name, :email, :solution1, :solution2, :solution3)"), 
                           {'name': name, 'email': email, 'solution1': solution1, 'solution2': solution2, 'solution3': solution3})
        
        connection.commit() 
        
        connection.close()
    return render_template('candidate_coding_platform.html')


# Hiring manager able to see candidate submitted solutions
@app.route('/coding_solutions')
def coding_solutions():
    connection = db.engines['hiring'].connect()
    result = connection.execute(text("SELECT id, name, email, solution1, solution2, solution3 FROM solution"))
    data = result.fetchall()
    connection.close()
    return render_template('coding_solutions.html', data=data)


# Evaluation takes place
@app.route('/Evaluation')
def evaluation():
    result = db.session.execute(text('SELECT * FROM solution')).fetchall()
    return render_template('evaluation.html', result=result)





# After manual evaluation hiring manager pushes data into database
@app.route('/submit_evaluations', methods=['POST'])
def submit_evaluations():
    try:
        connection = db.engines['hiring'].connect()  
        for key, value in request.form.items():
            if key.startswith('selected'):
                id = int(key.replace('selected', ''))
                selected = value == 'Yes'
                score = int(request.form.get(f'score{id}', 0))
                update_query = text("""
                    INSERT INTO final_candidates (id, selected, score) 
                    VALUES (:id, :selected, :score) 
                    ON CONFLICT (id) DO UPDATE 
                    SET selected = :selected, score = :score
                """)
                print(id, selected, score)
                connection.execute(update_query, {'id': id, 'selected': selected, 'score': score})
        connection.close()
        return redirect(url_for('coding_solutions'))  
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return "There was an issue submitting the evaluations", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
