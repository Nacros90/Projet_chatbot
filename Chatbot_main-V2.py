from src.chat_history import ChatHistory
from src.sentiment_analyzer import SentimentAnalyzer
from src.IA_client import IAClient
from src.bot_identity import identity_prompt
import sys

# Définition de la classe Chatbot pour encapsuler le comportement du chatbot
class Chatbot:
    def __init__(self):  # Initialisation des attributs de la classe
        self.prenom = ""  # Stocke le prénom de l'utilisateur
        self.humeur = "neutre"  # Stocke l'humeur du chatbot
        self.history = ChatHistory()
        self.analyzer = SentimentAnalyzer()

        print("Initialisation de l'identité du chatbot...")
        self.ia_brain = IAClient(system_instructions=identity_prompt)  # On passe les instructions système à l'IA
        
        #Initialisation de l'IA
        print("Initialisation du système IA...")
        self.ia_brain = IAClient()

        self.reponses = {  # Dictionnaire contenant des réponses prédéfinies et leurs variations selon l'humeur
            "aide": {
                "neutre" : "Que puis-je faire pour toi, {prenom} ?",
                "content" : "Je suis là pour t'aider, {prenom}, dis-moi ce que je peut faire pour toi.",
                "enerve": "Qu'est-ce que tu veux encore ..."
            },
            "merci": {
                "neutre": "Avec plaisir, {prenom} !",
                "content": "Oh, merci à toi aussi {prenom} ! Ça me fait plaisir !",
                "enerve": "Ouais ouais, pas besoin d'en faire des tonnes..."
            },
            "au revoir" : {
                "neutre": "À bientôt, {prenom} !",
                "content": "Reviens vite me parler {prenom} !",
                "enerve": "Enfin ! J'allais m'endormir..."
            },
            "salut": {
                "neutre": "Salut {prenom} !",
                "content": "Salut {prenom} ! Comment ça va ?",
                "enerve": "Qu'est-ce que tu veux encore ?"
            },
        }

    def demander_prenom(self):  # Demande le prénom de l'utilisateur
        prompt = "Chatbot : Salut ! Comment t'appelles-tu ?"
        print(prompt)
        self.history.add_message("Chatbot", prompt)
        self.prenom = input("Toi : ").capitalize()  # Récupère et capitalise le prénom
        if not self.prenom:
            self.prenom = "Utilisateur"  # Valeur par défaut si aucun prénom n'est donné
        if self.prenom.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte le programme
            print("Chatbot : Bye bye !")
            sys.exit()
        
        self.history.add_message("Utilisateur", self.prenom)
        welcome_message = f"Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation."
        print(f"Chatbot : {welcome_message}")
        self.history.add_message("Chatbot", welcome_message)
    
    def analyse_humeur(self, message):  # Analyse le message de l'utilisateur pour déterminer son humeur
        message = message.lower()  # Convertit le message en minuscules pour éviter les problèmes de casse
        for mot in self.analyzer.mots_mechants:
            if mot in message:
                self.humeur = "enerve"
                return
        if "merci" in message:
            self.humeur = "content"

    def obtenir_reponse(self, message):  # Analyse le message de l'utilisateur et retourne une réponse appropriée
        message = message.lower()  # Convertit le message en minuscules pour simplifier la recherche
        self.analyse_humeur(message)  # Analyse l'humeur de l'utilisateur
        
        #1. Réponse scriptée proiritaire
        # Vérifie si le message contient "bonjour"
        if "bonjour" in message:
            salutation={
                "neutre":f"Bonjour {self.prenom} !",
                "content":f"Hello {self.prenom} ! Très content de te voir !",
                "enerve":f"Qu'est-ce que tu veux encore {self.prenom} ?"
            }
            return salutation[self.humeur]  # Retourne la salutation appropriée selon l'humeur

        # Parcourt les mots-clés dans le dictionnaire des réponses
        for mot_cle in self.reponses:
            if mot_cle in message:  # Si un mot-clé est trouvé dans le message
                return self.reponses[mot_cle][self.humeur].format(prenom=self.prenom)  # Retourne la réponse formatée selon l'humeur

        # Si aucun mot-clé n'est trouvé, on utilise l'IA pour générer une réponse
        print(">>> Soumission de la requête à l'IA...")
        return self.ia_brain.generer_reponse(message, self.prenom)

    def discuter(self):  # Boucle principale pour interagir avec l'utilisateur
        while True:
            utilisateur = input(f"{self.prenom} : ")  # Récupère le message de l'utilisateur
            self.history.add_message("Utilisateur", utilisateur)

            if utilisateur.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte la boucle
                farewell_message = f"Bye bye, {self.prenom} !"
                print(f"Chatbot : {farewell_message}")
                self.history.add_message("Chatbot", farewell_message)
                break

            # Obtient une réponse du chatbot et l'affiche
            reponse = self.obtenir_reponse(utilisateur)
            print("Chatbot :", reponse)
            self.history.add_message("Chatbot", reponse)

    def final_analysis(self):
        print("\n--- Analyse de la conversation (Règles) ---")
        rule_analysis = self.analyzer.analyze_with_rules(self.history.history)
        print(rule_analysis)
        self.history.add_message("Analyse_conv_regles", rule_analysis)

        # Optionnel : On peut désactiver l'analyse Transformers si trop lent ou lourd
        if self.analyzer.use_transformers:
            print("   (Lancement de l'analyse neuronale...)")
            neural = self.analyzer.analyze_with_transformers(self.history.history)
            print(f"2. Analyse Neuronale (IA Locale) : {neural}")
        else:
            print("2. Analyse Neuronale : Non disponible (Module non installé).")

        self.history.save(self.prenom)

# --- Partie principale du programme ---
if __name__ == "__main__":  # Instancie un objet Chatbot et démarre la conversation
    bot = Chatbot()
    bot.demander_prenom()  # Demande le prénom de l'utilisateur
    bot.discuter()  # Démarre la conversation
    bot.final_analysis()