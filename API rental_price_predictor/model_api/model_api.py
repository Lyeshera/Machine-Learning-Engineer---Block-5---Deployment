import gc
import mlflow
import uvicorn
import numpy as np
import pandas as pd
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse

# Description de l'API pour la documentation automatique
description = """
API de prédiction des prix de location

Soumettez les caractéristiques de votre voiture et un modèle de Machine Learning, entraîné sur les données de GetAround, vous recommandera un prix par jour pour votre location.

Utilisez l'endpoint /predict pour estimer le prix de location quotidien de votre voiture !
"""

# Métadonnées pour la documentation des endpoints
tags_metadata = [
    {
        "name": "Predictions",
        "description": "Utilisez ce endpoint pour obtenir vos predictions"
    }
]

# Initialisation de l'application FastAPI avec titre, description, version et métadonnées
app = FastAPI(
    title="Prédicteur de prix de location de voitures",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

# Modèle de données pour les caractéristiques des voitures
class Car(BaseModel):
    model_key: Literal['Citroën','Peugeot','PGO','Renault','Audi','BMW','Mercedes','Opel','Volkswagen','Ferrari','Mitsubishi','Nissan','SEAT','Subaru','Toyota','other']
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: Literal['diesel','petrol','other']
    paint_color: Literal['black','grey','white','red','silver','blue','beige','brown','other']
    car_type: Literal['convertible','coupe','estate','hatchback','sedan','subcompact','suv','van']
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

# Redirige automatiquement vers /docs (sans afficher cet endpoint dans /docs)
@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

# Endpoint pour faire des prédictions
@app.post("/predict", tags=["Predictions"])
async def predict(cars: List[Car]):
    # Nettoie la mémoire inutilisée
    gc.collect(generation=2)

    # Lit les données d'entrée
    car_features = pd.DataFrame(jsonable_encoder(cars))

    # Charge le modèle en tant que PyFuncModel
    logged_model = 'runs:/7c8aca679d5d4aa395b7be5806197840/car_rental_price_predictor'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # Fait des prédictions et formate la réponse
    prediction = loaded_model.predict(car_features)
    response = {"prediction": prediction.tolist()}
    return response

# Point d'entrée principal pour lancer l'application avec uvicorn
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
