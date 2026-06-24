import sentry_sdk
import os
import os
from flask import Flask, jsonify, request
from flasgger import Swagger
from crud import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)


from logger_config import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

# =========================
# SENTRY INIT
# =========================
sentry_sdk.init(
    dsn="https://465ec9cb7ae79e1a793839d9b0ae29b2@o4511615170510848.ingest.de.sentry.io/4511615216975952",
    traces_sample_rate=1.0,
    environment="development"
)
Swagger(app)

# =========================
# HOME
# =========================
@app.route("/", methods=["GET"])
def home():
    logger.info(f"QUI=127.0.0.1 | QUOI=GET / | ACTION=API démarrée")
    return jsonify({"message": "API opérationnelle"})


# =========================
# GET ALL
# =========================
@app.route("/produits", methods=["GET"])
def get_produits():
    logger.info(f"QUI=127.0.0.1 | QUOI=GET /produits | ACTION=liste produits")
    return jsonify(get_all_products()), 200


# =========================
# GET BY ID
# =========================
@app.route("/produits/<int:id>", methods=["GET"])
def get_product(id):
    logger.debug(f"QUI=127.0.0.1 | QUOI=GET /produits/{id} | ACTION=recherche")

    product = get_product_by_id(id)

    if product:
        logger.info(f"QUI=127.0.0.1 | QUOI=produit {id} | ACTION=trouvé")
        return jsonify(product), 200

    logger.error(f"QUI=127.0.0.1 | QUOI=produit {id} | ACTION=introuvable")
    return jsonify({"error": "Produit introuvable"}), 404


# =========================
# CREATE
# =========================
@app.route("/produits", methods=["POST"])
def add_product():
    data = request.json

    logger.info(f"QUI=127.0.0.1 | QUOI=POST /produits | DATA={data}")

    create_product(data["nom"], data["prix"], data["stock"])

    logger.info("ACTION=produit créé")
    return jsonify({"message": "Produit ajouté"}), 201


# =========================
# UPDATE
# =========================
@app.route("/produits/<int:id>", methods=["PUT"])
def edit_product(id):
    data = request.json

    logger.debug(f"QUI=127.0.0.1 | QUOI=PUT /produits/{id} | ACTION=update")

    update_product(id, data["prix"], data["stock"])

    logger.info(f"QUI=127.0.0.1 | QUOI=produit {id} | ACTION=modifié")
    return jsonify({"message": "Produit modifié"}), 200


# =========================
# DELETE
# =========================
@app.route("/produits/<int:id>", methods=["DELETE"])
def remove_product(id):

    logger.warning(f"QUI=127.0.0.1 | QUOI=DELETE /produits/{id} | ACTION=suppression")

    delete_product(id)

    logger.info(f"QUI=127.0.0.1 | QUOI=produit {id} | ACTION=supprimé")
    return jsonify({"message": "Produit supprimé"}), 200

# =========================
# ERROR TEST
# =========================
#@app.route("/error-test")
#def error_test():
#    1 / 0  # 💥 Sentry capture

@app.route("/error-test")
def error_test():
    return "Erreur corrigée"

# =========================
# RUN
# =========================
if __name__ == "__main__":
    logger.info("SERVEUR DEMARRÉ")
    app.run(debug=True)