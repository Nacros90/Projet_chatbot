from google import genai
from google.genai import types # <-- Nouvel import pour la configuration
import os
import time
from dotenv import load_dotenv

class IAClient:
    """
    Client IA robuste avec intégration native du System Prompt.
    """
    def __init__(self, system_instruction=None):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.est_actif = False
        # --- DEBUG ---
        if system_instruction:
            print("[DEBUG] Le cerveau a bien reçu une identité !")
        else:
            print("[DEBUG] ATTENTION : Le cerveau n'a reçu AUCUNE identité (system_instruction est vide).")
        # --------------------------------------------
        if not api_key:
            print("[IA] Clé API manquante dans le fichier .env")
            return

        try:
            self.client = genai.Client(api_key=api_key)
            
            # 1. On prépare la configuration "Système" officielle
            config_ia = None
            if system_instruction:
                config_ia = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7 # Optionnel : Règle la créativité (0.0 = robotique, 1.0 = très créatif)
                )
            
            # 2. On crée le chat en lui injectant la configuration dès le départ
            self.chat_session = self.client.chats.create(
                model="gemini-flash-latest",
                config=config_ia
            )
            
            self.est_actif = True
            print("[IA] Cerveau connecté (Identité chargée avec succès) !")
        except Exception as e:
            print(f"[IA] Erreur critique au démarrage : {e}")

    def generer_reponse(self, message_utilisateur, prenom_utilisateur=""):
        if not self.est_actif:
            return "Désolé, je suis en mode hors-ligne."

        # Plus besoin de répéter l'énorme prompt d'identité à chaque fois !
        # On glisse juste le prénom de l'utilisateur discrètement.
        message_enrichi = f"(Info : L'utilisateur s'appelle {prenom_utilisateur}) {message_utilisateur}"

        tentatives_max = 3
        for i in range(tentatives_max):
            try:
                # Envoi du message allégé
                response = self.chat_session.send_message(message_enrichi)
                return response.text
            except Exception as e:
                if i == tentatives_max - 1:
                    return f"Je n'arrive pas à joindre mes serveurs. Erreur : {e}"
                
                print(f"   (Oups, petit délai réseau... Je réessaie {i+1}/{tentatives_max})")
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