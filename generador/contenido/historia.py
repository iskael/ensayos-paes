"""Historia y Ciencias Sociales: Historia (Mundo, América y Chile), Formación ciudadana y Sistema económico (temario 2026)."""
from nucleo import fijo


def H(eje, dificultad, enunciado, correcta, distractores, pasos):
    fijo("HCS", eje, dificultad, enunciado, correcta, distractores, pasos)


HI, FC, SE = "historia", "formacion_ciudadana", "sistema_economico"

# ---------------- Siglo XIX: Estado-nación, liberalismo, república en Chile

H(HI, "baja", "¿Cuál de los siguientes principios es propio del liberalismo político del siglo XIX?",
  "La separación de los poderes del Estado y la protección de las libertades individuales",
  [("La concentración del poder en un monarca absoluto", "es un rasgo del absolutismo, al que el liberalismo se opuso"),
   ("La abolición de la propiedad privada", "es una idea socialista; el liberalismo defendía la propiedad"),
   ("El gobierno de un partido único", "es propio de los totalitarismos del siglo XX")],
  "El liberalismo defendió las constituciones, la separación de poderes, la soberanía nacional y derechos como la libertad de expresión y de propiedad.")

H(HI, "media", "Durante el siglo XIX, Italia y Alemania se unificaron como Estados nacionales. ¿Qué idea impulsó principalmente estos procesos?",
  "El nacionalismo, que proponía que cada nación con una cultura común tuviera su propio Estado",
  [("El internacionalismo obrero", "buscaba la unión de los trabajadores por sobre las naciones"),
   ("El absolutismo monárquico", "defendía el poder del rey, no la nación"),
   ("La descolonización", "es un proceso del siglo XX en Asia y África")],
  "El nacionalismo vinculó lengua, historia y territorio con la idea de un Estado propio; Italia culminó su unificación en 1870 y Alemania en 1871.")

H(HI, "media", "¿Qué característica tuvo la Constitución chilena de 1833?",
  "Estableció un régimen presidencialista, centralizado y con la religión católica como oficial",
  [("Separó la Iglesia del Estado", "la separación llegó con la Constitución de 1925"),
   ("Creó un régimen parlamentario con un presidente sin poder", "fortaleció la figura presidencial"),
   ("Estableció el voto universal femenino", "el voto femenino en elecciones presidenciales es de 1949")],
  "La Constitución de 1833, asociada al orden conservador, dio amplias atribuciones al presidente y rigió hasta 1925.")

H(HI, "media", "¿Qué consecuencia económica tuvo para Chile la Guerra del Pacífico (1879-1884)?",
  "La incorporación de territorios salitreros, cuya exportación se convirtió en la principal fuente de ingresos fiscales",
  [("La pérdida de todos sus puertos en el norte", "Chile ganó territorios en el norte"),
   ("El inicio de la explotación del cobre en gran escala", "el gran auge del cobre es del siglo XX"),
   ("La nacionalización de las empresas extranjeras", "las salitreras quedaron en buena parte en manos de capitales británicos")],
  "Con Tarapacá y Antofagasta, Chile obtuvo el salitre, cuyos impuestos financiaron al Estado hasta la crisis de 1929.")

H(HI, "media", "¿A qué se denominó «cuestión social» en el Chile de fines del siglo XIX y comienzos del XX?",
  "Al conjunto de problemas de vivienda, salud y trabajo que afectaban a los sectores populares urbanos y mineros",
  [("Al debate sobre la separación de la Iglesia y el Estado", "fue un tema político, no la cuestión social"),
   ("A la discusión sobre los límites con Argentina", "es un tema de política exterior"),
   ("Al conflicto entre el presidente y el Congreso en 1891", "fue la guerra civil de 1891")],
  "Hacinamiento en conventillos, epidemias, jornadas extensas y bajos salarios dieron origen a movimientos obreros y a las primeras leyes sociales.")

H(HI, "alta", "La matanza de la Escuela Santa María de Iquique, en 1907, se relaciona con:",
  "la represión de una huelga de trabajadores del salitre que exigían mejores condiciones",
  [("la Guerra del Pacífico", "ocurrió más de veinte años después de la guerra"),
   ("la reforma agraria", "la reforma agraria es de la década de 1960"),
   ("la guerra civil de 1891", "es un conflicto distinto entre el presidente y el Congreso")],
  "Los obreros pampinos se concentraron en Iquique para pedir, entre otras cosas, el pago en dinero y no en fichas; el Ejército disparó contra ellos.")

H(HI, "media", "¿Qué estableció la Ley de Instrucción Primaria Obligatoria de 1920?",
  "Que la educación primaria fuera obligatoria y gratuita en las escuelas del Estado",
  [("Que la universidad fuera gratuita", "se refería a la educación primaria"),
   ("Que la educación quedara a cargo exclusivo de la Iglesia", "fortaleció el rol del Estado"),
   ("Que solo los hombres asistieran a la escuela", "era obligatoria para niños y niñas")],
  "La ley buscó reducir el analfabetismo, uno de los problemas señalados por la cuestión social.")

H(HI, "media", "¿Qué cambio institucional introdujo la Constitución de 1925 en Chile?",
  "La separación de la Iglesia y el Estado y el fortalecimiento del presidente frente al Congreso",
  [("La creación del sistema parlamentario", "puso fin al periodo parlamentario"),
   ("La declaración del catolicismo como religión oficial", "eso lo hacía la Constitución de 1833"),
   ("La supresión del Congreso", "el Congreso siguió existiendo")],
  "La Constitución de 1925 restableció un régimen presidencial y consagró la libertad de culto.")

# ---------------- Primera mitad del siglo XX

H(HI, "media", "¿Qué efecto tuvo la crisis económica de 1929 en Chile?",
  "Una fuerte caída de las exportaciones de salitre y cobre, con alto desempleo",
  [("Un aumento del precio del salitre", "la demanda mundial cayó"),
   ("El inicio de la Guerra del Pacífico", "la guerra es del siglo XIX"),
   ("La llegada masiva de inversiones extranjeras", "las inversiones se retrajeron")],
  "Chile, muy dependiente de sus exportaciones, fue uno de los países más afectados: miles de desempleados del norte llegaron a las ciudades.")

H(HI, "alta", "Después de la crisis de 1929, Chile impulsó la industrialización por sustitución de importaciones. ¿En qué consistió?",
  "En que el Estado fomentó la producción nacional de bienes que antes se importaban",
  [("En eliminar todos los aranceles a las importaciones", "se protegió la industria nacional con aranceles"),
   ("En privatizar las empresas públicas", "el Estado asumió un rol activo, creando empresas"),
   ("En exportar solo materias primas sin procesar", "buscaba reducir esa dependencia")],
  "La creación de la Corfo en 1939, bajo el gobierno de Pedro Aguirre Cerda, fue clave en ese modelo de desarrollo hacia adentro.")

H(HI, "media", "¿Cuál de los siguientes rasgos es común a los totalitarismos europeos del siglo XX, como el nazismo y el estalinismo?",
  "El control del Estado por un partido único y el uso de la propaganda y la represión",
  [("La existencia de elecciones libres y competitivas", "los totalitarismos suprimieron las elecciones libres"),
   ("La protección de la libertad de prensa", "controlaron los medios de comunicación"),
   ("La separación efectiva de los poderes del Estado", "concentraron el poder en el líder y el partido")],
  "Los totalitarismos buscaron controlar todos los ámbitos de la vida, con culto al líder, partido único, propaganda y policía política.")

H(HI, "media", "¿Qué caracterizó a los gobiernos populistas latinoamericanos de mediados del siglo XX, como los de Perón en Argentina y Vargas en Brasil?",
  "Un liderazgo carismático que buscó apoyo de los trabajadores urbanos con políticas sociales y un Estado activo",
  [("La reducción del Estado al mínimo", "el Estado tuvo un papel central en la economía"),
   ("El rechazo total a los sindicatos", "se apoyaron en los sindicatos"),
   ("La entrega de la economía a potencias extranjeras", "promovieron el nacionalismo económico")],
  "El populismo combinó industrialización, derechos laborales y una relación directa del líder con las masas.")

H(HI, "media", "El Estado de bienestar que se extendió tras la crisis de 1929 se caracterizó por:",
  "la intervención del Estado para garantizar empleo, salud, educación y previsión social",
  [("la eliminación de los impuestos", "requería impuestos para financiar los servicios"),
   ("la abolición de la propiedad privada", "operó en economías capitalistas"),
   ("la reducción de los derechos laborales", "amplió los derechos sociales")],
  "Inspirado en ideas como las de Keynes, el Estado asumió un rol activo para evitar el desempleo y proteger a la población.")

H(HI, "media", "¿En qué año se aprobó en Chile el derecho a voto de las mujeres en las elecciones presidenciales y parlamentarias?",
  "En 1949",
  [("En 1810", "corresponde a la Primera Junta de Gobierno"),
   ("En 1925", "en 1925 se aprobó una nueva Constitución, sin voto femenino pleno"),
   ("En 1988", "es el año del plebiscito")],
  "Las mujeres votaron desde 1934 en elecciones municipales; la ley de 1949 les dio el voto pleno y en 1952 votaron por primera vez en una presidencial.")

# ---------------- Posguerra y Guerra Fría

H(HI, "baja", "¿Con qué objetivo principal se creó la Organización de las Naciones Unidas en 1945?",
  "Mantener la paz y la seguridad internacionales y promover la cooperación entre los países",
  [("Unificar a todos los países bajo un solo gobierno", "la ONU respeta la soberanía de sus miembros"),
   ("Formar una alianza militar contra la Unión Soviética", "eso describe a la OTAN"),
   ("Administrar las colonias europeas", "la ONU apoyó procesos de descolonización")],
  "La ONU nació tras la Segunda Guerra Mundial para evitar nuevos conflictos y fomentar el respeto de los derechos humanos.")

H(HI, "media", "¿Qué importancia tiene la Declaración Universal de los Derechos Humanos de 1948?",
  "Estableció un conjunto de derechos que se reconocen a todas las personas por el hecho de serlo",
  [("Fue la primera constitución de Chile", "es un documento internacional de la ONU"),
   ("Creó la Unión Europea", "la UE surgió después, por otros tratados"),
   ("Puso fin a la Guerra Fría", "la Guerra Fría terminó hacia 1991")],
  "Tras las atrocidades de la guerra, la Declaración fijó derechos universales, inalienables e indivisibles.")

H(HI, "media", "¿Qué fue la Guerra Fría?",
  "El enfrentamiento político, ideológico y económico entre Estados Unidos y la Unión Soviética, sin guerra directa entre ambos",
  [("Una guerra armada entre Estados Unidos y la Unión Soviética en Europa", "nunca se enfrentaron directamente en una guerra"),
   ("El conflicto entre Chile y Perú por el salitre", "es la Guerra del Pacífico"),
   ("La guerra entre Alemania y Francia en 1870", "es la guerra franco-prusiana")],
  "Las superpotencias compitieron por áreas de influencia, carrera armamentista y espacial, y conflictos en otros países.")

H(HI, "media", "¿Qué fue la descolonización ocurrida después de la Segunda Guerra Mundial?",
  "El proceso por el cual colonias de Asia y África obtuvieron su independencia de las potencias europeas",
  [("La independencia de los países de América Latina", "ocurrió a comienzos del siglo XIX"),
   ("La conquista de África por Europa", "fue el reparto colonial del siglo XIX"),
   ("La caída del Muro de Berlín", "es de 1989 y se relaciona con el fin de la Guerra Fría")],
  "India (1947), Indonesia y numerosos países africanos en las décadas de 1950 y 1960 lograron su independencia.")

H(HI, "media", "¿Qué simbolizó la caída del Muro de Berlín en 1989?",
  "El fin de la división de Europa en bloques y el debilitamiento del bloque soviético",
  [("El comienzo de la Segunda Guerra Mundial", "la guerra comenzó en 1939"),
   ("La creación de la ONU", "la ONU es de 1945"),
   ("El inicio de la Guerra Fría", "marcó su fase final")],
  "El muro, levantado en 1961, dividía Berlín; su caída anticipó la reunificación alemana en 1990 y la disolución de la URSS en 1991.")

# ---------------- Chile en la segunda mitad del siglo XX

H(HI, "media", "A mediados del siglo XX, ¿qué fenómeno explica el crecimiento de las «poblaciones callampa» en Santiago?",
  "La migración masiva desde el campo a la ciudad sin viviendas suficientes para recibirla",
  [("El aumento de la natalidad en el barrio alto", "no explica asentamientos precarios"),
   ("La llegada de inmigrantes europeos ricos", "no corresponde a ese fenómeno"),
   ("La reforma agraria de la década de 1990", "la reforma agraria fue en los años sesenta")],
  "Miles de familias campesinas llegaron buscando trabajo y se instalaron en terrenos sin urbanizar, con viviendas precarias.")

H(HI, "media", "¿Cuál fue el objetivo de la reforma agraria impulsada en Chile entre 1962 y 1973?",
  "Redistribuir la tierra concentrada en latifundios y mejorar la situación de los campesinos",
  [("Privatizar las empresas del cobre", "el cobre se nacionalizó en 1971"),
   ("Aumentar el tamaño de los latifundios", "buscaba lo contrario"),
   ("Trasladar a los campesinos a las ciudades", "buscaba mejorar su vida en el campo")],
  "Iniciada por Alessandri, profundizada por Frei Montalva y acelerada por Allende, expropió latifundios para entregarlos a campesinos.")

H(HI, "media", "¿Qué medida tomó el gobierno de Salvador Allende con la gran minería del cobre en 1971?",
  "La nacionalizó, con la aprobación unánime del Congreso",
  [("La vendió a empresas estadounidenses", "las empresas estadounidenses eran las propietarias antes de la nacionalización"),
   ("La cerró por falta de rentabilidad", "siguió funcionando bajo control estatal"),
   ("La entregó a los trabajadores como propiedad privada", "pasó a manos del Estado")],
  "La reforma constitucional de 1971 traspasó al Estado las grandes minas de cobre; fue aprobada por todos los sectores políticos.")

H(HI, "alta", "Sobre el golpe de Estado de 1973 existen distintas interpretaciones historiográficas. ¿Qué afirmación describe mejor esta situación?",
  "Los historiadores discrepan sobre sus causas, pero coinciden en que significó el quiebre de la democracia",
  [("Todos los historiadores le atribuyen una única causa", "el temario pide comparar interpretaciones diversas"),
   ("No existe ninguna fuente sobre el golpe", "hay abundantes fuentes"),
   ("El golpe no tuvo consecuencias en la democracia chilena", "dio paso a diecisiete años de dictadura")],
  "Unas interpretaciones enfatizan la polarización y la crisis económica, otras la intervención externa o la decisión de las Fuerzas Armadas; el resultado fue el fin del régimen democrático.")

H(HI, "media", "¿Qué características tuvo el modelo económico implementado durante la Dictadura Militar?",
  "Apertura al comercio exterior, privatización de empresas públicas y reducción del rol del Estado",
  [("Nacionalización de la banca y de las industrias", "se privatizaron empresas"),
   ("Protección de la industria nacional con altos aranceles", "los aranceles se redujeron"),
   ("Expansión de la reforma agraria", "se devolvió parte de la tierra expropiada")],
  "Bajo la influencia de economistas formados en Chicago, se aplicó un modelo neoliberal; en 1980 se creó el sistema de AFP.")

H(HI, "media", "¿Qué hecho permitió iniciar la transición a la democracia en Chile?",
  "El triunfo de la opción «No» en el plebiscito de 1988",
  [("La aprobación de la Constitución de 1925", "es muy anterior"),
   ("La nacionalización del cobre", "es de 1971"),
   ("La creación de la Corfo", "es de 1939")],
  "El triunfo del «No» llevó a las elecciones de 1989; en marzo de 1990 asumió Patricio Aylwin.")

H(HI, "alta", "¿Qué labor cumplió la Comisión Nacional de Verdad y Reconciliación (Comisión Rettig), cuyo informe se entregó en 1991?",
  "Investigó y documentó las violaciones a los derechos humanos con resultado de muerte y desaparición durante la dictadura",
  [("Redactó una nueva Constitución", "no tuvo función constituyente"),
   ("Juzgó y condenó a los responsables", "no era un tribunal"),
   ("Organizó el plebiscito de 1988", "es posterior al plebiscito")],
  "El Informe Rettig estableció la verdad sobre ejecutados y detenidos desaparecidos; luego, la Comisión Valech abordó la prisión política y la tortura.")

H(HI, "alta", "Considera el siguiente fragmento, elaborado para esta pregunta a partir de los diagnósticos de salud pública de fines de la década de 1930: «Muchos niños nacen en hogares sin agua potable, y la mortalidad infantil en Chile es una de las más altas del continente». ¿Qué tema histórico ilustra mejor este fragmento?",
  "Las precarias condiciones de vida de los sectores populares a mediados del siglo XX",
  [("Los efectos de la Guerra del Pacífico", "la fuente es de 1939 y no habla de la guerra"),
   ("El auge económico del salitre", "describe pobreza, no auge"),
   ("La apertura económica de la década de 1980", "es una fuente anterior")],
  "Analizar una fuente exige ubicarla en su contexto: a fines de los años treinta la pobreza y la salud pública eran problemas centrales del país.")

# ---------------- Formación ciudadana

H(FC, "baja", "Según la Constitución chilena, ¿qué requisitos debe cumplir una persona para ser ciudadana?",
  "Ser chilena, tener 18 años cumplidos y no haber sido condenada a pena aflictiva",
  [("Ser chilena y tener 21 años cumplidos", "la mayoría de edad para la ciudadanía es 18 años"),
   ("Saber leer y escribir y tener propiedades", "esos requisitos censitarios ya no existen"),
   ("Haber nacido en Santiago", "no hay requisito de lugar de nacimiento dentro del país")],
  "La ciudadanía otorga derechos políticos, como votar y optar a cargos de elección popular.")

H(FC, "baja", "¿Qué institución ejerce el poder legislativo en Chile?",
  "El Congreso Nacional, formado por la Cámara de Diputadas y Diputados y el Senado",
  [("La Corte Suprema", "encabeza el Poder Judicial"),
   ("El Presidente de la República", "encabeza el Poder Ejecutivo, aunque colabora en la formación de las leyes"),
   ("La Contraloría General de la República", "controla la legalidad de los actos de la administración")],
  "El Congreso bicameral discute y aprueba las leyes, y fiscaliza al gobierno a través de la Cámara.")

H(FC, "media", "¿Qué significa que en Chile exista un Estado de derecho?",
  "Que gobernantes y gobernados están sometidos a la Constitución y a las leyes",
  [("Que el Estado puede actuar sin límites para mantener el orden", "el Estado de derecho limita el poder"),
   ("Que solo los ciudadanos deben cumplir las leyes", "también las autoridades"),
   ("Que el Presidente puede cambiar las leyes por decreto cuando quiera", "las leyes se aprueban en el Congreso")],
  "En un Estado de derecho el poder se ejerce conforme a normas, con separación de poderes y respeto de los derechos fundamentales.")

H(FC, "media", "Una persona considera que una decisión arbitraria de una autoridad vulnera su derecho a la igualdad ante la ley. ¿Qué acción judicial puede presentar?",
  "Un recurso de protección ante la Corte de Apelaciones",
  [("Un plebiscito comunal", "es un mecanismo de participación, no una acción judicial"),
   ("Una iniciativa popular de ley", "sirve para proponer leyes, no para proteger un derecho vulnerado"),
   ("Una cuenta pública", "es un informe de la autoridad")],
  "El recurso de protección resguarda los derechos constitucionales frente a actos u omisiones arbitrarios o ilegales.")

H(FC, "media", "¿Qué derecho protege el recurso de amparo, también llamado habeas corpus?",
  "La libertad personal y la seguridad individual frente a detenciones ilegales",
  [("El derecho de propiedad sobre un inmueble", "se protege con otras acciones"),
   ("El derecho a votar en las elecciones", "no es el objeto del amparo"),
   ("La libertad de enseñanza", "se puede proteger mediante el recurso de protección")],
  "El amparo puede ser presentado por quien es arrestado, detenido o preso con infracción de la Constitución o las leyes.")

H(FC, "media", "¿Cuál es la función principal del Tribunal Constitucional?",
  "Velar por que las leyes y otras normas se ajusten a la Constitución",
  [("Juzgar delitos comunes", "eso lo hacen los tribunales penales"),
   ("Elegir al Presidente de la República", "el Presidente se elige por votación popular"),
   ("Administrar el presupuesto de la nación", "es tarea del Ejecutivo con aprobación del Congreso")],
  "El Tribunal Constitucional controla la constitucionalidad de leyes y otros preceptos.")

H(FC, "media", "¿Cuál de las siguientes es una forma de participación ciudadana distinta del voto?",
  "Integrar una junta de vecinos para proponer mejoras al barrio",
  [("Pagar el impuesto al valor agregado al comprar", "es una obligación tributaria"),
   ("Obtener la cédula de identidad", "es un trámite, no una forma de participación"),
   ("Cumplir con el horario de trabajo", "es una obligación laboral")],
  "Las organizaciones comunitarias, las consultas ciudadanas y los consejos de la sociedad civil son formas de participación.")

H(FC, "alta", "¿Por qué la libertad de prensa se considera fundamental en una democracia?",
  "Porque permite a la ciudadanía informarse y fiscalizar a quienes ejercen el poder",
  [("Porque obliga a todos los medios a apoyar al gobierno", "la libertad de prensa supone independencia"),
   ("Porque reemplaza el voto como forma de elegir autoridades", "no reemplaza las elecciones"),
   ("Porque impide que existan opiniones distintas", "protege la diversidad de opiniones")],
  "Sin información libre, la ciudadanía no puede formarse opiniones ni exigir rendición de cuentas.")

H(FC, "media", "¿Qué son los derechos humanos?",
  "Derechos inherentes a todas las personas, universales e inalienables",
  [("Privilegios que el Estado concede solo a los ciudadanos", "corresponden a todas las personas, ciudadanas o no"),
   ("Normas que solo rigen en tiempo de guerra", "rigen siempre"),
   ("Derechos que se pueden vender o transferir", "son inalienables")],
  "Los derechos humanos no dependen de la nacionalidad, el sexo, la edad u otra condición, y el Estado debe respetarlos y garantizarlos.")

H(FC, "alta", "En una democracia, ¿por qué es importante que existan partidos políticos diversos?",
  "Porque canalizan distintas visiones de la sociedad y permiten que la ciudadanía elija entre alternativas",
  [("Porque garantizan que siempre gobierne el mismo partido", "la alternancia es propia de la democracia"),
   ("Porque reemplazan la Constitución", "actúan dentro del marco constitucional"),
   ("Porque eliminan la necesidad de elecciones", "compiten en las elecciones")],
  "El pluralismo político es una condición de la democracia: sin alternativas no hay elección real.")

H(FC, "media", "¿Cuál es la función de la Contraloría General de la República?",
  "Controlar la legalidad de los actos de la administración del Estado y el uso de los recursos públicos",
  [("Dictar sentencias en causas penales", "es tarea de los tribunales"),
   ("Proponer las leyes de presupuesto", "las propone el Ejecutivo"),
   ("Representar a Chile ante otros países", "es tarea del Presidente y la Cancillería")],
  "La Contraloría es un órgano autónomo que fiscaliza a la administración pública.")

H(FC, "alta", "Una municipalidad organiza una consulta para decidir en qué se usará parte de su presupuesto. ¿Qué principio democrático fortalece principalmente esta medida?",
  "La participación ciudadana en las decisiones públicas",
  [("La separación de los poderes del Estado", "no involucra a los poderes del Estado"),
   ("La independencia del Poder Judicial", "no se relaciona con los tribunales"),
   ("La supremacía constitucional", "no trata de la jerarquía de las normas")],
  "Los presupuestos participativos permiten que la comunidad incida directamente en el uso de recursos públicos.")

# ---------------- Sistema económico

H(SE, "baja", "¿Cuál es el problema económico fundamental que enfrentan todas las sociedades?",
  "La escasez: los recursos son limitados frente a necesidades ilimitadas",
  [("La abundancia de recursos naturales", "si sobraran recursos no habría que elegir"),
   ("La existencia del dinero", "el dinero facilita el intercambio, no es el problema fundamental"),
   ("La falta de bancos", "no es el problema de fondo")],
  "Como los recursos no alcanzan para todo, personas, empresas y Estados deben elegir cómo usarlos.")

H(SE, "media", "Una estudiante decide trabajar los sábados en vez de asistir a un preuniversitario. ¿Cuál es el costo de oportunidad de su decisión?",
  "Las clases de preuniversitario a las que renuncia",
  [("El sueldo que recibe por trabajar", "es lo que gana, no lo que deja"),
   ("El precio del transporte al trabajo", "es un costo directo, no la alternativa sacrificada"),
   ("No tiene costo, porque recibe dinero", "toda elección implica renunciar a algo")],
  "El costo de oportunidad es el valor de la mejor alternativa a la que se renuncia al elegir.")

H(SE, "media", "Si el precio de un bien aumenta y todo lo demás se mantiene constante, ¿qué ocurre, según la ley de la demanda?",
  "La cantidad demandada de ese bien disminuye",
  [("La cantidad demandada aumenta", "es lo contrario de la ley de la demanda"),
   ("La oferta del bien desaparece", "la oferta tiende a aumentar con el precio"),
   ("La cantidad demandada no cambia nunca", "solo en bienes muy especiales es poco sensible")],
  "Con un precio mayor, los consumidores compran menos de ese bien o buscan sustitutos.")

H(SE, "media", "Una helada destruye gran parte de la cosecha de paltas. ¿Qué efecto se espera en el mercado de la palta?",
  "Disminuye la oferta y sube el precio",
  [("Aumenta la oferta y baja el precio", "la helada reduce la cantidad disponible"),
   ("Aumenta la demanda y baja el precio", "la helada afecta la oferta, no la demanda"),
   ("No cambia nada, porque el precio lo fija el Estado", "en un mercado libre el precio responde a la oferta y la demanda")],
  "Con menos paltas disponibles y la misma demanda, el precio de equilibrio sube.")

H(SE, "media", "¿Qué es la inflación?",
  "El aumento sostenido y generalizado de los precios de una economía",
  [("La disminución del desempleo", "es otro indicador"),
   ("El aumento del precio de un solo producto", "debe ser generalizado, no de un bien aislado"),
   ("El crecimiento de la producción del país", "es el crecimiento económico, medido por el PIB")],
  "Con inflación, el dinero pierde poder adquisitivo: con la misma cantidad se compran menos bienes.")

H(SE, "alta", "Para controlar una inflación alta, el Banco Central de Chile suele subir la tasa de política monetaria. ¿Por qué esta medida ayuda a bajar la inflación?",
  "Porque encarece el crédito, reduce el gasto y con ello la presión sobre los precios",
  [("Porque obliga a las empresas a bajar sus precios por ley", "el Banco Central no fija precios"),
   ("Porque aumenta la cantidad de dinero en circulación", "subir la tasa tiende a reducirla"),
   ("Porque baja los impuestos", "los impuestos no los fija el Banco Central")],
  "Con tasas más altas, endeudarse cuesta más y conviene ahorrar; el menor gasto modera el alza de precios.")

H(SE, "media", "¿Qué mide el producto interno bruto (PIB) de un país?",
  "El valor de los bienes y servicios finales producidos en el país en un periodo",
  [("La cantidad de dinero que tienen los bancos", "no mide el dinero bancario"),
   ("El total de impuestos que recauda el Estado", "es solo una parte de la actividad económica"),
   ("La deuda externa del país", "es otro indicador")],
  "El PIB es el principal indicador de la actividad económica; su variación mide el crecimiento.")

H(SE, "media", "Un consumidor compra un producto que resulta defectuoso dentro de los tres meses siguientes. ¿Qué derecho le reconoce la ley chilena de protección al consumidor?",
  "Elegir entre la reparación, el cambio del producto o la devolución del dinero",
  [("Ninguno, porque ya pagó", "la ley establece la garantía legal"),
   ("Solo recibir un cupón de descuento", "el consumidor elige entre reparación, cambio o devolución"),
   ("Pedir que el producto le salga gratis para siempre", "no existe tal derecho")],
  "Es la llamada «garantía legal» o «triple opción», que fiscaliza el Sernac.")

H(SE, "alta", "Una familia gasta cada mes más de lo que gana y cubre la diferencia con tarjetas de crédito. ¿Cuál es el principal riesgo de esta situación?",
  "El sobreendeudamiento, porque los intereses aumentan la deuda con el tiempo",
  [("Que aumenten sus ingresos", "no es un riesgo"),
   ("Que el Banco Central le baje la tasa de interés", "no depende de la familia ni es un riesgo"),
   ("Que su gasto deje de influir en los precios", "no es el problema principal")],
  "Pagar solo el mínimo de una tarjeta genera intereses sobre el saldo; la deuda puede crecer más rápido que la capacidad de pago.")

H(SE, "media", "¿Qué es el desempleo en términos económicos?",
  "La situación de personas que buscan trabajo activamente y no lo encuentran",
  [("La situación de todas las personas que no trabajan, incluidos los estudiantes", "los que no buscan trabajo no se consideran desempleados"),
   ("La jubilación de los adultos mayores", "los jubilados no buscan empleo"),
   ("Un aumento de los sueldos", "no se relaciona")],
  "La tasa de desempleo se calcula sobre la fuerza de trabajo: ocupados más desocupados que buscan empleo.")

H(SE, "media", "¿Qué rol cumplen los impuestos en el sistema económico?",
  "Financiar los bienes y servicios que provee el Estado, como salud, educación y seguridad",
  [("Aumentar las ganancias de las empresas privadas", "los recauda el Estado"),
   ("Reemplazar el uso del dinero", "se pagan en dinero"),
   ("Eliminar la escasez", "la escasez es un problema permanente")],
  "Con los impuestos el Estado financia el gasto público y puede redistribuir recursos.")

H(SE, "alta", "Un país exporta principalmente cobre. Si el precio internacional del cobre cae con fuerza, ¿qué efecto es más probable en la economía de ese país?",
  "Disminuyen los ingresos por exportaciones y la recaudación fiscal",
  [("Aumentan sus ingresos por exportaciones", "el precio más bajo reduce los ingresos"),
   ("Desaparece la inflación", "no hay relación directa"),
   ("Aumenta la demanda interna de cobre", "el efecto principal es externo")],
  "Una economía poco diversificada depende del precio de su principal exportación, lo que la hace vulnerable a los ciclos internacionales.")
