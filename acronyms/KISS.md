# KISS (Keep It Simple, Stupid)

**Definición:** 
Es un principio de diseño que establece que la mayoría de los sistemas funcionan mejor si se mantienen simples, en lugar de complicarlos innecesariamente. La complejidad debe evitarse a menos que sea estrictamente necesaria.

**Puntos Core:**
- **Evitar la sobre-ingeniería:** No agregar funcionalidades, capas o abstracciones que el sistema no necesita *todavía*.
- **Legibilidad:** El código debe ser fácil de entender para cualquier miembro del equipo.
- **Refactorización:** Primero haz que funcione de la forma más simple, y luego (si es necesario) optimiza o mejora.
- **Evitar la optimización prematura:** No gastar tiempo resolviendo problemas de rendimiento que aún no existen.

**Ejemplo de valor para un cliente:**
Imagina que un cliente pide un ERP para gestionar inventario, pero exige una interfaz con 50 botones, animaciones 3D y gráficos complejos para funcionalidades extremadamente sencillas (como sumar y restar stock). 
Aplicar KISS nos permite proponerle una primera versión funcional (un formulario simple y una tabla): entregamos valor en semanas en lugar de meses, el cliente empieza a usar el producto rápido y la complejidad visual se añade solo si el uso real lo demuestra.
