# Ce script configure/met à jour les variables de configuration de chaque application Heroku
APP_NAME="car-rental-price-mlflow"

# Met à jour l'emplacement du dossier des artefacts sur S3
if [[ ( ! $ARTIFACT_ROOT = $(heroku config:get ARTIFACT_ROOT -a ${APP_NAME}) ) && ( ! -z "$ARTIFACT_ROOT" ) ]]
then
    heroku config:set ARTIFACT_ROOT=$ARTIFACT_ROOT -a $APP_NAME
fi

# AWS credentials
if [[ ( ! $AWS_ACCESS_KEY_ID = $(heroku config:get AWS_ACCESS_KEY_ID -a ${APP_NAME}) ) && ( ! -z "$AWS_ACCESS_KEY_ID" ) ]]
then
    heroku config:set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -a $APP_NAME
fi
if [[ ( ! $AWS_SECRET_ACCESS_KEY = $(heroku config:get AWS_SECRET_ACCESS_KEY -a ${APP_NAME}) ) && ( ! -z "$AWS_SECRET_ACCESS_KEY" ) ]]
then
    heroku config:set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -a $APP_NAME
fi

# Récupère DATABASE_URL des variables de configuration et remplace 'postgres' par 'postgresql' 
# pour qu'il soit une URI BACKEND_STORE valide pour mlflow (voir https://docs.sqlalchemy.org/en/14/core/engines.html#postgresql)
DATABASE_URL_POSTGRESQL=$(heroku config:get DATABASE_URL -a ${APP_NAME} | sed 's/postgres/postgresql/')
BACKEND_STORE_URI=$(heroku config:get BACKEND_STORE_URI -a ${APP_NAME})
if [ ! "$BACKEND_STORE_URI" = $DATABASE_URL_POSTGRESQL ]
then
    heroku config:set BACKEND_STORE_URI=$DATABASE_URL_POSTGRESQL -a $APP_NAME
fi