
# Projet Chatbot — Prototype

Ce dépôt contient un prototype de chatbot en console écrit en Python. L'objectif principal est d'avoir une base de conversation simple, capable d'analyser le ton, et d'utiliser une IA externe pour des réponses plus dynamiques.

Le projet intègre l'API **Gemini de Google** pour la génération de réponses lorsque le script ne trouve pas de correspondance prédéfinie.

**État actuel**

Le projet fournit une version console du chatbot (fichiers principaux) :

- `Chatbot_main-V2.py` : Point d'entrée de l'application. Il gère le déroulement de la conversation.
- **Dossier `src/`** : Contient les modules logiques de l'application :
  - `IA_client.py` : Gère la communication avec l'API Gemini de Google.
  - `chat_history.py` : Gère l'historique de la conversation et sa sauvegarde en fichier JSON.
  - `sentiment_analyzer.py` : Analyse le sentiment des messages (basé sur des règles simples). La partie utilisant Transformers est actuellement désactivée.
- `Chatbot_main-V1.py` : Première version du script, conservée pour archive (ancêtre du V2).
- `check_models.py` : Script utilitaire pour vérifier la clé API Gemini et lister les modèles disponibles.
- dossier `historiques/` : stockage des historiques JSON générés lors des sessions.

**Arborescence (simplifiée)**

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
	- Note : L'analyse de sentiment avancée via Transformers est présente dans le code mais désactivée par défaut.

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
