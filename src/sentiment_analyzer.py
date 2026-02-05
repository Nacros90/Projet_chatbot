import sys

#On tente d'importer la bibliothèque transformers pour une analyse plus avancée, mais on gère le cas où elle n'est pas installée
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    print("[Avertissement] La bibliothèque 'transformers' n'est pas installée. L'analyse avancée sera désactivée.")
    HAS_TRANSFORMERS = False

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
        #--- MOTEUR 2 : TRANSFORMERS (Optionnel) ---
        self.use_transformers = HAS_TRANSFORMERS
        self.pipe = None
        
        if self.use_transformers:
            print("🚀 [Info] Module Transformers détecté. Chargement du modèle...")
            try:
                # On charge le modèle (peut prendre quelques secondes au premier lancement)
                self.pipe = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
                print("[Info] Analyseur neuronal chargé avec succès.")
            except Exception as e:
                print(f"[Attention] Erreur au chargement de Transformers : {e}")
                print("-> Bascule automatique sur le mode 'Règles simples'.")
                self.use_transformers = False
        else:
            # Ce message s'affichera sur une machine sans la librairie
            print("[Info] Transformers non installé. Mode 'Règles simples' activé uniquement.")
    
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
        """
        Analyse puissante (S'active seulement si self.use_transformers est True).
        """
        if not self.use_transformers or not self.pipe:
            return "Analyse avancée indisponible sur cette machine."

        # On prend le dernier message de l'utilisateur pour l'analyser
        last_message = ""
        # On lit l'historique à l'envers pour trouver la dernière phrase de l'humain
        for entree in reversed(history):
            if entree["auteur"] == "Utilisateur":
                last_message = entree["message"]
                break
        
        if not last_message:
            return "Pas de message récent à analyser."

        try:
            # L'IA analyse le sentiment (retourne des étoiles de 1 à 5)
            # On coupe le message s'il est trop long (limite des modèles BERT)
            result = self.pipe(last_message[:512])[0]
            label = result['label'] # ex: "5 stars"
            score = result['score']
            return f"Analyse neuronale : {label} (Confiance : {score:.2f})"
        except Exception as e:
            return f"Erreur d'analyse : {e}"