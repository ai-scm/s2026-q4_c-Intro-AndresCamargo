# CQRS (Command Query Responsibility Segregation)

**Definición:**
Es un patrón arquitectónico que separa las operaciones de **escritura (Comandos)** de las operaciones de **lectura (Consultas)**. 
En lugar de usar un único modelo de datos para todo, se usan dos modelos distintos.

**Puntos Core:**
- **Comandos:** Cambian el estado del sistema (Crear, Actualizar, Borrar). Requieren validaciones y consistencia.
- **Consultas:** Solo leen datos, no modifican nada. Se pueden optimizar para búsquedas rápidas.
- **Escalabilidad independiente:** Si el sistema recibe muchas más lecturas que escrituras, puedes escalar solo la parte de lectura sin tocar la de escritura.
- **Seguridad:** Permite tener reglas de acceso más estrictas para quien escribe vs. quien solo lee.

**Ejemplo de valor para un cliente:**
Un sistema de tickets de soporte. Los agentes crean tickets a toda hora (escritura rápida), pero los gerentes consultan reportes pesados de rendimiento (lectura compleja). Con CQRS, separamos los modelos. El valor para el cliente es que el sistema **no se ralentiza para los agentes** (escritura) cuando los gerentes están generando reportes gigantes (lectura), 
y cada parte escala según su propia demanda.
