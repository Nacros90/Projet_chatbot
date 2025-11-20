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
        # Call the modernized save function directly with the history list and the user's name.
        Save_logs.sauvegarder_historique(self.history, prenom)
