from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  
import os

load_dotenv()

app = Flask(__name__)

# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

# Define a model for your data
class SiteSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    site = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('main.html')


@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        site = request.form['site']
        description = request.form['description']

        # Create a new SiteSuggestion object and add it to the database
        suggestion = SiteSuggestion(name=name, email=email, site=site, description=description)
        db.session.add(suggestion)
        db.session.commit()

        return redirect(url_for('thanks'))

    return render_template('Suggest.html')

@app.route('/thanks')
def thanks():
    return render_template('Thanks.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create sql tables for our data models
    app.run(debug=True)
