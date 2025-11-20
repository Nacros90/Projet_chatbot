from transformers import pipeline
import torch

class SentimentAnalyzer:
    """
    A class to analyze the sentiment of a conversation using different methods.
    """
    def __init__(self):
        # Rule-based analysis resources
        self.mots_mechants = ["stupide", "idiot", "nul", "con"]
        self.mots_positifs = ["bien", "super", "génial", "cool", "parfait"]
        self.motifs_positifs = [
            (["je suis", "content"], 1), (["je me sens", "bien"], 1),
            (["je me sens super", "bien"], 2), (["c'est", "super"], 2),
            (["c'est", "génial"], 2), (["je suis", "heureux"], 1)
        ]
        self.motifs_negatifs = [
            (["je suis", "triste"], 1), (["je me sens", "mal"], 2),
            (["c'est", "nul"], 2), (["c'est", "pourri"], 1),
            (["je suis", "déçu"], 1),
        ]
        self.mots_negation = ["pas", "ne", "aucun", "jamais", "rien"]

        # Transformers-based analysis resources
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            device=0 if torch.cuda.is_available() else -1
        )

    def _contient_negation(self, message):
        return any(neg in message for neg in self.mots_negation)

    def analyze_with_rules(self, history):
        positifs = 0
        negatifs = 0

        for entree in history:
            if entree["auteur"] == "Utilisateur":
                message = entree["message"].lower()
                negation = self._contient_negation(message)

                for mot in self.mots_positifs:
                    if mot in message:
                        negatifs += 1 if negation else -1
                        positifs += 0 if negation else 1
                
                for mot in self.mots_mechants:
                    if mot in message:
                        negatifs += 1

                for motif, poids in self.motifs_positifs:
                    if all(mot in message for mot in motif):
                        negatifs += poids if negation else 0
                        positifs += 0 if negation else poids
                        break
                
                for motif, poids in self.motifs_negatifs:
                    if all(mot in message for mot in motif):
                        negatifs += poids
                        break
        
        if positifs > negatifs:
            return "Conclusion : Conversation globalement POSITIVE"
        elif negatifs > positifs:
            return "Conclusion : Conversation plutôt NEGATIVE"
        else:
            return "Conclusion : Conversation NEUTRE ou équilibrée"

    def analyze_with_transformers(self, history):
        user_messages = [m["message"] for m in history if m["auteur"] == "Utilisateur"]
        if not user_messages:
            return "Aucun message utilisateur à analyser."

        results = self.sentiment_pipeline(user_messages)
        scores = [int(res["label"][0]) for res in results]
        moyenne = sum(scores) / len(scores)

        if moyenne >= 4:
            return "Ton globalement positif (Transformers)"
        elif moyenne <= 2:
            return "Ton globalement négatif (Transformers)"
        else:
            return "Ton globalement neutre ou incertain (Transformers)"

''' #Analyse l'historique de la conversation avec Flair
    def analyser_conversation_flair(self):  # Analyse l'historique de la conversation avec Flair
        pos_count, neg_count = 0, 0
        nb_messages = 0

        for message in self.historique:
            if message["auteur"] == "Utilisateur":
                sentence = Sentence(message["message"])
                self.classifier.predict(sentence)
                label = sentence.labels[0].value  # Récupère le label de sentiment
                if label == "POSITIVE":
                    pos_count += 1
                elif label == "NEGATIVE":
                    neg_count += 1
                nb_messages += 1
        
        if nb_messages == 0:
            ton = "Aucun message à analyser."
        else:
            if pos_count/nb_messages > 0.6:
                ton = "Ton positif (Flair)"
            elif neg_count/nb_messages > 0.6:
                ton = "Ton négatif (Flair)"
            else:
                ton = "Ton neutre ou incertain (Flair)"
        
        self.historique.append({
            "timestamp": self.get_timestamp(),
            "auteur": "Bot",
            "message": ton,
            })
        self.sauvegarder_historique()
        print(ton)
'''
''' #Analyse l'historique de la conversation avec NLP (VADER)
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
        self.sauvegarder_historique()   #Je pense que cette ligne n'est pas nécessaire ici, mais je la laisse pour l'instant
        print(ton)
'''
''' #Analyse l'historique de la conversation avec TextBlob
    def analyser_conversation_textblob(self):
        score_total = 0
        nb_messages = 0

        for message in self.historique:
            if message["auteur"] == "Utilisateur":
                blob = self.tb(message["message"])
                score_total += blob.sentiment[0]  # Utilise TextBlob pour obtenir le score de sentiment
                nb_messages += 1
        
        if nb_messages == 0:
            ton = "Aucun message à analyser."
        else:
            moyenne = score_total / nb_messages
            if moyenne > 0.3:
                ton = "Ton positif (TextBlob)"
            elif moyenne < -0.3:
                ton = "Ton négatif (TextBlob)"
            else:
                ton = "Ton neutre ou incertain (TextBlob)"
        
        self.historique.append({
            "timestamp": self.get_timestamp(),
            "auteur": "Bot",
            "message": ton,
            })
        self.sauvegarder_historique()
        print(ton)
'''
