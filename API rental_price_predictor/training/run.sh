# Exécute le job d'entraînement :
docker run -it\
 # Monte le répertoire courant sur le conteneur à /home/app
 -v "$(pwd):/home/app"\
 # Passe l'URI de suivi MLflow en tant que variable d'environnement dans le conteneur
 -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI\
 # Passe la clé d'accès AWS en tant que variable d'environnement dans le conteneur
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 # Passe la clé secrète AWS en tant que variable d'environnement dans le conteneur
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 # Spécifie l'image Docker à utiliser pour le conteneur
 getaround-mlflow-training \
 # Commande à exécuter dans le conteneur : exécute le script d'entraînement avec Python
 python train.py "$@"
