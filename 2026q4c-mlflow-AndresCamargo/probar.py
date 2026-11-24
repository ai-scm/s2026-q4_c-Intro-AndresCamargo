import json
import urllib.request
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Misma partición que train.py: estos casos NO se usaron para entrenar
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

payload = {"dataframe_split": {"columns": list(X_test.columns), "data": X_test.values.tolist()}}
req = urllib.request.Request(
    "http://localhost:5001/invocations",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)
preds = json.loads(urllib.request.urlopen(req).read())["predictions"]

nombre = {0: "maligno", 1: "benigno"}
print(f"Casos enviados al modelo desplegado: {len(preds)}\n")
print("Primeros 10 casos:")
for i in range(10):
    real, pred = int(y_test.iloc[i]), preds[i]
    print(f"  Paciente {i+1}: real={nombre[real]:8} predicho={nombre[pred]:8} {'OK' if real == pred else 'ERROR'}")

print(f"\nAccuracy sobre datos de prueba: {accuracy_score(y_test, preds):.3f}")
print("\nMatriz de confusión (filas=real, columnas=predicho) [maligno, benigno]:")
print(confusion_matrix(y_test, preds, labels=[0, 1]))
print("\n" + classification_report(y_test, preds, target_names=["maligno", "benigno"]))
