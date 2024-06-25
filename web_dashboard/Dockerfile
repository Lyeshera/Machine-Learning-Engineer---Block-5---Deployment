# Utilise l'image de base Miniconda
FROM continuumio/miniconda3

# Définit le répertoire de travail de l'application
WORKDIR /home/app

# Copie le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /home/app/

# Installe les paquets nécessaires spécifiés dans requirements.txt sans utiliser le cache pour économiser de l'espace
RUN pip install --no-cache-dir -r requirements.txt

# Met à jour la liste des paquets disponibles et installe nano, unzip et curl
RUN apt-get update && \
    apt-get install -y nano unzip && \
    apt install curl -y

# Installe l'outil de ligne de commande Deta
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

# Copie tous les fichiers de l'application dans le répertoire de travail du conteneur
COPY . /home/app

# Définit la commande par défaut à exécuter lorsque le conteneur démarre : lance l'application Streamlit sur le port 8502 et écoute sur toutes les interfaces réseau
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
