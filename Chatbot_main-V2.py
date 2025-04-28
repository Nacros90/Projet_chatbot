class Chatbot:
    def __init__(self):
        self.prenom = ""
        self.reponses = {
            "aide": "Que puis-je faire pour toi, {prenom} ?",
            "merci": "Avec plaisir, {prenom} !",
            "au revoir": "À bientôt, {prenom} !"
        }

    def demander_prenom(self):
        print("Chatbot : Salut ! Comment t'appelles-tu ?")
        self.prenom = input("Toi : ").capitalize()
        print(f"Chatbot : Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation.")

    def obtenir_reponse(self, message):
        message = message.lower()
        
        if "bonjour" in message:
            return f"Bonjour {self.prenom} ! Content de te revoir."

        for mot_cle in self.reponses:
            if mot_cle in message:
                return self.reponses[mot_cle].format(prenom=self.prenom)

        return f"Hmm, je n'ai pas compris, {self.prenom}..."

    def discuter(self):
        while True:
            utilisateur = input(f"{self.prenom} : ")
            if utilisateur.lower() == "quit":
                print(f"Chatbot : Bye bye, {self.prenom} !")
                break

            reponse = self.obtenir_reponse(utilisateur)
            print("Chatbot :", reponse)

# --- Partie principale du programme ---
if __name__ == "__main__":
    bot = Chatbot()
    bot.demander_prenom()
    bot.discuter()
