# Définition de la classe Chatbot
class Chatbot:
    def __init__(self):  # Initialisation des attributs de la classe
        self.prenom = ""  # Stocke le prénom de l'utilisateur
        self.reponses = {  # Dictionnaire contenant des réponses prédéfinies
            "aide": "Que puis-je faire pour toi, {prenom} ?",  # Réponse pour le mot-clé "aide"
            "merci": "Avec plaisir, {prenom} !",  # Réponse pour le mot-clé "merci"
            "au revoir": "À bientôt, {prenom} !"  # Réponse pour le mot-clé "au revoir"
        }

    def demander_prenom(self):  # Demande le prénom de l'utilisateur
        print("Chatbot : Salut ! Comment t'appelles-tu ?")
        self.prenom = input("Toi : ").capitalize()  # Récupère et capitalise le prénom
        print(f"Chatbot : Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation.")

    def obtenir_reponse(self, message):  # Analyse le message de l'utilisateur et retourne une réponse appropriée
        message = message.lower()  # Convertit le message en minuscules pour simplifier la recherche
        
        # Vérifie si le message contient "bonjour"
        if "bonjour" in message:
            return f"Bonjour {self.prenom} ! Content de te revoir."

        # Parcourt les mots-clés dans le dictionnaire des réponses
        for mot_cle in self.reponses:
            if mot_cle in message:  # Si un mot-clé est trouvé dans le message
                return self.reponses[mot_cle].format(prenom=self.prenom)  # Retourne la réponse formatée

        # Si aucun mot-clé n'est trouvé, retourne une réponse par défaut
        return f"Hmm, je n'ai pas compris, {self.prenom}..."

    def discuter(self):  # Boucle principale pour interagir avec l'utilisateur
        
        while True:
            utilisateur = input(f"{self.prenom} : ")  # Récupère le message de l'utilisateur
            if utilisateur.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte la boucle
                print(f"Chatbot : Bye bye, {self.prenom} !")
                break

            # Obtient une réponse du chatbot et l'affiche
            reponse = self.obtenir_reponse(utilisateur)
            print("Chatbot :", reponse)

# --- Partie principale du programme ---
if __name__ == "__main__":  # Instancie un objet Chatbot et démarre la conversation
    bot = Chatbot()
    bot.demander_prenom()  # Demande le prénom de l'utilisateur
    bot.discuter()  # Démarre la conversation
