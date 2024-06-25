# Utilise l'image de base Miniconda
FROM continuumio/miniconda3

# Définit le répertoire de travail de l'application
WORKDIR /home/app

# Met à jour la liste des paquets disponibles et installe nano, unzip et curl
RUN apt-get update && \
    apt-get install -y nano unzip curl

# Installe l'outil de ligne de commande Deta
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

# Télécharge, décompresse et installe l'outil de ligne de commande AWS
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Copie le fichier requirements.txt et installe les dépendances Python spécifiées
COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

# Définit la commande à exécuter lorsque le conteneur démarre
CMD mlflow server \ 
    -p $PORT \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_ROOT
