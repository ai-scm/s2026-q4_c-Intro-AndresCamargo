# Taller MLflow + Docker: del dato al modelo desplegado

Dataset: `load_breast_cancer` de scikit-learn, usado solo como vehículo pedagógico. El foco no es el diagnóstico, sino cómo los datos se convierten en un modelo, cómo se versiona y cómo se despliega.

## Archivos
| Archivo | Función |
|---|---|
| `explorar.py` | Exploración local de los datos |
| `train.py` | Entrenamiento, validación, tracking y registro (dentro de Docker) |
| `Dockerfile` | Imagen reproducible con versiones fijas de las librerías |
| `docker-compose.yml` | Tres servicios: `mlflow` (tracking y registry), `train` (entrenamiento) y `serve` (API) |
| `probar.py` | Cliente que consulta el modelo desplegado con datos no vistos |

## Cómo ejecutarlo
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements-local.txt
    python3 explorar.py
    docker compose up --build -d
    python3 probar.py
    docker compose down

## Ciclo de vida de los datos aplicado a lo que hicimos

| Etapa del data lifecycle | Qué hicimos en el taller | Dónde |
|---|---|---|
| **Ingestión** | Carga del dataset (569 registros, 30 variables y la clase objetivo) | `explorar.py`, `train.py` |
| **Calidad y exploración** | 0 nulos; clases 357 benignas (63 %) y 212 malignas (37 %): desbalance leve | `explorar.py` |
| **Transformación** | Partición 80/20 estratificada con semilla fija (`random_state=42`) para conservar la proporción de clases | `train.py` |
| **Almacenamiento y versionado** | MLflow guarda parámetros, métricas y artefactos en SQLite y un volumen Docker | servicio `mlflow` |
| **Consumo** | El modelo se expone como API REST y se consulta con datos nuevos | servicio `serve`, `probar.py` |

## Ciclo de vida del modelo (lo nuevo)

| Etapa del modelo | Qué hicimos | Dónde |
|---|---|---|
| Entrenamiento | Random Forest (100 árboles, profundidad 5) | `train.py` |
| Validación | Accuracy y F1 sobre el 20 % que el modelo no vio | `train.py` |
| Tracking | Parámetros y métricas registrados por corrida | MLflow, experimento `breast-cancer-classification` |
| Registro | Modelo `breast-cancer-clf` v1 con su firma (esquema de entrada/salida) | Model Registry |
| Despliegue | Alias `champion` apunta a la versión servida | servicio `serve` |
| Inferencia | Predicciones sobre los casos de prueba vía HTTP | `probar.py` |

## Qué se mantiene, qué cambia y qué se amplía
- **Se mantiene:** ingestión, revisión de calidad y transformación; siguen siendo la base.
- **Cambia:** el consumidor ya no lee una tabla o un dashboard, sino que envía datos a una API y recibe predicciones.
- **Se amplía:** la validación ya no revisa solo los datos, sino también el comportamiento del modelo; el versionado ya no cubre solo datasets, sino también modelos, parámetros y métricas.

## Resultados
Accuracy 0.96 y F1 0.97 sobre 114 casos de prueba. Detalle de aciertos y errores en la matriz de confusión de `probar.py`.
Limitación: es una sola partición train/test, y en un contexto clínico habría que priorizar el recall de la clase maligna.

## Evidencias
1. `evidencias-mlflow/01-exploracion-datos.jpeg`: salida de `explorar.py`.
2. `evidencias-mlflow/02-docker-servicios.jpeg`: `docker compose ps -a`.
3. `evidencias-mlflow/03-experimento-mlflow.jpeg`: lista de corridas con el modelo v1.
4. `evidencias-mlflow/04-metricas-parametros.jpeg`: métricas y parámetros de la corrida.
5. `evidencias-mlflow/05-modelo-registrado.jpeg`: Models, `breast-cancer-clf` con alias `champion`.
6. `evidencias-mlflow/06-inferencia.jpeg`: salida de `probar.py`.
