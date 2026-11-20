# SOLID

**Definición:**
Son cinco principios de diseño de software orientado a objetos que buscan crear sistemas más mantenibles, escalables y fáciles de entender.

**Puntos Core:**
1. **S - Single Responsibility (SRP):** Una clase debe tener una sola razón para cambiar (una única responsabilidad).
2. **O - Open/Closed (OCP):** El código debe estar abierto a la extensión pero cerrado a la modificación. (Se pueden agregar cosas nuevas sin romper lo que ya funciona).
3. **L - Liskov Substitution (LSP):** Una subclase (hija) debe poder sustituir a su clase padre sin que el programa se rompa. *(Ej: Imagine una clase `Ave` con método `volar()`, no puedes hacer que `Pingüino` herede de `Ave`, porque al intentar volar fallará. Solución: la creación de una clase `AveVoladora`)*.
4. **I - Interface Segregation (ISP):** Es mejor tener muchas interfaces pequeñas y específicas que una sola interfaz "gorda" con métodos que algunas clases no usan. *(Ej: Un `Robot` no debería implementar una interfaz `Trabajador` que le obligue a tener el método `comer()`)*.
5. **D - Dependency Inversion (DIP):** Depender de abstracciones (interfaces), no de implementaciones concretas. La lógica de negocio no debe depender de una base de datos específica, sino de una interfaz genérica, para que puedas cambiar de base de datos sin reescribir el código.

**Ejemplo de valor para un cliente:**
Un cliente pide un módulo de pagos que acepte tarjeta y PayPal. Aplicando DIP, creamos una interfaz `ProcesadorPago`. El sistema principal no depende de la lógica de PayPal, sino de esa interfaz. El valor es que mañana el cliente pide añadir "Pago con Cripto" y 
nosotros solo creamos un nuevo archivo que implemente la interfaz, sin tocar ni romper el código de pedidos o de PayPal.
