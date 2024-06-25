Créer une application Heroku :
heroku create NOM_DE_VOTRE_APPLICATION

Poussez votre conteneur vers Heroku :
heroku container
web -a NOM_DE_VOTRE_APPLICATION

👋 Assurez-vous de spécifier web lorsque votre application est une application web.

Libérez votre conteneur :
heroku container
web -a NOM_DE_VOTRE_APPLICATION

Ouvrez votre application :
heroku open -a NOM_DE_VOTRE_APPLICATION

👋 Si tout a fonctionné correctement, vous devriez voir votre application fonctionner dans votre navigateur !
