from pymongo import MongoClient

# Connexion à MongoDB Atlas (remplace par ton URI)
MONGO_URI = "mongodb+srv://saadanefatima23_db_user:UclliPpSvgCyyte8@cluster0.zqibef2.mongodb.net/?appName=Cluster0"
DB_NAME = "project"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Exemple : Mettre à jour la quantité du dispositif "DM-002" à 200
reference_cible = "DM-002"
nouvelle_quantite = 200

resultat = db["stock"].update_one(
    {"reference": reference_cible},
    {"$set": {"quantite": nouvelle_quantite}}
)

if resultat.modified_count > 0:
    print(f"Succès : La quantité pour {reference_cible} a été mise à jour à {nouvelle_quantite}.")
else:
    print("Aucune modification effectuée (vérifie la référence).")

client.close()