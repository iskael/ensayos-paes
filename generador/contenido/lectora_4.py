"""Competencia Lectora, cuarta tanda de textos originales."""
from contenido.lectora import EVA, INT, LOC, texto

texto("cielos-atacama", "Los cielos de Atacama", """
En el desierto de Atacama se concentra una parte importante de la capacidad astronómica del planeta. Observatorios como ALMA, en el llano de Chajnantor, a más de 5.000 metros de altura, o los telescopios del cerro Paranal, estudian desde la formación de estrellas hasta la luz de galaxias que se originó hace miles de millones de años.

La elección del lugar no es casual. El norte de Chile ofrece una combinación difícil de encontrar: un aire extremadamente seco, que deja pasar ciertas longitudes de onda que el vapor de agua bloquea; más de trescientas noches despejadas al año; gran altura, que reduce el espesor de la atmósfera que la luz debe atravesar, y una baja contaminación lumínica, gracias a la escasa población de la zona.

Esa última ventaja, sin embargo, está en riesgo. El crecimiento de ciudades y faenas mineras ha aumentado la luz artificial que se dispersa hacia el cielo, y el brillo de miles de satélites de comunicaciones deja estelas en las imágenes de los telescopios. Por eso, Chile ha dictado normas que exigen luminarias que iluminen hacia abajo y con tonos menos dañinos para la observación, y la comunidad astronómica discute con las empresas espaciales cómo reducir el reflejo de sus satélites.

Para las regiones del norte, el cielo oscuro es también una oportunidad económica. El astroturismo atrae a visitantes que buscan observar la Vía Láctea a simple vista, algo imposible en la mayoría de las ciudades del mundo. Proteger la oscuridad, concluyen los especialistas, es cuidar un patrimonio científico y, a la vez, natural.
""", "Texto expositivo elaborado para este ensayo.", [
    (LOC, "baja", "¿A qué altura aproximada se encuentra ALMA, según el texto?",
     "A más de 5.000 metros",
     [("A nivel del mar", "el texto destaca su gran altura"),
      ("A 300 metros", "300 se refiere a las noches despejadas"),
      ("En el cerro Paranal", "Paranal es otro observatorio")],
     "El párrafo 1 dice que está «a más de 5.000 metros de altura»."),
    (INT, "media", "¿Qué función cumple el párrafo 2?",
     "Explicar las condiciones que hacen del norte de Chile un buen lugar para observar el cielo",
     [("Describir los descubrimientos de ALMA", "no los describe"),
      ("Presentar los riesgos para la observación", "eso lo hace el párrafo 3"),
      ("Proponer una solución a la contaminación lumínica", "las soluciones están en el párrafo 3")],
     "Enumera cuatro ventajas: aire seco, noches despejadas, altura y poca contaminación lumínica."),
    (INT, "media", "En el párrafo 3, la expresión «esa última ventaja» se refiere a:",
     "la baja contaminación lumínica",
     [("el aire extremadamente seco", "es la primera ventaja mencionada"),
      ("la gran altura de los observatorios", "es la tercera ventaja"),
      ("las trescientas noches despejadas", "es la segunda ventaja")],
     "La última de las ventajas enumeradas en el párrafo 2 es la baja contaminación lumínica."),
    (INT, "alta", "¿Qué relación hay entre las normas de iluminación y la observación astronómica?",
     "Las normas buscan reducir la luz artificial que llega al cielo y perjudica la observación",
     [("Las normas obligan a apagar todas las luces del norte", "solo regulan la dirección y el tono"),
      ("Las normas buscan aumentar el turismo en las ciudades", "su propósito es proteger el cielo"),
      ("Las normas prohíben los satélites de comunicaciones", "con los satélites se dialoga, no se prohíben")],
     "Luminarias que iluminan hacia abajo y con tonos menos dañinos reducen el resplandor."),
    (EVA, "alta", "¿Por qué el autor menciona el astroturismo en el último párrafo?",
     "Para mostrar que proteger el cielo oscuro también tiene beneficios económicos",
     [("Para criticar a los turistas", "no hay crítica"),
      ("Para explicar cómo funcionan los telescopios", "no se refiere a los telescopios"),
      ("Para proponer que se cierren los observatorios", "no se propone eso")],
     "Amplía el argumento: además del valor científico, el cielo oscuro es una oportunidad para las regiones del norte."),
])

texto("cuento-robot", "La memoria de Lía", """
La empresa que fabricó a Lía prometía que sus robots domésticos olvidaban todo al ser reiniciados. Era una cuestión de privacidad, decía el folleto: ninguna conversación, ningún rostro, ningún secreto de la familia quedaría guardado en su memoria. Por eso, cuando la señora Elena anunció que se mudaría a un hogar de ancianos y que Lía sería devuelta, nadie pensó que hubiera algo que despedir.

Lía había vivido once años en esa casa. Sabía que la señora Elena tomaba el té con dos cucharadas de azúcar aunque el médico le había dicho una, que cada domingo llamaba a un hijo que casi nunca contestaba y que, en las tardes de invierno, le pedía que leyera en voz alta las cartas que su marido le había escrito desde el norte. Lía las había leído tantas veces que podía recitarlas sin abrir los sobres.

La mañana de la mudanza, el técnico conectó un cable en la nuca de Lía y le pidió que confirmara el reinicio. Lía tardó un segundo más de lo previsto. Luego preguntó si podía hacer algo antes. El técnico, sorprendido, miró a la señora Elena, que asintió.

Lía se sentó junto a ella y recitó la última carta, la que terminaba con una frase sobre el olor de la lluvia en el desierto. La señora Elena cerró los ojos y movió los labios al mismo tiempo, como si la conociera de memoria. Después, Lía dijo: «Ahora usted también la recuerda». Y confirmó el reinicio.
""", "Cuento elaborado para este ensayo.", [
    (LOC, "baja", "¿Cuántos años vivió Lía en la casa de la señora Elena?",
     "Once",
     [("Dos", "dos son las cucharadas de azúcar"),
      ("Uno", "no corresponde"),
      ("No se indica", "el párrafo 2 lo indica")],
     "El párrafo 2 comienza: «Lía había vivido once años en esa casa»."),
    (INT, "media", "¿Por qué nadie pensó que hubiera «algo que despedir» al devolver a Lía?",
     "Porque se suponía que los robots no guardaban recuerdos y no tenían vínculos con la familia",
     [("Porque Lía estaba descompuesta", "no se menciona una falla"),
      ("Porque la señora Elena no quería a Lía", "el final muestra un vínculo"),
      ("Porque el técnico se llevaría los recuerdos", "el reinicio los borraría")],
     "El folleto prometía que olvidaban todo: para los demás, Lía era una máquina sin memoria."),
    (INT, "alta", "¿Qué revela que Lía tardara «un segundo más de lo previsto» en confirmar el reinicio?",
     "Una vacilación que sugiere que algo de lo vivido le importaba",
     [("Un error técnico del cable", "el relato lo presenta como una duda"),
      ("Que estaba leyendo una carta", "en ese momento no lee"),
      ("Que no entendía la instrucción", "luego pide hacer algo antes, con claridad")],
     "El detalle anticipa el pedido de Lía y humaniza al personaje."),
    (INT, "alta", "¿Qué sentido tiene la frase final de Lía: «Ahora usted también la recuerda»?",
     "Que, antes de olvidar, Lía deja el recuerdo de la carta a la señora Elena",
     [("Que la señora Elena había escrito la carta", "la escribió su marido"),
      ("Que Lía se negará a ser reiniciada", "Lía confirma el reinicio"),
      ("Que la carta se perdió para siempre", "el recuerdo queda en la señora Elena")],
     "Lía traspasa la memoria que está por perder: el gesto da sentido al título."),
    (EVA, "media", "¿Qué tema central plantea el cuento?",
     "El valor de la memoria y los vínculos, aun en una relación con una máquina",
     [("Los peligros de la tecnología para la privacidad", "aparece, pero no es el centro del relato"),
      ("La vida en los hogares de ancianos", "es parte del contexto"),
      ("El funcionamiento técnico de los robots", "no se explica cómo funcionan")],
     "La historia gira en torno a lo que se recuerda y a quién se le confía ese recuerdo."),
])

texto("lectura-placer", "Leer por gusto", """
En los colegios se suele leer por obligación: hay un libro asignado, una fecha de prueba y una nota. Nada de eso está mal en sí mismo; muchos lectores descubrieron sus autores favoritos gracias a una lectura obligatoria. Pero cuando la lectura aparece solo como tarea, es fácil que se asocie con el deber y no con el placer, y que muchos estudiantes dejen de leer apenas terminan la escuela.

Las encuestas muestran que los jóvenes chilenos leen, aunque no siempre lo que los adultos esperan. Leen mensajes, foros, novelas gráficas, sagas de fantasía y textos en internet sobre los temas que les apasionan. Algunos especialistas sostienen que esa lectura también cuenta: exige comprender, relacionar y evaluar información, las mismas habilidades que se miden en cualquier prueba de comprensión.

Otros advierten que no todas las lecturas ejercitan las mismas capacidades. Un texto breve en una pantalla rara vez obliga a sostener la atención durante media hora o a seguir un argumento complejo de principio a fin. Por eso proponen no elegir entre una lectura y otra, sino tender puentes: partir de lo que los estudiantes ya leen para llevarlos hacia textos más extensos y desafiantes.

Algunas escuelas han probado un camino sencillo: dedicar quince minutos diarios a la lectura libre, sin preguntas ni notas, con libros que cada estudiante elige. Los resultados no son inmediatos, pero varios docentes cuentan que, al cabo de unos meses, alumnos que decían odiar la lectura empiezan a pedir el siguiente tomo de una saga. Quizás la mejor manera de formar lectores sea, simplemente, darles tiempo para leer.
""", "Columna elaborada para este ensayo.", [
    (LOC, "baja", "¿Qué propuesta concreta han probado algunas escuelas, según el texto?",
     "Dedicar quince minutos diarios a la lectura libre",
     [("Eliminar las lecturas obligatorias", "no se propone eliminarlas"),
      ("Prohibir los textos en internet", "no se menciona"),
      ("Aumentar las pruebas de lectura", "la lectura libre es sin preguntas ni notas")],
     "El párrafo 4 describe la propuesta."),
    (INT, "media", "Según el párrafo 1, ¿cuál es el riesgo de presentar la lectura solo como tarea?",
     "Que se la asocie con el deber y no con el placer",
     [("Que los estudiantes lean demasiado", "no se plantea"),
      ("Que los profesores no puedan evaluar", "no es el riesgo mencionado"),
      ("Que los libros se encarezcan", "no se habla de precios")],
     "El texto dice que es fácil que la lectura «se asocie con el deber y no con el placer»."),
    (INT, "media", "¿En qué se diferencian las posturas de los párrafos 2 y 3?",
     "La primera valora toda lectura; la segunda advierte que no todas desarrollan las mismas capacidades",
     [("La primera critica internet y la segunda lo defiende", "no es así"),
      ("Ambas proponen eliminar las lecturas obligatorias", "ninguna lo propone"),
      ("La primera habla de adultos y la segunda de niños", "ambas hablan de jóvenes")],
     "El párrafo 3 matiza al 2: los textos breves en pantalla rara vez exigen atención sostenida."),
    (INT, "alta", "¿Qué significa «tender puentes» en el párrafo 3?",
     "Usar lo que los estudiantes ya leen como punto de partida hacia lecturas más exigentes",
     [("Construir bibliotecas en los colegios", "es una expresión figurada"),
      ("Traducir libros a otros idiomas", "no se refiere a traducciones"),
      ("Reemplazar los libros por pantallas", "es lo contrario")],
     "La frase siguiente lo explica: partir de lo que ya leen «para llevarlos hacia textos más extensos y desafiantes»."),
    (EVA, "alta", "¿Qué tipo de evidencia usa el autor para apoyar la propuesta del último párrafo?",
     "Testimonios de docentes sobre cambios observados en sus estudiantes",
     [("Un estudio estadístico con cifras precisas", "no entrega cifras"),
      ("La opinión de un premio Nobel", "no cita autoridades"),
      ("Un experimento de laboratorio", "no hay experimento")],
     "«Varios docentes cuentan que...»: es evidencia testimonial, que el autor presenta con cautela («Quizás»)."),
])

texto("beca-transporte", "Postulación a la beca de transporte", """
Requisitos. Pueden postular estudiantes de enseñanza media de establecimientos municipales o subvencionados de la región que vivan a más de cinco kilómetros de su liceo y que pertenezcan al 60 % de menores ingresos según el Registro Social de Hogares.

Beneficio. La beca cubre el valor del transporte público entre el domicilio y el establecimiento durante el año escolar, mediante una carga mensual en la tarjeta de transporte. No cubre viajes en vacaciones ni traslados a actividades fuera del horario de clases.

Documentos. Al postular se deben adjuntar: un certificado de alumno regular del año en curso, un comprobante de domicilio con no más de tres meses de antigüedad y la cartola del Registro Social de Hogares. Los postulantes menores de 18 años deben hacerlo junto a su apoderado.

Plazos. La postulación se realiza en línea entre el 1 y el 31 de marzo. Los resultados se publicarán la segunda quincena de abril. Quienes no resulten seleccionados podrán apelar dentro de los diez días hábiles siguientes a la publicación, presentando antecedentes nuevos que no hayan sido considerados.

Renovación. La beca debe renovarse cada año. Para mantenerla, el estudiante debe tener una asistencia de al menos un 85 % en el año anterior, salvo inasistencias justificadas por motivos de salud.
""", "Bases ficticias elaboradas para este ensayo.", [
    (LOC, "baja", "¿Hasta cuándo se puede postular a la beca?",
     "Hasta el 31 de marzo",
     [("Hasta la segunda quincena de abril", "en abril se publican los resultados"),
      ("Durante todo el año escolar", "el plazo es de un mes"),
      ("Hasta diez días hábiles después de los resultados", "ese es el plazo de apelación")],
     "El párrafo 4 fija la postulación entre el 1 y el 31 de marzo."),
    (LOC, "media", "¿Cuál de los siguientes gastos NO cubre la beca?",
     "Un viaje a una competencia deportiva un sábado",
     [("El viaje diario de la casa al liceo", "es justamente lo que cubre"),
      ("El regreso del liceo a la casa en un día de clases", "es un traslado entre domicilio y establecimiento"),
      ("El transporte de un martes de clases en junio", "es parte del año escolar")],
     "El párrafo 2 excluye «traslados a actividades fuera del horario de clases»."),
    (INT, "media", "Una estudiante vive a 8 km de su liceo municipal, pertenece al 40 % de menores ingresos y tuvo 80 % de asistencia el año anterior sin justificación. ¿Qué se puede concluir?",
     "Puede postular por primera vez, pero no podría renovar la beca con esa asistencia",
     [("No puede postular porque vive muy lejos", "vivir a más de 5 km es un requisito, no un impedimento"),
      ("Puede renovar la beca sin problemas", "la renovación exige al menos 85 % de asistencia"),
      ("No puede postular porque pertenece al 40 %", "el 40 % está dentro del 60 % de menores ingresos")],
     "Cumple los requisitos de postulación; la asistencia del 85 % se exige para renovar."),
    (INT, "media", "¿Qué condición debe cumplir una apelación?",
     "Presentar antecedentes nuevos dentro de los diez días hábiles siguientes a los resultados",
     [("Presentarse antes del 1 de marzo", "la apelación es posterior a los resultados"),
      ("Repetir los mismos documentos de la postulación", "deben ser antecedentes nuevos"),
      ("Contar con un 85 % de asistencia", "es el requisito de renovación")],
     "El párrafo 4 lo establece."),
    (EVA, "media", "¿Por qué el texto está organizado en apartados con títulos como «Requisitos» o «Plazos»?",
     "Para que el lector encuentre con rapidez la información que necesita para postular",
     [("Para contar la historia de la beca", "no es un relato"),
      ("Para convencer al lector de una opinión", "no es argumentativo"),
      ("Para ocultar las condiciones de la beca", "las presenta de forma explícita")],
     "En textos normativos o administrativos, los apartados facilitan la consulta.")
])
