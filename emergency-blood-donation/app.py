from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///donors.db"

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
@app.route("/")
def home():
    return render_template("index.html")
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
    print("Database tables created successfully")
    app.run(debug=True)
