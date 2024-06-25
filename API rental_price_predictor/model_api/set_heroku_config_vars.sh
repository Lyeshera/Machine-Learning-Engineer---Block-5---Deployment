# Ce script configure et met à jour chacune des variables de configuration de l'application Heroku

APP_NAME="car-rental-price-api"

# AWS credentials
if [[ ( ! $AWS_ACCESS_KEY_ID = $(heroku config:get AWS_ACCESS_KEY_ID -a ${APP_NAME}) ) && ( ! -z "$AWS_ACCESS_KEY_ID" ) ]]
then
    heroku config:set AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -a $APP_NAME
fi
if [[ ( ! $AWS_SECRET_ACCESS_KEY = $(heroku config:get AWS_SECRET_ACCESS_KEY -a ${APP_NAME}) ) && ( ! -z "$AWS_SECRET_ACCESS_KEY" ) ]]
then
    heroku config:set AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -a $APP_NAME
fi

# MLFlow tracking server URI
if [[ ( ! $MLFLOW_TRACKING_URI = $(heroku config:get MLFLOW_TRACKING_URI -a ${APP_NAME}) ) && ( ! -z "$MLFLOW_TRACKING_URI" ) ]]
then
    heroku config:set MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI -a $APP_NAME
fi