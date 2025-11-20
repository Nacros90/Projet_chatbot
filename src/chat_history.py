from datetime import datetime
from . import Save_logs

class ChatHistory:
    """
    Manages the conversation history, including adding messages and saving them.
    """
    def __init__(self):
        self.history = []

    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_message(self, author, message):
        self.history.append({"timestamp": self._get_timestamp(), "auteur": author, "message": message})

    def save(self, prenom):
        # The original `sauvegarder_historique` function expects an object
        # with a `.historique` attribute. We can create a temporary object
        # to satisfy this requirement without changing Save_logs.py.
        class TempHistoryContainer:
            pass
        
        container = TempHistoryContainer()
        container.historique = self.history # The original code used 'historique'
        container.prenom = prenom
        Save_logs.sauvegarder_historique(container)
