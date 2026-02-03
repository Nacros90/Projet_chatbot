import google.generativeai as genai
import os
from dotenv import load_dotenv

class IAClient:
    """
    Gère la communication avec le modèle de langage (LLM) Gemini.
    """
    def __init__(self):
        #Chargement de la clé API depuis les variables d'environnement
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("[Erreur IA] Clé API Gemini non trouvée dans les variables d'environnement. Vérifiez votre fichier .env.")
            self.est_actif = False
            return
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.chat_session = self.model.start_chat(history=[])
            self.est_actif = True
            print("[Info IA] Connexion à l'IA Gemini réussie.")
        except Exception as e:
            print(f"[Erreur IA] Impossible de démarrer l'IA : {e}")
            self.est_actif = False

    def generer_reponse(self, message_utilisateur, prenom_utilisateur=""):
        """
        Envoie le message à l'IA et récupère la réponse.
        """
        if not self.est_actif:
            return "Désolé, mon cerveau d'IA n'est pas connecté."

        try:
            # On peut ajouter du contexte pour que l'IA sache à qui elle parle
            contexte = f"(L'utilisateur s'appelle {prenom_utilisateur}). "
            
            # Envoi du message
            response = self.chat_session.send_message(contexte + message_utilisateur)
            return response.text
        except Exception as e:
            return f"Oups, j'ai eu un mal de tête (Erreur API) : {e}"