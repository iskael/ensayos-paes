"""Historia y Ciencias Sociales, segunda tanda: formación ciudadana, sistema económico e historia."""
from contenido.historia import FC, HI, SE, H

H(FC, "media", "¿Qué institución tiene la función de dirigir la investigación de los delitos y ejercer la acción penal pública en Chile?",
  "El Ministerio Público",
  [("La Defensoría Penal Pública", "defiende a los imputados"),
   ("El Tribunal Constitucional", "controla la constitucionalidad de las leyes"),
   ("El Congreso Nacional", "legisla y fiscaliza")],
  "Desde la reforma procesal penal, los fiscales del Ministerio Público investigan y acusan; los tribunales juzgan.")

H(FC, "media", "¿Qué principio se expresa en que el Poder Ejecutivo, el Legislativo y el Judicial tengan funciones distintas y se controlen entre sí?",
  "La separación de poderes",
  [("La soberanía nacional", "se refiere a quién reside el poder, no a su división"),
   ("La descentralización", "se refiere al reparto territorial del poder"),
   ("El sufragio universal", "se refiere al derecho a voto")],
  "Dividir el poder y establecer controles mutuos evita que se concentre y se ejerza de manera arbitraria.")

H(FC, "media", "¿Cuál es la función principal de las municipalidades en Chile?",
  "Satisfacer las necesidades de la comunidad local y asegurar su participación en el progreso de la comuna",
  [("Dictar las leyes del país", "es tarea del Congreso"),
   ("Juzgar los delitos cometidos en la comuna", "es tarea de los tribunales"),
   ("Dirigir las relaciones internacionales", "corresponde al Presidente")],
  "Las municipalidades, encabezadas por el alcalde y el concejo, administran la comuna: aseo, áreas verdes, desarrollo comunitario y otros servicios.")

H(FC, "alta", "Una persona expresa en redes sociales una opinión crítica sobre el gobierno. ¿Qué derecho ejerce y cuál es su límite en una democracia?",
  "La libertad de expresión, que tiene como límite no vulnerar los derechos de otras personas",
  [("El derecho de propiedad, sin ningún límite", "no se trata de la propiedad"),
   ("El derecho a sufragio, limitado a los días de elección", "no está votando"),
   ("La libertad de expresión, que es absoluta y no tiene límites", "responde por abusos como la injuria o la calumnia")],
  "Se puede opinar sin censura previa, pero se responde de los delitos y abusos que se cometan en su ejercicio.")

H(FC, "media", "¿Qué son los tratados internacionales de derechos humanos ratificados por Chile?",
  "Compromisos que obligan al Estado a respetar y garantizar los derechos que reconocen",
  [("Recomendaciones sin ningún efecto jurídico", "una vez ratificados, obligan al Estado"),
   ("Leyes que solo rigen en otros países", "rigen también para Chile"),
   ("Normas que solo aplican en guerra", "rigen en todo tiempo")],
  "La Constitución reconoce como límite a la soberanía los derechos garantizados por los tratados vigentes ratificados por Chile.")

H(FC, "media", "¿Por qué es importante que los jueces sean independientes del gobierno?",
  "Para que resuelvan los conflictos conforme a la ley y no según intereses políticos",
  [("Para que puedan dictar leyes", "los jueces no legislan"),
   ("Para que no tengan que fundamentar sus sentencias", "deben fundamentarlas"),
   ("Para que gobiernen cuando el Presidente se ausenta", "no es su función")],
  "La independencia judicial asegura un juicio imparcial y protege los derechos de las personas frente al poder.")

H(FC, "alta", "¿Qué diferencia a una democracia representativa de una democracia directa?",
  "En la representativa, la ciudadanía elige autoridades que deciden en su nombre",
  [("En la representativa no hay elecciones", "las elecciones son su base"),
   ("En la directa, un líder decide por todos", "en la directa decide la ciudadanía"),
   ("En la representativa solo votan los propietarios", "el voto censitario no es propio de la democracia moderna")],
  "En Chile predomina la representación, complementada con mecanismos directos como los plebiscitos.")

H(FC, "media", "Un grupo de estudiantes recolecta firmas para pedir un nuevo paradero frente a su liceo. ¿Qué tipo de acción ciudadana realizan?",
  "Participación ciudadana organizada para incidir en una decisión pública",
  [("Un recurso de protección", "es una acción judicial"),
   ("Una elección popular", "no eligen autoridades"),
   ("Un acto de desobediencia civil", "su acción es legal y pacífica")],
  "Peticiones, cabildos y organizaciones comunitarias son formas legítimas de participación.")

H(SE, "media", "¿Qué es un bien sustituto?",
  "Un bien que satisface una necesidad similar y puede reemplazar a otro",
  [("Un bien que se consume junto a otro", "ese es un bien complementario"),
   ("Un bien que no tiene precio", "todo bien económico tiene precio"),
   ("Un bien que solo produce el Estado", "no se relaciona con quién lo produce")],
  "Si sube el precio de la mantequilla, aumenta la demanda de margarina: son sustitutos.")

H(SE, "media", "Si el precio de las impresoras baja mucho, ¿qué se espera que ocurra con la demanda de cartuchos de tinta?",
  "Que aumente, porque son bienes complementarios",
  [("Que disminuya, porque son sustitutos", "no se reemplazan entre sí; se usan juntos"),
   ("Que no cambie", "más impresoras implican más cartuchos"),
   ("Que desaparezca", "no hay razón para eso")],
  "Al bajar el precio de las impresoras se venden más, y quienes las compran necesitan cartuchos.")

H(SE, "alta", "¿Qué es un monopolio y qué efecto suele tener en el mercado?",
  "Un mercado con un solo oferente, que puede fijar precios más altos que en competencia",
  [("Un mercado con muchos oferentes pequeños", "eso describe la competencia perfecta"),
   ("Un mercado donde el Estado fija todos los precios", "no es la definición"),
   ("Un mercado sin compradores", "sin compradores no hay mercado")],
  "Sin competidores, el monopolista puede restringir la producción y cobrar más; por eso existen leyes de libre competencia.")

H(SE, "media", "¿Qué es el ahorro desde el punto de vista de una persona?",
  "La parte del ingreso que no se gasta en consumo",
  [("El total del ingreso mensual", "solo una parte se ahorra"),
   ("El dinero que se pide prestado", "eso es un crédito"),
   ("El pago de impuestos", "no es ahorro")],
  "El ahorro permite enfrentar imprevistos y financiar proyectos futuros.")

H(SE, "alta", "Una persona compara dos créditos de consumo por el mismo monto y plazo. ¿Qué indicador le permite comparar el costo total de ambos?",
  "La carga anual equivalente (CAE)",
  [("El valor de la primera cuota solamente", "no incluye todos los costos"),
   ("El nombre del banco", "no mide el costo"),
   ("La tasa de desempleo", "es un indicador macroeconómico")],
  "La CAE incluye intereses, comisiones y seguros, y permite comparar créditos en Chile.")

H(SE, "media", "¿Qué es el sistema de AFP, creado en Chile en 1980?",
  "Un sistema de pensiones basado en la capitalización individual de las cotizaciones de cada trabajador",
  [("Un sistema de salud público", "la salud se organiza en Fonasa e isapres"),
   ("Un seguro de desempleo administrado por las municipalidades", "no es su función"),
   ("Un sistema de reparto en que los trabajadores activos financian a los jubilados", "ese era el sistema anterior")],
  "Cada trabajador cotiza en una cuenta individual que administra una AFP; la pensión depende de lo ahorrado y su rentabilidad.")

H(SE, "media", "¿Qué es la balanza comercial de un país?",
  "La diferencia entre el valor de sus exportaciones y el de sus importaciones",
  [("La cantidad de dinero que tiene el Banco Central", "son las reservas internacionales"),
   ("El total de impuestos cobrados a las empresas", "no es la balanza comercial"),
   ("El número de empresas exportadoras", "no mide valores de comercio")],
  "Si se exporta más de lo que se importa hay superávit; en caso contrario, déficit.")

H(SE, "alta", "Un aumento del precio internacional del petróleo, que Chile importa, ¿qué efecto tiene probablemente en la economía chilena?",
  "Encarece el transporte y la producción, lo que presiona al alza los precios internos",
  [("Baja el precio de la bencina", "subiría"),
   ("Aumenta las exportaciones de petróleo chileno", "Chile importa casi todo el petróleo que usa"),
   ("No tiene ningún efecto", "el petróleo es un insumo clave")],
  "El mayor costo del combustible se traspasa a muchos bienes y servicios y puede elevar la inflación.")

H(HI, "media", "¿Qué fue el Frente Popular que gobernó Chile desde 1938?",
  "Una coalición de partidos de centro e izquierda que llevó a Pedro Aguirre Cerda a la presidencia",
  [("Un movimiento militar que derrocó al gobierno", "llegó al poder por elecciones"),
   ("Un partido conservador que gobernó en el siglo XIX", "es del siglo XX"),
   ("La alianza que ganó el plebiscito de 1988", "fue la Concertación")],
  "El Frente Popular impulsó la educación («gobernar es educar») y la industrialización mediante la Corfo.")

H(HI, "media", "¿Qué caracterizó a la Revolución Industrial iniciada en Inglaterra a fines del siglo XVIII?",
  "El uso de máquinas y nuevas fuentes de energía en la producción en fábricas",
  [("El regreso a la producción artesanal", "reemplazó la producción artesanal"),
   ("La desaparición de las ciudades", "las ciudades crecieron con la industria"),
   ("La abolición del trabajo asalariado", "el trabajo asalariado se extendió")],
  "La máquina a vapor, la industria textil y el ferrocarril transformaron la economía y la sociedad.")

H(HI, "alta", "¿Qué consecuencia social tuvo la industrialización en Europa durante el siglo XIX?",
  "El surgimiento del proletariado urbano y de los movimientos obreros",
  [("La desaparición de la burguesía", "la burguesía se fortaleció"),
   ("La disminución de la población de las ciudades", "la población urbana creció"),
   ("El fin de toda desigualdad social", "las desigualdades se hicieron muy visibles")],
  "Las malas condiciones laborales impulsaron sindicatos, el socialismo y las primeras leyes de protección del trabajo.")
