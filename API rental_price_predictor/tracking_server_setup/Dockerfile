# Utilise l'image de base continuumio/miniconda3
FROM continuumio/miniconda3

# Définit le répertoire de travail à /home/app
WORKDIR /home/app

# Met à jour la liste des paquets apt-get et installe nano, unzip, et curl
RUN apt-get update
RUN apt-get install nano unzip -y
RUN apt install curl -y

# Installe l'outil de ligne de commande Deta
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

# Télécharge, décompresse et installe l'AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Copie le fichier requirements.txt et installe les dépendances Python
COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Définit la commande à exécuter lorsque le conteneur démarre, pour démarrer le serveur MLflow
CMD mlflow server \ 
    -p $PORT \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \ 
    --default-artifact-root $ARTIFACT_ROOT
