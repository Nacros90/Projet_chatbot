class SentimentAnalyzer:
    """
    Analyseur de sentiment simplifié (sans Transformers) pour éviter les bugs.
    """
    def __init__(self):
        # Règles simples
        self.mots_mechants = [
            "stupide", "idiot", "inutile", "déteste", "nul", 
            "mauvais", "horrible", "casse-pieds", "ferme-la"
        ]
        self.mots_gentils = [
            "merci", "super", "bravo", "génial", "cool", 
            "aime", "gentil", "top", "excellent"
        ]

    def analyze_with_rules(self, history):
        """
        Analyse basée sur des règles simples (comptage de mots).
        """
        score = 0
        details = []

        # CORRECTION ICI : On parcourt la liste des dictionnaires
        for entree in history:
            # On vérifie que c'est bien l'utilisateur qui parle
            if entree["auteur"] == "Utilisateur":
                message_lower = entree["message"].lower()
                
                # Vérification des mots méchants
                for mot in self.mots_mechants:
                    if mot in message_lower:
                        score -= 1
                
                # Vérification des mots gentils
                for mot in self.mots_gentils:
                    if mot in message_lower:
                        score += 1

        if score > 0:
            return "Conclusion : L'utilisateur semble content."
        elif score < 0:
            return "Conclusion : L'utilisateur semble énervé."
        else:
            return "Conclusion : L'humeur est neutre."

    def analyze_with_transformers(self, history):
        return "Analyse avancée désactivée."