# La inteligencia artificial y la nueva forma de crear software

## Presentación

La inteligencia artificial generativa está cambiando quién escribe el código, y también cómo se organizan los equipos, qué roles necesitan y cómo le explican a la máquina lo que quieren construir.

Los dos temas se complementan. 

El primero, ¿La IA mató SCRUM?.
El segundo, profundiza en una forma concreta de trabajar con la IA: el desarrollo guiado por especificaciones.


## Contexto

Scrum es un marco de trabajo ágil pensado para que las personas colaboren en ciclos cortos llamados *sprints*. Su última guía oficial es de 2020, antes de la llegada de ChatGPT en 2022, 
en 2025 apareció un suplemento de la guía SCRUM sobre IA, pero el núcleo del marco siguió igual, por ende surge la pregunta: ¿sigue siendo adecuada una forma de trabajo diseñada solo para humanos cuando la IA hace parte del equipo?

## Tema 1: El impacto de la IA en Scrum

Se plantea que la IA sacude tres bases de Scrum siendo la primera la **velocidad**: si un producto puede avanzar en un día, esperar dos semanas pierde sentido, la segunda es el **tamaño de los equipos**, que se reduce porque cada persona produce más, 
de modo que reuniones pensadas para grupos grandes empiezan a sobrar y la tercera es la **comunicación**: la IA actúa como un compañero más, pero no se le habla igual que a una persona.

Esto transforma los **roles**. El Product Owner, que ya había evolucionado hacia Product Manager, avanza ahora hacia el **IA Product Manager**. Aparece también el **IA Product Builder**, que construye soluciones apoyado en IA y en cambio, el Scrum Master queda en riesgo: 
si desaparecen las ceremonias, hay menos que facilitar.

Cambia además el **ciclo de vida**, con un modelo de doble carril. El *Vibe Coding* permite crear prototipos muy rápido, mientras el *Vibe Engineering* cuida la robustez y la calidad, con el ser humano como responsable de exigir estándares.
Las historias de usuario siguen vigentes, pero ahora conviven con las *specs*, instrucciones detalladas para la IA, y el riesgo es hacerlas tan extensas que se regrese al modelo en cascada y por último, el **testing** se reinventa, porque hay que controlar lo que la IA genera.

## Tema 2: Spec-Driven Development

Si a la IA hay que explicarle bien lo que se necesita, la pregunta siguiente es cómo hacerlo, con el *Vibe Coding* se escribe una petición general y se corrige sobre la marcha siendo muy útil para experimentar, pero los resultados varían y se saltan etapas del ciclo de vida del software (SDLC).

El **Spec-Driven Development (SDD)** propone empezar por una especificación que describa el comportamiento del sistema y sus restricciones. 
Funciona como un **contrato**: de ella salen el diseño y la lista de tareas, que una persona revisa; después un agente de IA implementa y crea las pruebas, y el resultado se ajusta hasta cumplir lo acordado.

El cambio está en el punto de partida. De forma tradicional se programaba y luego se documentaba; en el desarrollo guiado por pruebas (TDD) primero se escriben las pruebas; en SDD todo nace de la especificación.

Un ejemplo es un inicio de sesión. En lugar de pedir "necesito una página de login", se definen la ruta, el tipo de petición, los datos que recibe y qué debe pasar si falta el usuario o si las credenciales son válidas por lo que hay menos ambigüedad, resultados más predecibles y un mantenimiento más sencillo.

La IA acelera la construcción de software, pero hace más importante saber qué se quiere construir y comprobar que esté bien hecho. El papel humano se desplaza hacia definir, revisar y decidir.

## Mis conclusiones
La llegada de la Inteligencia Artificial innovo en el desarrollo de Software, una conclusión que hice es que el Software es más rápido la ingeniería ha bajado, conocer estos roles que evolucionaron es interesante, 
y precisamente para contrarrestar la conclusión que yo hago sobre la calidad del software, SCRUM de por si es una metodólogia que tiene sus años en algún momento iba a tener que cambiar y con la llegada de esta nueva herramienta no fue la excepción.
## Referencias
- [Scrum ha muerto](https://javiergarzas.com/2026/03/scrum-ha-muerto-esto-es-lo-que-viene-ahora.html)
- [La IA te ha devuelto al cascada](https://javiergarzas.com/2026/10/la-ia-te-ha-devuelto-al-cascada-pistas-de-que-ya-trabajas-asi.html)
- [Evolución de los roles de producto](https://javiergarzas.com/2026/04/asi-han-evolucionado-los-roles-de-producto-cuando-el-equipo-trabaja-con-ia-sea-cual-sea-tu-rol-ya-esta-mutando-lo-estas-viendo.html)
- [Spec-Driven Development: AI Assisted Coding Explained](https://www.youtube.com/watch?v=mViFYTwWvcM)
- [Resumen en Geeky Gadgets](https://www.geeky-gadgets.com/spec-driven-development-ai-coding/)
- [Resumen de Learn by Doing with Steven](https://learnbydoingwithsteven.substack.com/p/spec-driven-development-an-analysis)
