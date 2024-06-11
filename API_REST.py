from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/egapro_db'  # Replace with your actual database credentials
db = SQLAlchemy(app)


class EgaProData(db.Model):
    siren = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    adresse = db.Column(db.String(255))
    # Add more columns as needed

@app.route("/egapro", methods=["GET"])
def get_all_data():
    data = EgaProData.query.all()
    if data:
        return jsonify([data.serialize() for data in data]), 200
    else:
        return jsonify({"message": "No data found"}), 404


@app.route("/egapro/<siren>", methods=["GET"])
def get_data_by_siren(siren: int):
    data = EgaProData.query.filter_by(siren=siren).first()
    if data:
        return jsonify(data.serialize()), 200
    else:
        return jsonify({"message": "Data not found for SIREN {}".format(siren)}), 404


@app.route("/egapro", methods=["POST"])
def create_data():
    request_data = request.get_json()
    siren = request_data.get("siren")
    nom = request_data.get("nom")
    adresse = request_data.get("adresse")

    if not siren or not nom or not adresse:
        return jsonify({"message": "Missing required fields"}), 400

    new_data = EgaProData(siren=siren, nom=nom, adresse=adresse)
    db.session.add(new_data)
    db.session.commit()

    return jsonify({"message": "Data created successfully"}), 201


@app.route("/egapro/<siren>", methods=["PUT"])
def update_data(siren: int):
    request_data = request.get_json()
    nom = request_data.get("nom")
    adresse = request_data.get("adresse")

    data = EgaProData.query.filter_by(siren=siren).first()
    if not data:
        return jsonify({"message": "Data not found for SIREN {}".format(siren)}), 404

    data.nom = nom or data.nom
    data.adresse = adresse or data.adresse
    db.session.commit()

    return jsonify({"message": "Data updated successfully"}), 200


@app.route("/egapro/<siren>", methods=["DELETE"])
def delete_data(siren: int):
    data = EgaProData.query.filter_by(siren=siren).first()
    if not data:
        return jsonify({"message": "Data not found for SIREN {}".format(siren)}), 404

    db.session.delete(data)
    db.session.commit()

    return jsonify({"message": "Data deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
