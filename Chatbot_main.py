# Dictionnaire des réponses du chatbot
reponses = {
    "bonjour": "Bonjour à toi ! Comment puis-je t'aider ?",
    "aide": "Bien sûr, je peux t'aider. Que cherches-tu à faire ?",
    "merci": "Avec plaisir !",
    "au revoir": "À bientôt !"
}

print("Chatbot : Salut ! Tape 'quit' pour quitter la conversation.")

# Boucle principale du chatbot
while True:
    utilisateur = input("Toi : ").lower()  # On convertit en minuscule pour éviter les problèmes

    if utilisateur == "quit":
        print("Chatbot : Bye bye !")
        break  # On arrête la boucle

    reponse = None

    # Chercher une réponse adaptée
    for mot_cle in reponses:
        if mot_cle in utilisateur:
            reponse = reponses[mot_cle]
            break

    # Répondre soit avec une réponse connue, soit une réponse par défaut
    if reponse:
        print("Chatbot :", reponse)
    else:
        print("Chatbot : Désolé, je n'ai pas compris...")
