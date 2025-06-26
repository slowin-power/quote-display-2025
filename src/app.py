from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cytaty.db'  # Nazwa pliku bazy danych SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definicja modelu Cytatu
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    context = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Quote by {self.author}>'

# Tworzenie bazy danych i dodawanie przykładowych danych
#@app.before_first_request
@app.before_request
def create_tables():
    db.create_all()
    # Dodaj przykładowe cytaty, jeśli baza danych jest pusta
    if not Quote.query.first():
        quote1 = Quote(
            author='Albert Einstein',
            content='Imagination is more important than knowledge.',
            date=datetime.date(1930, 1, 1),
            time=datetime.time(10, 0, 0),
            context='From a letter to a friend.'
        )
        quote2 = Quote(
            author='Marie Curie',
            content='Nothing in life is to be feared, it is only to be understood.',
            date=datetime.date(1920, 5, 15),
            time=datetime.time(14, 30, 0),
            context='During a public speech.'
        )
        quote3 = Quote(
            author='Adam Małysz',
            content='Najważniejsze są skoki, no i żeby dobrze wylądować.',
            date=datetime.date(2005, 3, 10),
            time=datetime.time(11, 45, 0),
            context='Wywiad po zawodach.'
        )
        db.session.add_all([quote1, quote2, quote3])
        db.session.commit()

# Główna trasa - wyświetla wszystkie cytaty
@app.route('/')
def index():
    quotes = Quote.query.all()
    return render_template('index.html', quotes=quotes)

if __name__ == '__main__':
    app.run(debug=True)