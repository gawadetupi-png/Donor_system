from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "donors.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    bloodGroup = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- REGISTER DONOR ----------------
@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    donor = Donor(
        fullName=data['fullName'],
        phone=data['phone'],
        gender=data['gender'],
        bloodGroup=data['bloodGroup'],
        location=data['location']
    )

    db.session.add(donor)
    db.session.commit()

    return jsonify({
    "message": "Registration Successful",
    "name": donor.fullName,
    "donorId": f"ADYF{donor.id:05d}"
})

# ---------------- GET ALL DONORS ----------------
@app.route('/getDonors', methods=['GET'])
def getDonors():

    donors = Donor.query.all()

    result = []

    for d in donors:
        result.append({
            "id": d.id,
            "fullName": d.fullName,
            "phone": d.phone,
            "gender": d.gender,
            "bloodGroup": d.bloodGroup,
            "location": d.location
        })

    return jsonify(result)

# ---------------- SEARCH DONORS ----------------
@app.route("/search")
def search():

    blood = request.args.get("bloodGroup", "").strip()
    city = request.args.get("location", "").strip()

    query = Donor.query

    if blood:
        query = query.filter(Donor.bloodGroup == blood)

    if city:
        query = query.filter(Donor.location.ilike(f"%{city}%"))

    donors = query.all()

    return jsonify([
        {
            "fullName": d.fullName,
            "phone": d.phone,
            "gender": d.gender,
            "bloodGroup": d.bloodGroup,
            "location": d.location
        }
        for d in donors
    ])

# ---------------- MAIN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database created at:", DATABASE_PATH)

    app.run(debug=True)