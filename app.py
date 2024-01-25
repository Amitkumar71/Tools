from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  
from flask_migrate import Migrate
import os

load_dotenv()

app = Flask(__name__)

# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Model
class SiteSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    site = db.Column(db.String(200), nullable=False)
    type=db.Column(db.String(50),nullable=False)
    link=db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))

    def __str__(self) -> str:
        return f'{self.email} - {self.site} - {self.type} - {self.link} - {self.description} - {self.image_path}'

@app.route('/')

def home():
    return render_template('main.html')


@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    if request.method == 'POST':
        email = request.form['email']
        site = request.form['site']
        description = request.form['description']
        type=request.form['type']
        link=request.form['link']
        image_path = request.form['image_path']

        # Creates a new SiteSuggestion object and add it to the database
        suggestion = SiteSuggestion(type=type, email=email, site=site, description=description, image_path=image_path,link=link)
        db.session.add(suggestion)
        db.session.commit()

        return redirect(url_for('thanks'))

    return render_template('Suggest.html')

@app.route('/images')
def image():
    data=SiteSuggestion.query.filter(SiteSuggestion.type=="image").all()

    return render_template('Images.html',data=data)

@app.route('/thanks')
def thanks():
    return render_template('Thanks.html')

def start_app():
    with app.app_context():
        db.create_all()  
    # app.run(debug=True)
    # return app

@app.route('/video')
def video():
    data=SiteSuggestion.query.filter(SiteSuggestion.type =='video').all()
    return render_template('Video.html',data=data)

@app.route('/ai')
def ai():
    data=SiteSuggestion.query.filter(SiteSuggestion.type =='AI').all()
    return render_template('AI.html',data=data)

@app.route('/test')
def test():
    return render_template('test.html')