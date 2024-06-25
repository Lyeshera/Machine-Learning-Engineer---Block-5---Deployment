import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split, GridSearchCV 
from sklearn.preprocessing import  StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

if __name__ == "__main__":

    # Définition de l'expérience
    experiment_name = "GetAround_car_rental_price_predictor"
    client = mlflow.tracking.MlflowClient()
    if (mlflow.get_experiment(0).name == "Default") & (mlflow.get_experiment_by_name(experiment_name) is None): 
        # Renomme et enregistre dans l'expérience "Default" si elle existe
        client.rename_experiment(0, experiment_name)
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    print("Entraînement du modèle...")
    
    # Mesure le temps d'exécution
    start_time = time.time()

    # Active l'autolog de mlflow pour sklearn
    mlflow.sklearn.autolog(log_models=True)

    # Analyse des arguments fournis dans le script shell 'run.sh' ou en ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument("--regressor", default = 'LR', choices = ['LR', 'Ridge', 'RF'])
    parser.add_argument("--cv", type = int, default = None)
    parser.add_argument("--alpha", type = float, nargs = "*")
    parser.add_argument("--max_depth", type = int, nargs="*")
    parser.add_argument("--min_samples_leaf", type = int, nargs="*")
    parser.add_argument("--min_samples_split", type = int, nargs="*")
    parser.add_argument("--n_estimators", type = int, nargs="*")
    args = parser.parse_args()

    # Importe le dataset
    df = pd.read_csv("input_data/get_around_pricing_project.csv", index_col = 0)

    # Supprime les lignes non pertinentes
    df = df[(df['mileage'] >= 0) & (df['engine_power'] > 0)]

    # Séparation des variables indépendantes (X) et de la variable cible (y)
    target_col = 'rental_price_per_day'
    y = df[target_col]
    X = df.drop(target_col, axis = 1)

    # Catégorisation des features
    numerical_features = []
    binary_features = []
    categorical_features = []
    for i,t in X.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numerical_features.append(i)
        elif ('bool' in str(t)):
            binary_features.append(i)
        else :
            categorical_features.append(i)

    # Regroupe les labels peu représentés sous le label 'other'
    for feature in categorical_features:
        label_counts = X[feature].value_counts()
        fewly_populated_labels = list(label_counts[label_counts < 0.5 / 100 * len(X)].index)
        for label in fewly_populated_labels:
            X.loc[X[feature]==label, feature] = 'other'

    # Séparation des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # Prétraitement des features
    categorical_transformer = OneHotEncoder(drop='first', sparse_output = False)
    numerical_transformer = StandardScaler()
    binary_transformer = FunctionTransformer(None, feature_names_out = 'one-to-one') # Fonction identité
    feature_preprocessor = ColumnTransformer(
            transformers=[
                ("categorical_transformer", categorical_transformer, categorical_features),
                ("numerical_transformer", numerical_transformer, numerical_features),
                ("binary_transformer", binary_transformer, binary_features)
            ]
        )

    # Définition du modèle
    grid_search_done = False
    if args.regressor == 'LR':
        model = LinearRegression()
    else: # Si un modèle peut avoir des hyperparamètres à optimiser, effectue une GridSearch avec validation croisée
        regressor_args = {option : parameters for option, parameters in vars(args).items() if (parameters is not None and option not in ['cv', 'regressor'])}
        regressor_params = {param_name : values for param_name, values in regressor_args.items()}
        if args.regressor == 'Ridge':
            regressor = Ridge()
        elif args.regressor == 'RF':
            regressor = RandomForestRegressor()
        model = GridSearchCV(regressor, param_grid = regressor_params, cv = args.cv, verbose = 3)
        grid_search_done = True

    # Pipeline
    predictor = Pipeline(steps=[
        ('features_preprocessing', feature_preprocessor),
        ("model", model)
    ])

    # Enregistrement de l'expérience dans MLFlow
    with mlflow.start_run() as run:
        
        # Entraîne le modèle sur l'ensemble d'entraînement
        predictor.fit(X_train, y_train)

        # Enregistre les meilleurs paramètres de GridSearch si une recherche de grille a été effectuée
        if grid_search_done:
            mlflow.log_params({"best_param_" + k: v for k, v in model.best_params_.items()})

        # Realise les prédictions
        y_train_pred = predictor.predict(X_train)
        y_test_pred = predictor.predict(X_test)

        # Enregistre le score MAE exprimé en % de la médiane de la cible comme nouvelle métrique pour l'ensemble d'entraînement 
        mlflow.log_metric(
            "training_MAE_percent_of_target_median", round(mean_absolute_error(y_train, y_train_pred) / y.median() * 100, 2)
        )

        # Enregistre les métriques d'autolog pour l'ensemble de test
        # mlflow.sklearn.eval_and_log_metrics(predictor, X_test, y_test, prefix = "test_")

        # Enregistre le score MAE exprimé en % de la médiane de la cible comme nouvelle métrique pour l'ensemble de test 
        mlflow.log_metric(
            "test_MAE_percent_of_target_median", round(mean_absolute_error(y_test, y_test_pred) / y.median() * 100, 2)
        )

        # Rempli le champ 'description' de la run avec les informations du modèle et la métrique principale
        mlflow.set_tags({'mlflow.note.content':f"{model}\ntest MAE: {round(mean_absolute_error(y_test, y_test_pred) / y.median() * 100, 2)}% of target median"})

        # Désactive l'autolog mlflow pour réentraîner le modèle sur l'ensemble complet (entraînement + test) 
        mlflow.sklearn.autolog(disable=False)
        predictor.fit(X, y)

        # Enregistre le modèle séparément pour plus de flexibilité dans la configuration 
        mlflow.sklearn.log_model(
            sk_model=predictor,
            artifact_path="car_rental_price_predictor",
            registered_model_name=f"{args.regressor}_car_rental_price_predictor",
            signature=infer_signature(X, y)
        )
        
    print("...Terminé!")
    print(f"---Total temps de training: {time.time()-start_time}")
