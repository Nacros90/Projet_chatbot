from google import genai
import os
from dotenv import load_dotenv
import time

class IAClient:
    """
    Gère la communication avec l'IA via la nouvelle bibliothèque google-genai.
    """
    def __init__(self, system_instructions=None):
        # Charge les variables du fichier .env
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.est_actif = False

        #On stocke les instructions système pour les envoyer à chaque requête (si besoin)
        self.system_instructions = system_instructions
        
        if not api_key:
            print("[Erreur IA] Clé API non trouvée dans .env")
            self.est_actif = False
            return

        try:
            # Connexion avec la nouvelle syntaxe
            self.client = genai.Client(api_key=api_key)
            # On crée une session de chat pour garder la mémoire
            self.chat_session = self.client.chats.create(model="gemini-flash-latest")
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
            return "Désolé, l'IA est hors ligne pour le moment."
        
        #On combine les instructions système avec le message de l'utilisateur pour donner plus de contexte à l'IA
        contexte_global=""
        # 1. On ajoute l'identité si elle existe
        if self.system_instructions:
            contexte_global += f"{self.system_instructions}\n\n"
        
        # 2. On ajoute le contexte dynamique (Prénom, etc.)
        contexte_global += f"(Info contexte : L'utilisateur s'appelle {prenom_utilisateur}).\n"
        
        # 3. Le message réel
        prompt_final = contexte_global + "Message utilisateur : " + message_utilisateur

        tentatives_max = 3
        for i in range(tentatives_max):
            try:
                # On envoie le tout. L'utilisateur ne voit pas le prompt système, 
                # mais l'IA le reçoit à chaque fois pour rester "dans le personnage".
                response = self.chat_session.send_message(prompt_final)
                return response.text
            except Exception as e:
                if i == tentatives_max - 1:
                    return f"Je n'arrive pas à joindre mes serveurs. Erreur : {e}"
                print(f"   (Oups, délai réseau... Je réessaie {i+1}/{tentatives_max})")
                time.sleep(2)
"""
        try:
            # On ajoute le contexte (prénom) de manière subtile
            contexte = f"(L'utilisateur s'appelle {prenom_utilisateur}). "
            
            # Envoi du message via la nouvelle méthode
            response = self.chat_session.send_message(contexte + message_utilisateur)
            return response.text
        except Exception as e:
            return f"Oups, petite erreur technique : {e}"
"""