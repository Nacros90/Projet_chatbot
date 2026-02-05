from google import genai
import os
from dotenv import load_dotenv

# Charge la clé
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Erreur : Pas de clé API trouvée dans .env")
else:
    print(f"Clé trouvée, interrogation de Google...")
    try:
        client = genai.Client(api_key=api_key)
        # On demande la liste des modèles qui supportent la génération de contenu
        print("\n--- Modèles disponibles pour ta clé ---")
        found = False
        for m in client.models.list():
            if "generateContent" in m.supported_actions:
                # On nettoie le nom (enlève 'models/')
                model_name = m.name.replace("models/", "")
                print(f"- {model_name}")
                found = True
        
        if not found:
            print("Aucun modèle compatible trouvé. Vérifie tes droits API.")
            
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")