# Pipeline de datos serverless en AWS: CSV → JSON → Glue → Athena

| | |
|---|---|
| **Autor** | Andrés Camargo |
| **Fecha** | 17 de noviembre de 2026 |
| **Región AWS** | US East (N. Virginia) `us-east-1` |
| **Servicios** | Amazon S3 · AWS Lambda · AWS IAM · Amazon CloudWatch · AWS Glue · Amazon Athena |
| **Lenguajes** | Python 3 (Lambda) · SQL (Athena) |

---

## 1. Objetivo

Construir un pipeline de datos orientado a eventos que:

1. Reciba un archivo **CSV** en un bucket de entrada (*input*).
2. Lo transforme automáticamente con una función **Lambda** en Python, generando **un archivo JSON por cada fila**.
3. Deje los JSON en un bucket de salida (*output*).
4. Catalogue esos JSON en una base de datos de **AWS Glue** mediante un *crawler*.
5. Permita consultarlos con **SQL** desde **Amazon Athena**.

---

## 2. Arquitectura

```mermaid
flowchart LR
    U([Usuario]) -- "1. sube CSV" --> I[(S3 Input<br/>bld-tseed-workshop-input-<br/>semillero-2026-q4-c)]
    I -- "2. evento ObjectCreated (.csv)" --> L[[AWS Lambda<br/>bld-tseed-workshop-andres-camargo]]
    L -- "3. GetObject (lee CSV)" --> I
    L -- "4. PutObject (1 JSON por fila)" --> O[(S3 Output<br/>bld-tseed-workshop-output-<br/>semillero-2026-q4-c)]
    O -- "5. lee y deduce el esquema" --> C{{Glue Crawler}}
    C -- "6. crea la tabla" --> G[(Glue Data Catalog<br/>tabla users_dataset_100)]
    G -- "7. consultas SQL" --> A[/Amazon Athena/]
    L -. "logs" .-> CW[CloudWatch Logs]
```

**Tipo de patrón:** ETL (*Extract, Transform, Load*) serverless, disparado por eventos.

| Fase ETL | Dónde ocurre |
|---|---|
| **Extract** | La Lambda lee el CSV del bucket input (`get_object`) |
| **Transform** | `csv.DictReader` convierte cada fila en diccionario y `json.dumps` en JSON |
| **Load** | La Lambda escribe cada JSON en el bucket output (`put_object`); luego Glue los cataloga |

---

## 3. Servicios de AWS utilizados

| Servicio | Rol en el proyecto | Concepto clave |
|---|---|---|
| **Amazon S3** | Almacena el CSV (input) y los JSON (output) | Almacenamiento de objetos. Las "carpetas" no existen: son parte del nombre (*key*) del objeto, p. ej. `AndresCamargo/archivo.csv` |
| **AWS Lambda** | Ejecuta el código Python que transforma los datos | Cómputo sin servidor; se paga por ejecución; tiene timeout y memoria configurables |
| **Notificaciones de S3 (trigger)** | Conecta el bucket input con la Lambda | Arquitectura orientada a eventos |
| **AWS IAM** | Define qué puede hacer cada servicio | Roles, políticas y principio de mínimo privilegio |
| **Amazon CloudWatch** | Registra logs de la Lambda | Herramienta principal de depuración |
| **AWS Glue** | Base de datos (Data Catalog) y *crawler* | El catálogo solo guarda **metadatos**; los datos siguen en S3 |
| **Amazon Athena** | Consultas SQL sobre los datos en S3 | Motor de consultas sin servidor; guarda los resultados en S3 |

---

## 4. Desarrollo paso a paso

### 4.1 Creación de los buckets

Se crearon dos buckets en S3, con una carpeta `AndresCamargo/` dentro de ellos:

| Bucket | Función |
|---|---|
| `bld-tseed-workshop-input-semillero-2026-q4-c` | Recibe el archivo CSV |
| `bld-tseed-workshop-output-semillero-2026-q4-c` | Recibe los JSON generados |

> **Por qué dos buckets distintos:** si la Lambda escribiera en el mismo bucket que la dispara, se invocaría a sí misma en un bucle infinito (con el consiguiente costo).


### 4.2 Función Lambda

Función: `bld-tseed-workshop-andres-camargo` (Python 3).

**Lógica:**

1. S3 dispara la Lambda y le entrega un `event` con el bucket y la *key* del archivo.
2. La Lambda descarga el CSV con `boto3`.
3. `csv.DictReader` usa la primera fila como encabezado y devuelve cada fila como diccionario.
4. Cada diccionario se serializa a JSON y se guarda como un objeto independiente en el output.

**Código final:**

```python
import csv
import io
import json
import urllib.parse

import boto3

s3 = boto3.client('s3')

OUTPUT_BUCKET = 'bld-tseed-workshop-output-semillero-2026-q4-c'


def lambda_handler(event, context):
    total_filas = 0

    # Un evento de S3 puede traer uno o varios registros
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        # La key viene codificada en URL (espacios -> '+'), por eso se decodifica
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        # 1. Leer el CSV desde el bucket input
        respuesta = s3.get_object(Bucket=bucket, Key=key)
        contenido = respuesta['Body'].read().decode('utf-8-sig')  # quita el BOM de Excel

        # 2. Convertir cada fila en un diccionario
        lector = csv.DictReader(io.StringIO(contenido))
        nombre_base = key.rsplit('.', 1)[0]

        # 3. Guardar cada fila como un JSON en el bucket output
        for i, fila in enumerate(lector, start=1):
            s3.put_object(
                Bucket=OUTPUT_BUCKET,
                Key=f"{nombre_base}/fila_{i}.json",
                Body=json.dumps(fila, ensure_ascii=False),
                ContentType='application/json'
            )
            total_filas += 1

    return {
        'statusCode': 200,
        'body': json.dumps(f'{total_filas} filas convertidas a JSON')
    }
```

| Elemento del código | Para qué sirve |
|---|---|
| `event['Records']` | Lista de eventos que envía S3 |
| `unquote_plus` | Decodifica la *key* (S3 la entrega codificada en URL) |
| `utf-8-sig` | Evita que el BOM de los CSV exportados desde Excel contamine el primer encabezado |
| `csv.DictReader` | Entrega cada fila con los nombres de columna como llaves, que es justo la forma de un JSON |
| `ensure_ascii=False` | Conserva tildes y caracteres especiales |
| `nombre_base/fila_N.json` | Ruta de salida: una carpeta por CSV y un archivo por fila |


### 4.3 Rol de ejecución y permisos (primera configuración)

Al crear la Lambda se generó un rol de ejecución (`bld-tseed-workshop-andres-camargo-role-dqxholhy`) que por defecto incluye solo `AWSLambdaBasicExecutionRole`, que permite únicamente escribir logs en CloudWatch. Se le agregó una **política adicional** con permisos sobre S3:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bld-tseed-workshop-input-semillero-2026-q4-c/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::bld-tseed-workshop-output-semillero-2026-q4-c/*"
    }
  ]
}
```

El **Resumen de recursos** (Configuración → Permisos) confirmó el permiso: `Amazon S3 – 2 acciones, 2 recursos` (`GetObject` sobre el input y `PutObject` sobre el output).

#### Dos tipos de política distintos (confusión inicial)

Durante la configuración apareció una pantalla que pedía un `Principal`. Se identificó que existen dos tipos de política y que no se deben mezclar:

| | Política **basada en identidad** | Política **basada en recursos** |
|---|---|---|
| **Pregunta que responde** | ¿Qué puede **hacer** esta Lambda? | ¿Quién puede **invocar** esta Lambda? |
| **Dónde vive** | En el **rol** de ejecución (IAM) | En la propia Lambda (Configuración → Permisos) |
| **Lleva `Principal`** | No | Sí |
| **Ejemplo en este proyecto** | `GetObject`, `ListBucket`, `PutObject` sobre S3 | Permiso para que `s3.amazonaws.com` ejecute `lambda:InvokeFunction` |
| **Quién la crea** | Nosotros, en IAM | La crea **automáticamente** el trigger de S3 |

### 4.4 Configuración del trigger (desencadenador)

Lambda → **Agregar desencadenador** → origen **S3**:

| Parámetro | Valor |
|---|---|
| Bucket | `bld-tseed-workshop-input-semillero-2026-q4-c` |
| Tipo de evento | Todos los eventos de creación de objetos |
| Sufijo (recomendado) | `.csv` |

AWS confirmó con el mensaje *"El desencadenador … se agregó correctamente a la función"*, y el diagrama de la Lambda muestra S3 conectado a la izquierda. Al crearlo, AWS agregó solo, en la política basada en recursos, el permiso `lambda:InvokeFunction` para S3 con condiciones de cuenta y de bucket de origen.

### 4.5 Pruebas y depuración de la Lambda


Evento de prueba (`Unit-test`) que simula lo que envía S3:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "bld-tseed-workshop-input-semillero-2026-q4-c" },
        "object": { "key": "AndresCamargo/NOMBRE-DEL-ARCHIVO.csv" }
      }
    }
  ]
}
```


### 4.6 AWS Glue: base de datos y crawler

Los JSON están en S3, pero AWS no conoce su estructura. Para exponerlos como tabla se usaron dos componentes de Glue:

- **Base de datos (Data Catalog):** contenedor lógico de metadatos.
- **Crawler:** lee los archivos, deduce columnas y tipos, y **crea la tabla**.

```mermaid
flowchart LR
    J[JSON en S3 output] --> CR{{Crawler}}
    CR -- "deduce esquema" --> T[(Tabla users_dataset_100<br/>en la base de datos Glue)]
    T --> AT[/Athena/]
```

| Elemento | Valor |
|---|---|
| Base de datos | `bld-tseed-workshop-andres-camargo` |
| Crawler | `bld-tseed-workshop-crawlers-Andres-camargo` |
| Origen de datos | Carpeta del bucket output con los JSON (`s3://bld-tseed-workshop-output-semillero-2026-q4-c/...`) |
| Ejecución | *On demand* |
| Tabla generada | `users_dataset_100` |

**Columnas detectadas** (todas de tipo `string`): `user_id`, `name`, `country`, `city`, `role`, `department`, `education`, `age`, `gender`, `marital_status`, `experience_years`, `skills`, `languages`, `hobbies`, `salary`, `email`, entre otras.

> **Hallazgo:** todas las columnas quedaron como `string`, incluso `age` y `salary`, porque `csv.DictReader` lee todos los valores como texto y la Lambda los escribió así en el JSON. Por eso, en Athena hay que usar `CAST` para comparar o calcular con números.


### 4.7 Amazon Athena: consultas SQL

Athena consulta directamente los JSON en S3 usando el esquema de la tabla del catálogo. Antes de la primera consulta fue necesario configurar dónde guardar los resultados 

---

## 5. Cambios de permisos realizados

Los permisos no funcionaron a la primera; se fueron ajustando según los errores. Resumen de cada cambio:

| # | Dónde | Cambio | Por qué fue necesario |
|---|---|---|---|
| 1 | Rol de la Lambda (IAM) | Se agregó `s3:GetObject` (input) y `s3:PutObject` (output) | Por defecto el rol solo podía escribir logs; sin esto la Lambda no puede leer ni escribir en S3 |
| 2 | Rol de la Lambda (IAM) | Se agregó `s3:ListBucket` sobre el bucket input (**sin** `/*`) | Sin este permiso, cuando un objeto no existe S3 responde `AccessDenied` en lugar de `NoSuchKey`, ocultando la causa real del error |
| 3 | Política de la Lambda (basada en recursos) | Se agregó automáticamente `lambda:InvokeFunction` para `s3.amazonaws.com` | Lo crea el trigger; permite que S3 invoque la función |
| 4 | Rol del crawler de Glue (IAM) | Se asignó un rol de servicio válido para Glue con lectura del bucket output | El primer intento falló por un rol inexistente (ver sección 6) |
| 5 | Athena (configuración del workgroup) | Se definió la ubicación de resultados de consultas | Athena exige un destino en S3 antes de ejecutar la primera consulta |

**Política final del rol de la Lambda:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bld-tseed-workshop-input-semillero-2026-q4-c/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::bld-tseed-workshop-input-semillero-2026-q4-c"
    },
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::bld-tseed-workshop-output-semillero-2026-q4-c/*"
    }
  ]
}
```

> **Detalle de sintaxis que se identificó:** `GetObject` y `PutObject` actúan sobre *objetos* y por eso el recurso termina en `/*`; `ListBucket` actúa sobre el *bucket* y por eso el recurso **no** lleva `/*`.

---

## 6. Errores encontrados, causa y solución

| # | Error | Dónde | Causa real | Solución |
|---|---|---|---|---|
| 1 | `KeyError: 'Records'` | Lambda, botón *Test* | El evento de prueba por defecto no tiene el formato de S3 y el código espera `event['Records']` | Crear un evento de prueba con la estructura de S3 (sección 4.5). La subida real de un CSV sí envía `Records` |
| 2 | `AccessDenied` al llamar `GetObject` (*no autorizado para `s3:ListBucket`*) | Lambda | Faltaba `s3:ListBucket` en el rol y, además, la *key* del evento de prueba no coincidía con un archivo existente. Con el permiso ausente, S3 oculta la inexistencia del objeto | Agregar `s3:ListBucket` al rol |
| 3 | `NoSuchKey: The specified key does not exist` | Lambda | La *key* del evento de prueba no incluía la "carpeta" `AndresCamargo/`. En S3 la ruta completa forma parte del nombre del objeto | Usar la *key* completa: `AndresCamargo/archivo.csv` |
| 4 | `Task timed out after 3.00 seconds` | Lambda | El timeout por defecto (3 s) no alcanza: el código hace un `put_object` por fila, en serie, más el tiempo de arranque. **Los JSON sí aparecieron en el output**, lo que confirma que la lógica y los permisos eran correctos | Aumentar el timeout (Configuración → Configuración general → Editar; p. ej. 1 minuto), re-ejecutar y verificar que el número de JSON coincida con las filas del CSV |
| 5 | Pantalla que exigía `Principal` | IAM / Lambda | Se intentó pegar una política de identidad en la pantalla de la política basada en recursos | Editar la política en el **rol** (IAM), no en la política de la Lambda |
| 6 | `AccessDeniedException … unable to assume the role …/AWSGlueServiceRole-` | Glue, creación del crawler | El nombre del rol quedó incompleto (terminaba en guion), por lo que el rol no existía y Glue no pudo asumirlo. El mensaje sugería "habilitar STS", pero **STS no era el problema** | Seleccionar o crear un rol válido para Glue con permiso de lectura sobre el bucket output |
| 7 | `No output location provided` | Athena | Athena guarda cada resultado en S3 y no había ubicación configurada | Editar ajustes → configurar *Athena managed query results* o un bucket/carpeta de resultados |
| 8 | Consulta apuntaba a un nombre de base de datos mal escrito y a `age` como si fuera una tabla | Athena | Se mezclaron nombres; `age` es una **columna**, no una tabla | Seleccionar la base en el panel y consultar `users_dataset_100` |
| 9 | `Only one sql statement is allowed` | Athena | Un `;` al final de la primera línea cerró la sentencia y `WHERE …` quedó como una segunda | El `;` va una sola vez, al final de toda la consulta |

---

## 7. Flujo temporal de una ejecución

```mermaid
sequenceDiagram
    actor U as Usuario
    participant I as S3 Input
    participant L as Lambda
    participant O as S3 Output
    participant CW as CloudWatch
    participant GL as Glue Crawler
    participant AT as Athena

    U->>I: Sube archivo .csv
    I->>L: Evento ObjectCreated (bucket + key)
    L->>I: GetObject (lee el CSV)
    loop Por cada fila
        L->>O: PutObject (fila_N.json)
    end
    L->>CW: Escribe logs
    U->>GL: Ejecuta el crawler
    GL->>O: Lee los JSON y deduce el esquema
    GL-->>GL: Crea la tabla en el Data Catalog
    U->>AT: Consulta SQL
    AT->>O: Lee los datos según el catálogo
    AT-->>U: Resultados
```

---

## 8. Consultas SQL practicadas en Athena

Tabla: `users_dataset_100`. Todas las columnas son `string`, por lo que se usa `CAST` para comparaciones numéricas.

| # | Pregunta | Consulta |
|---|---|---|
| 1 | Personas que hablan inglés y tienen más de 35 años | `SELECT * FROM users_dataset_100 WHERE languages LIKE '%English%' AND CAST(age AS INTEGER) > 35;` |
| 2 | Personas que viven en Berlín y tienen estudios *Bachelor's* | `SELECT * FROM users_dataset_100 WHERE city = 'Berlin' AND education = 'Bachelor''s';` |
| 3 | Data Analysts con más de 20 años | `SELECT * FROM users_dataset_100 WHERE role = 'Data Analyst' AND CAST(age AS INTEGER) > 20;` |
| 4 | Quienes ganan más (salario máximo) | Ver abajo |
| 5 | Top 5 de salarios | Ver abajo |

**Consulta 4: subconsulta con `MAX`:**

```sql
SELECT *
FROM users_dataset_100
WHERE CAST(salary AS DOUBLE) = (
    SELECT MAX(CAST(salary AS DOUBLE))
    FROM users_dataset_100
);
```

**Consulta 5: ranking con `ORDER BY` y `LIMIT`:**

```sql
SELECT name, role, country, salary
FROM users_dataset_100
ORDER BY CAST(salary AS DOUBLE) DESC
LIMIT 5;
```

**Conceptos de SQL aplicados:**

| Concepto | Uso |
|---|---|
| `SELECT … FROM … WHERE` | Estructura básica de filtrado |
| `AND` / `OR` | Combinar condiciones (en lugar de `&&` / `\|\|`) |
| `=` | Comparación de igualdad (un solo signo) |
| `LIKE '%texto%'` | Búsqueda parcial en campos con varios valores (p. ej. `languages`) |
| `CAST(col AS tipo)` | Convertir texto a número para comparar o calcular |
| Comilla doble `''` | Escapar un apóstrofe dentro de un texto (`'Bachelor''s'`) |
| Subconsulta | Calcular un valor (p. ej. el máximo) para usarlo en el `WHERE` |Spanish
| `ORDER BY … DESC` + `LIMIT` | Ranking de los N primeros |

---

## 9. Hallazgos y lecciones aprendidas

1. **Los permisos se definen de forma explícita.** Por defecto una Lambda no puede tocar S3; hay que concederlo en su rol.
2. **Identidad vs. recurso.** Lo que la Lambda *puede hacer* va en su rol (IAM). Quién *puede invocarla* va en su política basada en recursos, que el trigger crea solo.
3. **`ListBucket` aclara los errores.** Sin ese permiso, S3 responde `AccessDenied` aunque el problema real sea que el archivo no existe. Con él, el error es el claro `NoSuchKey`.
4. **En S3 no hay carpetas reales.** La ruta forma parte de la *key*, y por eso el evento de prueba debía incluir `AndresCamargo/`.
5. **El botón *Test* no simula a S3 por defecto.** Una Lambda depende del formato exacto del evento que recibe.
6. **Un timeout no implica fallo lógico.** Los JSON se generaron aunque la ejecución se cortó a los 3 s; conviene verificar el conteo de filas contra el de archivos.
7. **Glue no almacena datos.** El Data Catalog guarda metadatos; los datos permanecen en S3.
8. **Los tipos se heredan del origen.** Como el CSV se leyó como texto, el JSON y la tabla tienen todo en `string`.
9. **Los mensajes de error pueden engañar.** El error de Glue sugería habilitar STS, pero la causa era un nombre de rol incompleto.
10. **Mínimo privilegio.** Cada rol recibió solo lo necesario: leer el input, escribir el output, y (Glue) leer el output.

**Propiedades del diseño:**

- **Idempotencia:** volver a procesar el mismo CSV sobrescribe los mismos JSON, sin duplicar.
- **Desacoplamiento:** quien sube el CSV no conoce la Lambda; el trigger conecta las piezas.
- **Escalabilidad:** al ser serverless, no hay servidores que administrar.

---
