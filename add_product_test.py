from connexion import get_connection

conn = get_connection()
cursor = conn.cursor()

sql = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)"
values = ("Clavier Gamer", 59.99, 15)

cursor.execute(sql, values)

conn.commit()
conn.close()

print("Produit ajouté avec succès")