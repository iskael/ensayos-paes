"""Competencia Lectora, quinta tanda: poema, fragmento dramático, entrevista, texto argumentativo, reglamento y crónica."""
from contenido.lectora import EVA, INT, LOC, texto

texto("poema-cordillera", "Oda breve a la cordillera", """
Cada mañana te levantas antes que nosotros,
vieja espalda de piedra,
y te pones la nieve como quien se pone un abrigo
que ya no le queda grande.

Te miramos desde la micro, entre los cables,
y decimos «qué linda está hoy»
como se dice de una abuela
que nunca supo envejecer del todo.

No sabes de semáforos ni de horarios.
Tu reloj cuenta en glaciares,
y cada verano, más temprano,
se te va quedando sin agujas.

Quédate, te pedimos sin saber cómo,
nosotros, que apenas sabemos quedarnos.
""", "Poema elaborado para este ensayo.", [
    (LOC, "baja", "¿Desde dónde mira el hablante a la cordillera, según la segunda estrofa?",
     "Desde la micro",
     [("Desde la cumbre de un cerro", "el hablante no está en la montaña"),
      ("Desde un glaciar", "los glaciares se mencionan como el «reloj» de la cordillera"),
      ("Desde la casa de su abuela", "la abuela aparece solo en una comparación")],
     "Los versos 5 y 6 dicen: «Te miramos desde la micro, entre los cables»."),
    (INT, "media", "En la primera estrofa, la nieve se compara con:",
     "un abrigo",
     [("una espalda de piedra", "así se nombra a la cordillera, no a la nieve"),
      ("un reloj", "el reloj aparece en la tercera estrofa"),
      ("unos cables", "los cables están en la segunda estrofa")],
     "«Te pones la nieve como quien se pone un abrigo»: es un símil, con el nexo «como»."),
    (INT, "alta", "¿Qué sugieren los versos «y cada verano, más temprano, / se te va quedando sin agujas»?",
     "Que los glaciares de la cordillera se están derritiendo y disminuyendo",
     [("Que la cordillera ya no tiene árboles", "las agujas pertenecen al «reloj» de glaciares"),
      ("Que el tiempo se detuvo en la cordillera", "el reloj se gasta, no se detiene"),
      ("Que los veranos son cada vez más cortos", "lo que llega «más temprano» es la pérdida")],
     "Si el reloj de la cordillera «cuenta en glaciares», perder las agujas es perder hielo, cada año antes."),
    (INT, "media", "¿Qué recurso predomina en todo el poema?",
     "La personificación de la cordillera, a la que se habla como a una persona",
     [("La descripción técnica de la geografía", "no hay datos ni lenguaje técnico"),
      ("La narración de una historia con personajes", "no hay una secuencia de acciones"),
      ("La rima consonante en todos los versos", "el poema está en verso libre")],
     "El hablante se dirige a la cordillera con «tú»: se levanta, se pone abrigo, no sabe de horarios."),
    (EVA, "alta", "¿Qué tensión expresan los dos últimos versos?",
     "El hablante pide permanencia a la cordillera, aunque reconoce que los propios seres humanos son poco constantes",
     [("El hablante rechaza a la cordillera por ser fría", "el poema expresa afecto"),
      ("El hablante celebra que la cordillera cambie", "le pide que se quede"),
      ("El hablante afirma que la cordillera es eterna", "teme que desaparezca")],
     "«Quédate, te pedimos [...] nosotros, que apenas sabemos quedarnos»: la súplica contrasta con la propia fragilidad."),
])

texto("teatro-herencia", "La radio del abuelo (fragmento)", """
(Living de una casa antigua. Cajas de cartón por todas partes. MARTA, de cincuenta años, envuelve platos en papel de diario. Entra TOMÁS, su hijo, de diecisiete, con una radio vieja entre las manos.)

TOMÁS: ¿Y esto? Estaba en el fondo del clóset.

MARTA: (Sin mirar.) A la caja de las cosas para botar.

TOMÁS: Pero si funciona. (La enciende. Se oye estática y, de pronto, un tango.) ¿Ves?

MARTA: (Se detiene. Deja el plato a medio envolver.) Tu abuelo la prendía todos los domingos. Decía que la música sonaba mejor con ese ruidito de fondo.

TOMÁS: ¿Ruidito?

MARTA: La estática. Decía que era el sonido de la distancia. (Pausa.) Yo le decía que era el sonido de un aparato malo.

TOMÁS: (Sonríe.) Y tenías razón.

MARTA: Sí. (Pausa larga. Toma la radio y la pone en la caja de las cosas que se llevan.) Pero él también.
""", "Fragmento dramático elaborado para este ensayo.", [
    (LOC, "baja", "¿Dónde encontró Tomás la radio?",
     "En el fondo del clóset",
     [("En una caja de cartón", "las cajas son para la mudanza"),
      ("En el living, sobre la mesa", "la trae desde otra parte"),
      ("En la casa de su abuelo", "no se menciona otra casa")],
     "Tomás dice: «Estaba en el fondo del clóset»."),
    (INT, "media", "¿Qué función cumplen los textos entre paréntesis?",
     "Indicar acciones, gestos y características de la escena (acotaciones)",
     [("Expresar los pensamientos del narrador", "en el texto dramático no hay narrador"),
      ("Reproducir lo que dicen los personajes en voz baja", "no son parlamentos"),
      ("Explicar el significado de palabras difíciles", "no son notas de vocabulario")],
     "Las acotaciones describen el espacio, los personajes y sus acciones, como «Sin mirar» o «Pausa larga»."),
    (INT, "media", "Según el abuelo, la estática era:",
     "el sonido de la distancia",
     [("el sonido de un aparato malo", "esa era la opinión de Marta"),
      ("parte de un tango", "el tango es la música que suena"),
      ("una molestia que había que reparar", "a él le gustaba ese ruido")],
     "Marta recuerda: «Decía que era el sonido de la distancia»."),
    (INT, "alta", "¿Qué muestra el cambio de actitud de Marta a lo largo del fragmento?",
     "Que el recuerdo de su padre la lleva a valorar un objeto que al principio quería botar",
     [("Que descubre que la radio tiene valor económico", "no se menciona su precio"),
      ("Que se enoja con Tomás por desordenar", "no hay enojo"),
      ("Que decide quedarse a vivir en la casa", "la mudanza continúa")],
     "Primero la manda a «botar» sin mirarla; tras recordar al abuelo, la pone en la caja de lo que se llevan."),
    (EVA, "alta", "¿Qué sentido tiene la última réplica de Marta, «Pero él también»?",
     "Reconoce que la explicación poética de su padre también era verdadera",
     [("Afirma que su padre también tenía una radio mala", "no se refiere a otra radio"),
      ("Quiere decir que Tomás se equivoca", "le dio la razón a Tomás antes"),
      ("Indica que su padre también quería botar la radio", "él la prendía cada domingo")],
     "Marta admite que ambos tenían razón: la radio era defectuosa y, a la vez, su sonido evocaba la distancia y la memoria."),
])

texto("entrevista-vulcanologa", "«Un volcán no avisa con un día de anticipación»", """
La siguiente entrevista es un texto elaborado para este ensayo; la especialista es un personaje ficticio.

—¿Cuántos volcanes activos tiene Chile?
—Alrededor de noventa, según la red de vigilancia. Es una de las cadenas volcánicas más extensas del mundo, porque el país está sobre la zona donde la placa de Nazca se hunde bajo la placa Sudamericana.

—¿Se puede predecir una erupción?
—No como se predice la lluvia de mañana. Lo que hacemos es leer señales: sismos pequeños bajo el volcán, deformación del terreno, cambios en los gases que emite. Cuando esas señales aumentan, subimos la alerta. Pero un volcán no avisa con un día de anticipación; a veces las señales duran meses y no pasa nada, y otras veces la erupción llega en pocas horas.

—Entonces, ¿de qué sirve vigilar?
—De mucho. La alerta permite preparar evacuaciones, cerrar caminos y avisar a los vuelos. En las últimas erupciones del sur, nadie murió por la lava; los mayores riesgos fueron la ceniza y los aluviones de barro, los lahares, que se pueden anticipar si uno sabe por dónde bajarán.

—¿Qué debería saber una familia que vive cerca de un volcán?
—Tres cosas: cuál es su ruta de evacuación, dónde está el punto de encuentro y qué llevar en una mochila de emergencia. Parece poco, pero es lo que más salva vidas.
""", "Entrevista ficticia elaborada para este ensayo.", [
    (LOC, "baja", "¿Cuántos volcanes activos tiene Chile, según la entrevistada?",
     "Alrededor de noventa",
     [("Alrededor de tres", "tres son las cosas que debe saber una familia"),
      ("Más de mil", "no se menciona esa cifra"),
      ("Ninguno", "el texto habla de volcanes activos")],
     "La primera respuesta dice: «Alrededor de noventa, según la red de vigilancia»."),
    (INT, "media", "¿Qué explicación da la entrevistada sobre la gran cantidad de volcanes en Chile?",
     "Que el país está sobre la zona donde la placa de Nazca se hunde bajo la Sudamericana",
     [("Que en Chile llueve poco", "el clima no se menciona"),
      ("Que la red de vigilancia es muy extensa", "la red los cuenta, no los origina"),
      ("Que los volcanes del sur son muy antiguos", "no se menciona su antigüedad")],
     "La subducción de una placa bajo otra genera la cadena volcánica."),
    (INT, "media", "¿A qué se refiere la entrevistada con «leer señales»?",
     "A interpretar sismos, deformación del terreno y cambios en los gases",
     [("A leer los informes de otros países", "se refiere a mediciones del volcán"),
      ("A observar el pronóstico del tiempo", "lo distingue del pronóstico de lluvia"),
      ("A revisar los mapas de evacuación", "eso es parte de la preparación de las familias")],
     "En la misma respuesta enumera las tres señales que se vigilan."),
    (EVA, "alta", "¿Qué propósito tiene comparar la predicción de erupciones con la de la lluvia?",
     "Aclarar que la vigilancia volcánica no permite anunciar fechas exactas",
     [("Mostrar que es más fácil predecir erupciones que lluvias", "dice lo contrario"),
      ("Explicar que la lluvia provoca las erupciones", "no hay relación causal"),
      ("Criticar a los meteorólogos", "no hay crítica")],
     "La comparación sirve para corregir una expectativa: el volcán da señales, no un aviso con fecha."),
    (EVA, "media", "¿Cuál es la principal intención de la última respuesta?",
     "Entregar recomendaciones prácticas de preparación ante una erupción",
     [("Explicar el origen geológico de los volcanes", "eso está en la primera respuesta"),
      ("Describir una erupción reciente", "no describe ninguna"),
      ("Convencer a las familias de mudarse lejos de los volcanes", "no propone mudarse")],
     "Enumera tres acciones concretas: ruta, punto de encuentro y mochila de emergencia."),
])

texto("columna-reparar", "Reparar en vez de botar", """
Hace treinta años, cuando un televisor fallaba, se llevaba al técnico de la esquina. Hoy, si se rompe la pantalla de un celular, muchas veces resulta más barato comprar otro. No es que hayamos olvidado cómo reparar: es que los productos se diseñan para que sea difícil hacerlo.

Las baterías pegadas, los tornillos con formas especiales y la falta de repuestos a la venta convierten pequeñas fallas en el fin de un aparato. El resultado se ve en los vertederos: los residuos electrónicos son uno de los tipos de basura que más crece en el mundo, y en su mayoría no se reciclan.

Algunos países han comenzado a exigir que los fabricantes vendan repuestos durante varios años y publiquen manuales de reparación. Los críticos responden que esas reglas encarecen los productos y frenan la innovación, porque obligan a diseños más voluminosos. Es un argumento que merece atención, pero no convence del todo: un teléfono que dura el doble cuesta, en la práctica, la mitad.

Reparar no es nostalgia. Es una forma de ahorrar, de generar empleo local y de reducir basura. Basta con que la ley haga posible lo que el sentido común ya pide.
""", "Columna de opinión elaborada para este ensayo.", [
    (LOC, "baja", "Según el texto, ¿cuál es una de las razones por las que hoy es difícil reparar un aparato?",
     "Las baterías pegadas y los tornillos con formas especiales",
     [("La falta de técnicos en las ciudades", "el texto no lo atribuye a eso"),
      ("La prohibición legal de abrir los aparatos", "no hay tal prohibición"),
      ("El alto precio de los manuales", "el problema es que no se publican")],
     "El párrafo 2 menciona baterías pegadas, tornillos especiales y falta de repuestos."),
    (INT, "media", "¿Cuál es la tesis del autor?",
     "La ley debería facilitar la reparación de los productos, porque trae beneficios económicos y ambientales",
     [("Los aparatos antiguos eran de mejor calidad que los actuales", "es solo el punto de partida"),
      ("La innovación tecnológica debe detenerse", "no propone eso"),
      ("Reciclar es mejor que reparar", "defiende la reparación")],
     "La conclusión pide que «la ley haga posible» reparar, por el ahorro, el empleo y la menor basura."),
    (INT, "media", "¿Qué función cumple el párrafo 3?",
     "Presentar medidas de otros países, exponer una objeción y responderla",
     [("Describir cómo se repara un celular", "no hay instrucciones"),
      ("Entregar cifras de reciclaje", "las cifras no aparecen"),
      ("Resumir la tesis del texto", "eso lo hace el último párrafo")],
     "Menciona leyes de otros países, la crítica sobre costos e innovación y la contraargumentación del autor."),
    (EVA, "alta", "¿Con qué argumento el autor responde a quienes dicen que las reglas encarecen los productos?",
     "Un producto que dura más resulta, en la práctica, más barato",
     [("Los fabricantes ganan demasiado dinero", "no lo dice"),
      ("La innovación no es importante", "no desestima la innovación"),
      ("Los productos voluminosos son más bonitos", "no se refiere a la estética")],
     "«Un teléfono que dura el doble cuesta, en la práctica, la mitad»."),
    (EVA, "alta", "¿Qué efecto busca la frase «Reparar no es nostalgia»?",
     "Anticipar y descartar la idea de que defender la reparación es añorar el pasado",
     [("Expresar tristeza por el pasado", "niega justamente ese sentimiento"),
      ("Recomendar comprar aparatos antiguos", "no hace esa recomendación"),
      ("Criticar a los técnicos de antes", "no hay crítica a ellos")],
     "El autor abrió con un recuerdo de hace treinta años; con esa frase evita que su postura se lea como simple añoranza."),
])

texto("reglamento-bicicletas", "Reglamento del sistema de bicicletas compartidas", """
El presente reglamento corresponde a un servicio ficticio, elaborado para este ensayo.

Artículo 1. Pueden inscribirse en el sistema las personas mayores de 15 años. Los menores de 18 años necesitan la autorización de un adulto responsable.

Artículo 2. Cada usuario puede usar una bicicleta por un máximo de 45 minutos seguidos. Si se supera ese tiempo, se cobrará una multa por cada 15 minutos adicionales o fracción.

Artículo 3. La bicicleta debe devolverse en cualquier estación del sistema, anclada correctamente hasta que la luz del anclaje cambie a verde. Una bicicleta que no quede anclada se considera no devuelta.

Artículo 4. Si la bicicleta presenta una falla, el usuario debe devolverla en la estación más cercana y presionar el botón rojo del anclaje. En ese caso, no se cobrará el tiempo excedido.

Artículo 5. Tres multas impagas en un mismo año implican la suspensión de la cuenta hasta que se regularice la deuda.
""", "Texto funcional elaborado para este ensayo.", [
    (LOC, "baja", "¿Cuál es la edad mínima para inscribirse en el sistema?",
     "15 años",
     [("18 años", "es la edad desde la que no se necesita autorización"),
      ("45 años", "45 son los minutos de uso"),
      ("No hay edad mínima", "el artículo 1 la establece")],
     "El artículo 1 permite la inscripción a mayores de 15 años."),
    (INT, "media", "Una usuaria usa una bicicleta durante 70 minutos seguidos, sin fallas. ¿Cuántas multas se le cobran?",
     "Dos",
     [("Una", "los 25 minutos extra incluyen una fracción de un segundo período de 15"),
      ("Ninguna", "superó los 45 minutos"),
      ("Cinco", "cuenta períodos de 15 desde el inicio")],
     "70 − 45 = 25 minutos adicionales: un período completo de 15 y una fracción, que también se cobra."),
    (INT, "media", "Según el artículo 3, ¿cuándo se considera devuelta una bicicleta?",
     "Cuando queda anclada en una estación y la luz del anclaje cambia a verde",
     [("Cuando se deja junto a cualquier estación", "debe quedar anclada"),
      ("Cuando se avisa por teléfono", "no se menciona esa opción"),
      ("Cuando han pasado 45 minutos", "el tiempo no define la devolución")],
     "El artículo exige anclarla «hasta que la luz del anclaje cambie a verde»."),
    (INT, "alta", "Un usuario nota que la cadena se cortó a los 50 minutos de uso, la devuelve en la estación más cercana y presiona el botón rojo. ¿Qué indica el reglamento?",
     "No se le cobra el tiempo excedido",
     [("Se le cobra una multa por los 5 minutos adicionales", "el artículo 4 lo exime"),
      ("Su cuenta queda suspendida", "la suspensión requiere tres multas impagas"),
      ("Debe pagar la reparación de la bicicleta", "no se menciona ese cobro")],
     "El artículo 4 señala que, si hay una falla y se informa con el botón rojo, no se cobra el tiempo excedido."),
    (EVA, "media", "¿Cuál es el propósito principal de este texto?",
     "Establecer las normas de uso del servicio y sus consecuencias",
     [("Convencer a las personas de usar la bicicleta", "no tiene un propósito persuasivo"),
      ("Narrar la experiencia de un usuario", "no es un relato"),
      ("Explicar cómo se fabrican las bicicletas", "no se refiere a su fabricación")],
     "Es un texto normativo: los artículos fijan obligaciones, plazos y sanciones."),
])

texto("cronica-feria", "Sábado en la feria", """
A las seis de la mañana, cuando la calle todavía es de los perros y del camión de la basura, don Julio ya está armando su puesto. Primero los fierros, después el toldo azul, después los cajones de tomates puestos en escalera, del más verde al más rojo, «para que la gente elija con los ojos».

A las ocho llegan las primeras caseras con sus carros de dos ruedas. Don Julio las conoce por lo que compran: la señora de las paltas, el caballero del cilantro, la profesora que pregunta siempre si hay duraznos aunque sea invierno. A todas les dice «mi reina» y a todos «jefe», y nadie parece molestarse.

Al mediodía la feria es un solo ruido. Los gritos de los vendedores compiten con los parlantes de un puesto de música y con el chirrido de los carros. Don Julio baja los precios de lo que no aguantará hasta el martes y regala una mandarina a cada niño que pasa de la mano de su mamá.

A las tres, los cajones están vacíos y el toldo azul vuelve a ser un bulto amarrado. Antes de irse, don Julio barre su pedazo de calle. «La calle es prestada», dice, y se va con el sol de frente.
""", "Crónica elaborada para este ensayo.", [
    (LOC, "baja", "¿A qué hora empieza don Julio a armar su puesto?",
     "A las seis de la mañana",
     [("A las ocho", "a esa hora llegan las primeras caseras"),
      ("Al mediodía", "a esa hora la feria está en su punto más ruidoso"),
      ("A las tres", "a esa hora termina")],
     "El texto comienza: «A las seis de la mañana [...] don Julio ya está armando su puesto»."),
    (INT, "media", "¿Por qué don Julio ordena los tomates «del más verde al más rojo»?",
     "Para que los clientes puedan elegir según su madurez con solo mirarlos",
     [("Porque los tomates verdes son más caros", "no se mencionan precios distintos"),
      ("Porque así ocupan menos espacio", "no es la razón que da"),
      ("Porque los rojos son los que nadie compra", "no se dice eso")],
     "Él mismo lo explica: «para que la gente elija con los ojos»."),
    (INT, "media", "¿Cómo está organizado el texto?",
     "Cronológicamente, siguiendo las horas de un día de feria",
     [("Por causas y consecuencias", "no explica causas"),
      ("Como una comparación entre dos ferias", "describe una sola feria"),
      ("A partir de una pregunta y su respuesta", "no hay pregunta inicial")],
     "Cada párrafo comienza con una hora: seis, ocho, mediodía y tres."),
    (INT, "alta", "¿Qué rasgo de don Julio se destaca a lo largo de la crónica?",
     "Su cercanía con la gente y su cuidado por el espacio común",
     [("Su interés exclusivo por ganar dinero", "regala mandarinas y baja precios"),
      ("Su mal humor con los clientes", "trata a todos con afecto"),
      ("Su deseo de cambiar de trabajo", "no se menciona")],
     "Conoce a sus clientes, regala fruta a los niños y barre su pedazo de calle antes de irse."),
    (EVA, "alta", "¿Qué sentido tiene la frase final de don Julio, «La calle es prestada»?",
     "Expresa que el espacio público se debe cuidar porque pertenece a todos",
     [("Indica que don Julio arrienda su puesto", "no habla de arriendo"),
      ("Señala que la feria se cambiará de calle", "no se anuncia un cambio"),
      ("Muestra que don Julio no quiere volver", "vuelve cada semana")],
     "Explica por qué barre: usa un espacio que no es suyo y lo devuelve limpio."),
])
