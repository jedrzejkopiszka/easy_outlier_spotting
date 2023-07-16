import sqlite3
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class CheckBox(db.Model):
    __tablename__ = "checkboxes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    checkboxes = CheckBox.query.first()
    if checkboxes is None:
        for i in range(1, 11):
            checkbox = CheckBox(name=f'checkbox_{i}', state=False)
            db.session.add(checkbox)
        db.session.commit()

    checkboxes = CheckBox.query.all()
    return render_template('index.html', checkboxes=checkboxes)

@app.route('/update', methods=['POST'])
def update():
    checkbox_name = request.json.get('checkbox_name')
    checkbox_state = request.json.get('checkbox_state', False)
    checkbox = CheckBox.query.filter_by(name=checkbox_name).first()
    checkbox.state = checkbox_state
    db.session.commit()

    checkboxes = CheckBox.query.all()
    conn = sqlite3.connect('/tmp/test.db')
    query = "SELECT * FROM {}".format(CheckBox.__tablename__)
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)
    return "success"

if __name__ == "__main__":
    app.run(debug=True, port=500)

