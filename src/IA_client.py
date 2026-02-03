from google import genai
import os
from dotenv import load_dotenv

class IAClient:
    """
    Gère la communication avec l'IA via la nouvelle bibliothèque google-genai.
    """
    def __init__(self):
        # Charge les variables du fichier .env
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("[Erreur IA] Clé API non trouvée dans .env")
            self.est_actif = False
            return

        try:
            # Connexion avec la nouvelle syntaxe
            self.client = genai.Client(api_key=api_key)
            
            # On crée une session de chat pour garder la mémoire
            self.chat_session = self.client.chats.create(model="gemini-1.5-flash")
            
            self.est_actif = True
            print("[IA] Cerveau connecté (Nouvelle version) !")
        except Exception as e:
            print(f"[Erreur IA] Impossible de démarrer : {e}")
            self.est_actif = False

    def generer_reponse(self, message_utilisateur, prenom_utilisateur=""):
        """
        Envoie le message à l'IA et récupère la réponse.
        """
        if not self.est_actif:
            return "Désolé, mon cerveau est déconnecté."

        try:
            # On ajoute le contexte (prénom) de manière subtile
            contexte = f"(L'utilisateur s'appelle {prenom_utilisateur}). "
            
            # Envoi du message via la nouvelle méthode
            response = self.chat_session.send_message(contexte + message_utilisateur)
            return response.text
        except Exception as e:
            return f"Oups, petite erreur technique : {e}"