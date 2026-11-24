import os
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

MODEL_NAME = "breast-cancer-clf"
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
mlflow.set_experiment("breast-cancer-classification")

# 1) Ingestión y partición (stratify conserva el 63/37 de clases)
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

params = {"n_estimators": 100, "max_depth": 5, "random_state": 42}

with mlflow.start_run() as run:
    # 2) Entrenamiento
    model = RandomForestClassifier(**params).fit(X_train, y_train)

    # 3) Validación sobre datos que el modelo no vio
    preds = model.predict(X_test)
    metrics = {"accuracy": accuracy_score(y_test, preds), "f1": f1_score(y_test, preds)}

    # 4) Tracking: parámetros y métricas quedan versionados
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)

    # 5) Registro del modelo con su firma (esquema de entrada/salida)
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(
        model, artifact_path="model", signature=signature,
        input_example=X_train.head(2), registered_model_name=MODEL_NAME,
    )
    print("Run:", run.info.run_id, "| Métricas:", metrics)

# 6) El alias "champion" marca qué versión se despliega
client = MlflowClient()
newest = max(int(v.version) for v in client.search_model_versions(f"name='{MODEL_NAME}'"))
client.set_registered_model_alias(MODEL_NAME, "champion", str(newest))
print(f"Modelo {MODEL_NAME} v{newest} -> alias 'champion'")
