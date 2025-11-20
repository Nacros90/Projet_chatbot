
# Projet Chatbot — Prototype

Ce dépôt contient un prototype de chatbot écrit en Python. L'objectif principal est d'avoir une base simple de conversation et d'analyse de ton, puis d'évoluer vers une "vraie IA" :

- intégration d'une API (ex. Gemini) pour la version cloud
- version autonome utilisant un modèle de langage local

**État actuel**

Le projet fournit une version console du chatbot (fichiers principaux) :

- `Chatbot_main-V2.py` : Point d'entrée de l'application. Il gère le déroulement de la conversation.
- **Dossier `src/`** : Contient tous les modules logiques de l'application :
  - `chat_history.py` : Classe responsable de la gestion de l'historique de la conversation.
  - `sentiment_analyzer.py` : Classe qui encapsule toute la logique d'analyse de sentiment (basée sur des règles et via Transformers).
  - `Save_logs.py` : Utilitaire pour sauvegarder l'historique des conversations dans un fichier.
- `Chatbot_main-V1.py` : Première version du script, conservée pour archive (ancêtre du V2).
- dossier `historiques/` : stockage des historiques JSON générés lors des sessions.

**Arborescence (extrait)**

```
Chatbot_main-V2.py
Chatbot_main-V1.py
Save_logs.py
historiques/
README.md
```

**Installation (rapide)**

1. Créez et activez un environnement virtuel (PowerShell) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Installer les dépendances recommandées :

```powershell
pip install -U pip
pip install transformers torch
# Pour GPU et versions spécifiques de PyTorch, suivez les instructions officielles PyTorch
```

Remarque : il est recommandé d'ajouter un fichier `requirements.txt` pour figer les versions. Si vous utilisez CUDA/GPU, installez PyTorch selon la documentation officielle pour Windows.

**Utilisation**

Lancer la version principale :

```powershell
python Chatbot_main-V2.py
```

Comportement attendu : le bot demande votre prénom, puis entre en boucle de conversation. Tapez `quit` pour terminer la session. L'historique est collecté et peut être sauvegardé via la fonction `sauvegarder_historique()` (implémentée dans `Save_logs.py`).

**Logs et historiques**

- Les échanges sont stockés en mémoire pendant la session dans `bot.historique` et peuvent être sauvegardés dans le dossier `historiques/` au format JSON via `Save_logs.sauvegarder_historique`.

**Fonctionnalités implémentées**

- Gestion simple d'humeur (positif / négatif / énervé) à partir de mots-clés et motifs.
- Analyse de conversation basique (comptage de mots positifs/négatifs).
- Pipeline Transformers (`nlptown/bert-base-multilingual-uncased-sentiment`) pour une analyse plus avancée (option GPU si disponible).

**Roadmap / Projets futurs**

1. Intégration d'une API externe (ex. Gemini) :
	- Créer une version qui envoie les messages à une API cloud (authentification, quotas, latence, sécurité).
	- Ajouter gestion des appels asynchrones et file d'attente.

2. Version locale avec LLM :
	- Supporter un modèle de langage local (quantized ou autre) pour exécution hors-ligne.
	- Prendre en charge l'accélération GPU/CPU et la gestion mémoire.

3. Robustification :
	- Ajouter `requirements.txt`, tests unitaires, et exemples de sessions.
	- Améliorer la PNL (tokenization multilingue, meilleure gestion de la négation, contextualisation).

4. Déploiement :
	- Fournir un wrapper HTTP/REST ou une petite API Flask/FastAPI pour accès distant.

**Contribuer**

N'hésitez pas à proposer des améliorations :

- Fonctionnalités (intégration Gemini, modèle local)
- Ajout d'un `requirements.txt` et d'un guide d'installation détaillé
- Tests et gestion des erreurs

Créez une issue ou une pull request pour que nous puissions en discuter.

**Licence**

Licence : à définir (par défaut, demandez au propriétaire du dépôt).

---

Si vous voulez, je peux :

- Générer un `requirements.txt` basé sur les imports actuels.
- Ajouter un exemple minimal d'appel API pour Gemini (squelette).
