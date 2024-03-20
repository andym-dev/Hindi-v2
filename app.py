from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openpyxl
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(255), nullable=False)
    hindi = db.Column(db.String(255), nullable=False)
    flashcard_type_id = db.Column(db.Integer, db.ForeignKey('flashcard_type.id'), nullable=False)
    marks = db.relationship('Mark', backref='flashcard', lazy=True)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcard.id'), nullable=False)
    date_inserted = db.Column(db.DateTime, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)

class FlashcardType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    flashcards = db.relationship('Flashcard', backref='flashcard_type', lazy=True)

def load_flashcards():
    excel_file = 'Vocabulary.xlsx'
    workbook = openpyxl.load_workbook(excel_file)
    flashcard_types = workbook.sheetnames

    # Load or create flashcard types
    flashcard_type_objects = {}
    for flashcard_type_name in flashcard_types:
        flashcard_type = FlashcardType.query.filter_by(name=flashcard_type_name).first()
        if not flashcard_type:
            flashcard_type = FlashcardType(name=flashcard_type_name)
        flashcard_type_objects[flashcard_type_name] = flashcard_type
    db.session.add_all(flashcard_type_objects.values())
    db.session.commit()

    # Load or create flashcards
    for flashcard_type_name in flashcard_types:
        flashcard_type = flashcard_type_objects[flashcard_type_name]
        df = pd.read_excel(excel_file, sheet_name=flashcard_type_name)
        df.fillna('', inplace=True)  # Replace NaN values with an empty string
        for index, row in df.iterrows():
            flashcard = Flashcard.query.filter_by(english=row['English'], hindi=row['Hindi'], flashcard_type_id=flashcard_type.id).first()
            if not flashcard:
                flashcard = Flashcard(english=row['English'], hindi=row['Hindi'], flashcard_type_id=flashcard_type.id)
                db.session.add(flashcard)
    db.session.commit()



# Routes
@app.route('/')
def index():
    flashcard_types = FlashcardType.query.all()
    return render_template('index.html', flashcard_types=flashcard_types)

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcard_display():
    if request.method == 'POST':
        flashcard_type_id = request.form.get('flashcard_type')
        flashcards = Flashcard.query.filter_by(flashcard_type_id=flashcard_type_id).all()
        return render_template('flashcard_display.html', flashcards=flashcards)
    else:
        return render_template('flashcard_display.html')

if __name__ == '__main__':
    with app.app_context():
        load_flashcards()
    app.run(debug=True)

