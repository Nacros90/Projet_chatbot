# Dictionnaire des réponses du chatbot
reponses = {
    "bonjour": "Bonjour à toi ! Comment puis-je t'aider",
    "wesh": "Wesh mon gaté ! Ça va",
    "salut": "Salut ! Quoi de neuf",
    "aide": "Bien sûr, je peux t'aider. Que cherches-tu à faire ?",
    "merci": "Avec plaisir !",
    "au revoir": "À bientôt !",
    "bye": "Salut à la prochaine !",
}

print("Chatbot : Salut ! Tape 'quit' pour quitter la conversation.")
print("Comment t'appelles-tu ?")
Nom=input("Toi : ").capitalize()  # On met la première lettre en majuscule
print(f"Chatbot : Enchanté de te rencontrer, {Nom} !")

# Boucle principale du chatbot
while True:
    utilisateur = input(f"{Nom} : ").lower()  # On convertit en minuscule pour éviter les problèmes

    if utilisateur == "quit":
        print(f"Chatbot : Bye bye {Nom} !")
        break  # On arrête la boucle

    reponse = None

    # Réponse spéciale pour les salutations
    if "bonjour" in utilisateur or "wesh" in utilisateur or "salut" in utilisateur:
        reponse = reponses.get(utilisateur, "Salut ! Comment ça va ?")  # On utilise get pour éviter l'erreur si la clé n'existe pas
        print(f"Chatbot : {reponse} {Nom} ?")
        continue

    # Chercher une réponse adaptée
    for mot_cle in reponses:
        if mot_cle in utilisateur:
            reponse = reponses[mot_cle].format(Nom=Nom)  # On formate la réponse avec le nom de l'utilisateur
            break

    # Répondre soit avec une réponse connue, soit une réponse par défaut
    if reponse:
        print("Chatbot :", reponse)
    else:
        print(f"Chatbot : Désolé, je n'ai pas compris,{Nom}...")
