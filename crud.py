from connexion import get_connection

# READ ALL
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nom, prix, stock FROM produits")
    rows = cursor.fetchall()

    conn.close()

    # 🔥 transformation en JSON propre
    products = []
    for r in rows:
        products.append({
            "id": r[0],
            "nom": r[1],
            "prix": float(r[2]),
            "stock": r[3]
        })

    return products


# CREATE
def create_product(nom, prix, stock):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nom, prix, stock))

    conn.commit()
    conn.close()


# UPDATE
def update_product(id, prix, stock):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "UPDATE produits SET prix=%s, stock=%s WHERE id=%s"
    cursor.execute(sql, (prix, stock, id))

    conn.commit()
    conn.close()



def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nom, prix, stock FROM produits WHERE id=%s",
        (product_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "nom": row[1],
            "prix": float(row[2]),
            "stock": row[3]
        }

    return None

# DELETE
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM produits WHERE id=%s", (id,))

    conn.commit()
    conn.close()