# XSS (Cross-Site Scripting)

**Definición:**
Es una vulnerabilidad de seguridad web que permite a un atacante inyectar scripts maliciosos (generalmente JavaScript) en las páginas web que ven otros usuarios. Ocurre cuando la aplicación no valida ni escapa correctamente los datos que ingresa el usuario.

**Puntos Core:**
- **XSS Reflejado:** El script malicioso viene en la petición (ej. un link con código) y se refleja inmediatamente en la respuesta.
- **XSS Almacenado:** El script se guarda en la base de datos (ej. en un comentario) y se ejecuta cada vez que alguien carga la página.
- **Impacto:** Robo de cookies, suplantación de identidad, redirección a sitios falsos.
- **Prevención:** Validar entradas, escapar la salida (convertir `<` en `&lt;`) y usar cabeceras de seguridad como CSP (Content Security Policy).

**Ejemplo de valor para un cliente:**
Un cliente tiene un foro donde sus usuarios publican comentarios. Un atacante publica un comentario con un script invisible que roba las contraseñas de los administradores. Al aplicar validación y escape de salida, el foro muestra el texto literal inofensivo. 
El valor es que protegemos la **reputación del cliente y la seguridad de sus usuarios**, evitando un incidente que podría costarle una multa por fuga de datos y la pérdida de confianza.
