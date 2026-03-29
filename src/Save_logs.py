import os
import json
from datetime import datetime

def sauvegarder_historique(historique, prenom):
    """
    Sauvegarde une liste d'historique de conversation dans un fichier JSON.

    Args:
        historique (list): La liste des messages de la conversation.
        prenom (str): Le prénom de l'utilisateur.
    """
    try:
        # Le dossier de sauvegarde (à la racine du projet)
        dossier = "historiques"
        
        # On crée le dossier s'il n'existe pas déjà
        if not os.path.exists(dossier):
            os.makedirs(dossier)

        # On crée un nom de fichier unique avec la date et l'heure
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"historique_{prenom.lower()}_{date_str}.json"
        chemin_fichier = os.path.join(dossier, nom_fichier)

        # On écrit les données dans le fichier JSON
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            json.dump(historique, f, ensure_ascii=False, indent=4)
            
        print(f"[Info] Historique sauvegardé dans {chemin_fichier}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'historique : {e}")