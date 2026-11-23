# Ciclo de Vida de los Datos en AWS

- **Etapa 5 – Archivado de datos** (almacenamiento a largo plazo con Amazon S3 y S3 Glacier).
- **Punto 4 – Seguridad de datos, privacidad y cumplimiento** (acceso, cifrado y normativas).


---

## Rama izquierda – Etapa 5: Archivado de datos

AWS ofrece servicios flexibles de almacenamiento en la nube para archivar, lo que permite centrarse en los datos y no en administrar sistemas de cintas y bibliotecas.

### Servicios y clases de almacenamiento

| Servicio / clase | Qué dice el documento |
|---|---|
| **Amazon S3 Glacier** | Conservación de datos a largo plazo y almacenamiento de bajo costo para archivado. La API de S3 ofrece múltiples opciones de acceso, con recuperación desde unos pocos minutos hasta 48 horas. Casos de uso: archivos de medios digitales, registros financieros y de atención médica, datos de secuencias genómicas, copias de seguridad a largo plazo y datos para cumplimiento normativo. Precio: **$0.004 por GB/mes** (región este de EE. UU.). |
| **Amazon S3 Glacier Deep Archive** | Servicio de reemplazo de cintas: clase de almacenamiento de S3 para retención a largo plazo y preservación digital, con el precio más bajo de almacenamiento de AWS (**$0.00099 por GB/mes**). Ideal para copias duraderas a las que rara vez se accederá; elimina las bibliotecas de cintas locales y la reescritura de datos en cintas nuevas. Todos los datos se pueden recuperar en 12 horas. Complementa a S3 Glacier, ideal para archivos más activos recuperables en minutos. |
| **Amazon S3 Standard-IA** | Acceso poco frecuente con acceso rápido cuando se necesita. Ofrece la durabilidad, el rendimiento y la baja latencia de S3 Estándar, con bajo precio de almacenamiento por GB y una tarifa de recuperación por GB. |
| **Amazon S3 One Zone-IA** | Almacena los datos en una sola zona de disponibilidad, con un 20 % menos de costo que S3 Standard-IA, que replica en múltiples zonas de disponibilidad. |
| **Amazon S3 Intelligent-Tiering** | Niveles automatizados para datos con patrones de acceso desconocidos o cambiantes: mueve objetos entre un nivel de acceso frecuente y otro de menor costo. |
| **Amazon S3 (más rápido)** | Opción cuando se necesita almacenamiento más rápido, frente a Glacier y Deep Archive, que son asequibles y no sensibles al tiempo. |

### Preguntas clave del documento
- ¿Se archivarán los datos para análisis y cumplimiento?
- ¿Cuáles son los beneficios de costo y rendimiento de la nube frente al archivo tradicional?
- ¿Cómo puede complementar las prácticas actuales de archivo?

### Cumplimiento y cifrado
Las soluciones de almacenamiento de AWS han alcanzado numerosos estándares de cumplimiento y certificaciones de seguridad, y ofrecen cifrado integrado.

---

## Rama derecha – Punto 4: Seguridad de datos, privacidad y cumplimiento

Los datos se almacenan en múltiples entornos de TI, en cientos de aplicaciones y con miles de usuarios; la privacidad y la clasificación de datos son un componente central de los requisitos de seguridad.

### Clasificación de datos
- **Confidencialidad:** acceso controlado y autorizado según permisos.
- **Integridad:** exactitud y ausencia de cambios no autorizados.
- **Disponibilidad:** accesibilidad y usabilidad cuando se necesiten.

### Cumplimiento normativo
- **Normativas mencionadas:** GDPR, United States Munitions List / CUI, HIPAA e ISM.
- **Programa de garantía de seguridad de AWS:** protecciones y controles validados por evaluaciones independientes de terceros.
- **AWS GovCloud (US) Regions:** entornos aislados que ayudan a cumplir FedRAMP High, CJIS, ITAR, EAR, Cloud Computing SRG (niveles 2, 4 y 5), FIPS 140-2, IRS-1075 y otros regímenes.

### Servicios de AWS para proteger los datos

| Servicio | Función según el documento |
|---|---|
| **AWS IAM** | Define cuentas de usuario individuales con permisos sobre los recursos de AWS. |
| **AWS MFA** | Autenticación segura para cuentas privilegiadas, con opciones de autenticadores por hardware. |
| **AWS Directory Service** | Integración y federación con directorios corporativos. |
| **AWS KMS** | Permite elegir si AWS administra las claves de cifrado o el cliente mantiene el control. |
| **Cifrado del lado del servidor (SSE)** | **SSE-S3** (claves administradas por S3), **SSE-KMS** (claves en AWS KMS) y **SSE-C** (claves del cliente). |

Los datos se cifran en tránsito y en reposo, con opción de administrar las propias claves, disponible en Amazon EBS, S3, RDS y Redshift. El cliente conserva el control total de su contenido y AWS nunca lo usa para marketing o publicidad.

---

**Andrés Felipe Camargo García** Blend 360 All-Star
