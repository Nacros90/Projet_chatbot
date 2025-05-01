import json
import os
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Définition de la classe Chatbot pour encapsuler le comportement du chatbot
class Chatbot:
    def __init__(self):  # Initialisation des attributs de la classe
        self.prenom = ""  # Stocke le prénom de l'utilisateur
        self.humeur = "neutre"  # Stocke l'humeur du chatbot
        self.historique=[]
        self.sia=SentimentIntensityAnalyzer()  # Instancie l'analyseur de sentiment VADER
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
        self.mots_positifs = ["bien", "super", "génial", "cool","parfait"]  # Liste de mots considérés comme positifs
        self.motifs_positifs = [  # Liste de motifs positifs pour la réponse
            (["je suis","content"],1),
            (["je me sens","bien"],1),
            (["je me sens super","bien"],2),
            (["c'est","super"],2),
            (["c'est","génial"],2),
            (["je suis","heureux"],1)
        ]
        self.motifs_negatifs = [  # Liste de motifs négatifs pour la réponse
            (["je suis","triste"],1),
            (["je me sens","mal"],2),
            (["c'est","nul"],2),
            (["c'est","pourri"],1),
            (["je suis","déçu"],1),
        ]
        self.mots_negation=["pas", "ne", "aucun", "jamais","rien"]  # Liste de mots de négation

    def get_timestamp(self):  # Retourne l'heure actuelle au format "YYYY-MM-DD HH:MM:SS"
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def demander_prenom(self):  # Demande le prénom de l'utilisateur
        print("Chatbot : Salut ! Comment t'appelles-tu ?")
        self.prenom = input("Toi : ").capitalize()  # Récupère et capitalise le prénom
        if self.prenom.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte le programme
            print("Chatbot : Bye bye !")
            exit()
        self.historique.append({
            "timestamp": self.get_timestamp(),
            "auteur": "Chatbot",
            "message":"Salut ! Comment t'appelles-tu ?"
            })
        self.historique.append({
            "timestamp": self.get_timestamp(),
            "auteur": "Utilisateur",
            "message": self.prenom,
            })
        print(f"Chatbot : Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation.")
        self.historique.append({
            "timestamp": self.get_timestamp(),
            "auteur": "Chatbot",
            "message": f"Enchanté, {self.prenom} ! Tape 'quit' pour quitter la conversation."
            })
    
    def analyse_humeur(self, message):  # Analyse le message de l'utilisateur pour déterminer son humeur
        message = message.lower()  # Convertit le message en minuscules pour éviter les problèmes de casse
        for mot in self.mots_mechants:
            if mot in message:
                self.humeur = "enerve"
                return
        if "merci" in message:
            self.humeur = "content"

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
            self.historique.append({  # Enregistre le message de l'utilisateur dans l'historique
                "timestamp": self.get_timestamp(),
                "auteur": "Utilisateur",
                "message": utilisateur
                })

            if utilisateur.lower() == "quit":  # Si l'utilisateur tape "quit", on quitte la boucle
                print(f"Chatbot : Bye bye, {self.prenom} !")
                self.historique.append({
                    "timestamp": self.get_timestamp(),
                    "auteur": "Chatbot",
                    "message": f"Bye bye, {self.prenom} !"
                    })
                break

            # Obtient une réponse du chatbot et l'affiche
            reponse = self.obtenir_reponse(utilisateur)
            print("Chatbot :", reponse)
            self.historique.append({
                "timestamp": self.get_timestamp(),
                "auteur": "Chatbot",
                "message": reponse
                })

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

    def contient_negation(self, message):  # Vérifie si le message contient des mots de négation
        return any(neg in message for neg in self.mots_negation)

    def analyser_conversation(self):  # Analyse l'historique de la conversation pour détecter les messages positifs et négatifs
            positifs = 0
            negatifs = 0

            for entree in self.historique:
                if entree["auteur"] == "Utilisateur":
                    message = entree["message"].lower()
                    negation=self.contient_negation(message)  # Vérifie si le message contient des mots de négation

                    #Vérification simple de mots isolés
                    for mot in self.mots_positifs:
                        if mot in message:
                            if negation:
                                negatifs += 1
                            else:
                                positifs += 1
                    
                    for mot in self.mots_mechants:
                        if mot in message:
                            negatifs += 1

                    #Vérification de motifs complexes avec poids
                    for motif,poids in self.motifs_positifs:  #motifs positifs
                        if all(mot in message for mot in motif):
                            if negation:
                                negatifs += poids
                            else:
                                positifs += poids
                            break #Evite de compter plusieurs fois le même message
                    
                    for motif,poids in self.motifs_negatifs:  #motifs négatifs
                        if all(mot in message for mot in motif):
                            negatifs += poids
                            break

            print("\n--- Analyse de la conversation ---")
            print(f"Messages positifs détectés : {positifs}")
            print(f"Messages négatifs détectés : {negatifs}")

            if positifs > negatifs:
                ton="Conclusion : Conversation globalement POSITIVE"
                print(ton)
            elif negatifs > positifs:
                ton="Conclusion : Conversation plutôt NEGATIVE"
                print(ton)
            else:
                ton="Conclusion : Conversation NEUTRE ou équilibrée"
                print(ton)
                        
            self.historique.append({
                "timestamp": self.get_timestamp(),
                "auteur": "Chatbot",
                "message": ton
                })
    def analyser_conversation_nlp(self):
        score_total = 0
        nb_messages = 0

        for message in self.historique:
            if message["auteur"] == "Utilisateur":
                s = self.sia.polarity_scores(message["message"])
                score_total += s["compound"]
                nb_messages += 1

        if nb_messages == 0:
            ton = "Aucun message à analyser."
        else:
            moyenne = score_total / nb_messages
            if moyenne > 0.3:
                ton = "Ton positif (NLP)"
            elif moyenne < -0.3:
                ton = "Ton négatif (NLP)"
            else:
                ton = "Ton neutre ou incertain (NLP)"

        self.historique.append({
            "auteur": "Bot",
            "message": ton,
            "timestamp": self.get_timestamp()
        })
        self.sauvegarder_historique()
        print(ton)


# --- Partie principale du programme ---
if __name__ == "__main__":  # Instancie un objet Chatbot et démarre la conversation
    bot = Chatbot()
    bot.demander_prenom()  # Demande le prénom de l'utilisateur
    bot.discuter()  # Démarre la conversation
    bot.analyser_conversation()  # Analyse l'historique de la conversation
    bot.analyser_conversation_nlp()  # Analyse l'historique de la conversation avec NLP
    bot.sauvegarder_historique()  # Sauvegarde l'historique de la conversation dans un fichier JSON