# JWT (JSON Web Token)

**Definición:**
Es un estándar abierto (RFC 7519) que define una forma compacta y segura de transmitir información entre partes como un objeto JSON. 
Se usa principalmente para autenticación y autorización.

**Puntos Core:**
- **Stateless (Sin estado):** El servidor no necesita guardar sesiones ni consultar una base de datos en cada petición. El token contiene toda la info necesaria del usuario.
- **Firma digital:** El token está firmado, lo que garantiza que no ha sido alterado por terceros.
- **Estructura:** Se divide en tres partes separadas por puntos: `Header.Payload.Signature` (Cabecera, Cuerpo y Firma).
- **Expiración:** Por seguridad, los tokens tienen un tiempo de vida corto (`exp`).

**Ejemplo de valor para un cliente:**
Un cliente tiene una app móvil con miles de usuarios consumiendo su API. Si usara sesiones tradicionales, tendría que pagar servidores gigantes solo para recordar quién está conectado. Con JWT, el servidor solo valida la firma del token. El valor es que el cliente puede 
**escalar su backend horizontalmente (añadir más servidores)** sin necesidad de compartir sesiones y ahorra costos de infraestructura.
