# Utilise l'image de base continuumio/miniconda3
FROM continuumio/miniconda3

# Définit le répertoire de travail à /home/app
WORKDIR /home/app

# Met à jour la liste des paquets apt-get et installe nano, unzip, Python 3.10, et curl
RUN apt-get update -y 
RUN apt-get install nano unzip -y
RUN apt-get install -y python3.10
RUN apt install curl -y

# Installe l'outil de ligne de commande "Deta"
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

# Copie le fichier requirements.txt dans le répertoire /dependencies/ et installe les dépendances Python
COPY requirements.txt /dependencies/requirements.txt
RUN pip --default-timeout=100 install -r /dependencies/requirements.txt

# Copie tout le contenu du répertoire local dans le répertoire de travail de l'image
COPY . /home/app

# Définit la commande à exécuter lorsque le conteneur démarre
CMD gunicorn model_api:app  --bind 0.0.0.0:$PORT --timeout 100 --worker-class uvicorn.workers.UvicornWorker
