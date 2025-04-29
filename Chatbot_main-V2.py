import json
import os

# Définition de la classe Chatbot pour encapsuler le comportement du chatbot
class Chatbot:
    def __init__(self):  # Initialisation des attributs de la classe
        self.prenom = ""  # Stocke le prénom de l'utilisateur
        self.humeur = "neutre"  # Stocke l'humeur du chatbot
        self.historique=[]
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
        self.mots_mechants = ["stupide", "idiot", "nul", "con"]  # Liste de mots considérés comme méchants

    def demander_prenom(self):  # Demande le prénom de l'utilisateur
        print("Chatbot : Salut ! Comment t'appelles-tu ?")
        self.prenom = input("Toi : ").capitalize()  # Récupère et capitalise le prénom
        if self.prenom.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte le programme
            print("Chatbot : Bye bye !")
            exit()
        self.historique.append({"auteur": "Chatbot", "message":"Salut ! Comment t'appelles-tu ?"})
        self.historique.append({"auteur": "Utilisateur", "message": self.prenom})
        print(f"Chatbot : Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation.")
        self.historique.append({"auteur": "Chatbot", "message": f"Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation."})
        # Enregistre l'historique de la conversation dans un fichier JSON
    
    def analyse_humeur(self, message):  # Analyse le message de l'utilisateur pour déterminer son humeur
        message = message.lower()  # Convertit le message en minuscules pour éviter les problèmes de casse
        for mot in self.mots_mechants:
            if mot in message:
                self.humeur = "enerve"
                print(f"Humeur changée à : {self.humeur}")  # Debug
                return
        if "merci" in message:
            self.humeur = "content"
            print(f"Humeur changée à : {self.humeur}")  # Debug

    def obtenir_reponse(self, message):  # Analyse le message de l'utilisateur et retourne une réponse appropriée
        message = message.lower()  # Convertit le message en minuscules pour simplifier la recherche
        self.analyse_humeur(message)  # Analyse l'humeur de l'utilisateur
        
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

        # Si aucun mot-clé n'est trouvé, retourne une réponse par défaut
        return f"Hmm, je n'ai pas compris, {self.prenom}..."

    def discuter(self):  # Boucle principale pour interagir avec l'utilisateur
        while True:
            utilisateur = input(f"{self.prenom} : ")  # Récupère le message de l'utilisateur
            self.historique.append({"auteur": "Utilisateur", "message": utilisateur})  # Enregistre le message de l'utilisateur dans l'historique

            if utilisateur.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte la boucle
                print(f"Chatbot : Bye bye, {self.prenom} !")
                self.historique.append({"auteur": "Chatbot", "message": f"Bye bye, {self.prenom} !"})
                self.sauvegarder_historique()
                break

            # Obtient une réponse du chatbot et l'affiche
            reponse = self.obtenir_reponse(utilisateur)
            print("Chatbot :", reponse)
            self.historique.append({"auteur": "Chatbot", "message": reponse})
    def sauvegarder_historique(self):
        # Change le répertoire courant
        nouveau_repertoire = "E:/Naël/Python/Script/Projet_chatbot/historiques"
        os.makedirs(nouveau_repertoire, exist_ok=True)  # Crée le répertoire s'il n'existe pas
        os.chdir(nouveau_repertoire)  # Change le répertoire courant

        # Sauvegarde l'historique dans le nouveau répertoire
        nom_fichier = f"historique_{self.prenom.lower()}.json"
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            json.dump(self.historique, fichier, ensure_ascii=False, indent=4)
        print(f"\n[Info] Historique de la conversation sauvegardé dans le fichier {os.path.join(nouveau_repertoire, nom_fichier)}.")

# --- Partie principale du programme ---
if __name__ == "__main__":  # Instancie un objet Chatbot et démarre la conversation
    bot = Chatbot()
    bot.demander_prenom()  # Demande le prénom de l'utilisateur
    bot.discuter()  # Démarre la conversation
