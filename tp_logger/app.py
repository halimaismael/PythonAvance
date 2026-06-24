
from flask import Flask, jsonify, request
from flasgger import Swagger

from crud import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)

app = Flask(__name__)
from logger_config import get_logger

logger = get_logger(__name__)
# =========================
# SWAGGER CONFIG PROPRE
# =========================
app.config['SWAGGER'] = {
    'title': 'API Produits',
    'uiversion': 3
}

Swagger(app)


# =========================
# HOME (test API)
# =========================
@app.route("/")
def home():
    return jsonify({"message": "API opérationnelle"})


# =========================
# GET ALL
# =========================
@app.route("/produits", methods=["GET"])
def get_produits():
    """
    Liste des produits
    ---
    responses:
      200:
        description: Retourne tous les produits
    """
    return jsonify(get_all_products()), 200


# =========================
# GET BY ID
# =========================
@app.route("/produits/<int:id>", methods=["GET"])
def get_product(id):
    """
    Récupérer un produit par ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Produit trouvé
      404:
        description: Produit introuvable
    """
    product = get_product_by_id(id)

    if product:
        return jsonify(product), 200

    return jsonify({"error": "Produit introuvable"}), 404


# =========================
# CREATE
# =========================
@app.route("/produits", methods=["POST"])
def add_product():
    """
    Ajouter un produit
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nom:
              type: string
            prix:
              type: number
            stock:
              type: integer
    responses:
      201:
        description: Produit ajouté
    """
    data = request.json

    create_product(
        data["nom"],
        data["prix"],
        data["stock"]
    )

    return jsonify({"message": "Produit ajouté"}), 201


# =========================
# UPDATE
# =========================
@app.route("/produits/<int:id>", methods=["PUT"])
def edit_product(id):
    """
    Modifier un produit
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            prix:
              type: number
            stock:
              type: integer
    responses:
      200:
        description: Produit modifié
    """
    data = request.json

    update_product(
        id,
        data["prix"],
        data["stock"]
    )

    return jsonify({"message": "Produit modifié"}), 200


# =========================
# DELETE
# =========================
@app.route("/produits/<int:id>", methods=["DELETE"])
def remove_product(id):
    """
    Supprimer un produit
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Produit supprimé
    """
    delete_product(id)

    return jsonify({"message": "Produit supprimé"}), 200

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)