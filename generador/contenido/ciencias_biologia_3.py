"""Biología, tercera tanda: sistemas del cuerpo humano, inmunidad, genética molecular, evolución, ecología y análisis de datos."""
from contenido.ciencias_biologia import B

# ---------------- Sistemas del cuerpo humano

B("baja", "¿Cuál es la unidad estructural y funcional del sistema nervioso?",
  "La neurona",
  [("El nefrón", "es la unidad funcional del riñón"),
   ("El alvéolo", "es la estructura del pulmón donde ocurre el intercambio de gases"),
   ("La fibra muscular", "es la célula del tejido muscular")],
  "La neurona recibe, integra y transmite impulsos nerviosos; es la unidad básica del sistema nervioso.")

B("media", "¿Qué ocurre en la sinapsis química entre dos neuronas?",
  "La neurona presináptica libera neurotransmisores que se unen a receptores de la neurona postsináptica",
  [("El impulso pasa directamente por el citoplasma de una neurona a otra", "en la sinapsis química las membranas no se fusionan; hay un espacio sináptico"),
   ("La neurona postsináptica libera hormonas a la sangre", "eso describe una secreción endocrina"),
   ("Las neuronas intercambian su ADN", "no hay intercambio de material genético")],
  "El impulso que llega al terminal del axón provoca la liberación de neurotransmisores al espacio sináptico; estos se unen a receptores de la otra célula.")

B("media", "Al tocar accidentalmente una superficie muy caliente, la mano se retira antes de sentir dolor. ¿Qué estructura integra esta respuesta refleja?",
  "La médula espinal",
  [("El cerebelo", "coordina el equilibrio y los movimientos finos"),
   ("La corteza cerebral", "la percepción consciente del dolor llega después del reflejo"),
   ("El hipotálamo", "regula la temperatura y otras funciones internas")],
  "En el arco reflejo, la información sensorial llega a la médula espinal, que activa directamente a las neuronas motoras sin esperar al encéfalo.")

B("media", "¿Dónde se absorbe la mayor parte de los nutrientes de los alimentos?",
  "En el intestino delgado",
  [("En el estómago", "allí se digieren las proteínas, pero la absorción de nutrientes es escasa"),
   ("En el intestino grueso", "absorbe principalmente agua y sales"),
   ("En el esófago", "solo transporta el bolo alimenticio")],
  "Las vellosidades y microvellosidades del intestino delgado aumentan la superficie de absorción.")

B("media", "¿Qué función cumple la bilis en la digestión?",
  "Emulsionar las grasas para facilitar la acción de las lipasas",
  [("Digerir las proteínas hasta aminoácidos", "lo hacen las proteasas, como la pepsina y la tripsina"),
   ("Degradar el almidón en glucosa", "lo hace la amilasa"),
   ("Absorber el agua de los desechos", "ocurre en el intestino grueso")],
  "La bilis, producida por el hígado y almacenada en la vesícula, no es una enzima: divide las grasas en gotas pequeñas.")

B("media", "¿Qué tipo de vaso sanguíneo transporta la sangre desde el corazón hacia los órganos?",
  "Las arterias",
  [("Las venas", "llevan la sangre de regreso al corazón"),
   ("Los vasos linfáticos", "transportan linfa, no sangre"),
   ("Los capilares", "conectan arterias y venas, donde ocurre el intercambio con los tejidos")],
  "Las arterias salen del corazón y tienen paredes gruesas y elásticas que resisten la presión.")

B("alta", "¿Por qué la arteria pulmonar transporta sangre pobre en oxígeno, a diferencia de la mayoría de las arterias?",
  "Porque lleva la sangre desde el ventrículo derecho hacia los pulmones para oxigenarla",
  [("Porque transporta la sangre desde los pulmones hacia la aurícula izquierda", "esa es la función de las venas pulmonares"),
   ("Porque sale del ventrículo izquierdo hacia todo el cuerpo", "es la aorta, que lleva sangre oxigenada"),
   ("Porque las arterias siempre llevan sangre pobre en oxígeno", "la mayoría de las arterias llevan sangre oxigenada")],
  "Arteria y vena se definen por la dirección respecto del corazón, no por el contenido de oxígeno: la arteria pulmonar sale del corazón hacia los pulmones.")

B("media", "¿En qué estructura del sistema respiratorio ocurre el intercambio de oxígeno y dióxido de carbono con la sangre?",
  "En los alvéolos pulmonares",
  [("En la tráquea", "conduce el aire, pero no intercambia gases"),
   ("En los bronquios", "conducen el aire hacia los bronquiolos"),
   ("En la laringe", "contiene las cuerdas vocales")],
  "Los alvéolos tienen paredes muy delgadas rodeadas de capilares, lo que permite la difusión de los gases.")

B("media", "¿Qué molécula de los glóbulos rojos transporta la mayor parte del oxígeno en la sangre?",
  "La hemoglobina",
  [("La insulina", "es una hormona que regula la glucosa"),
   ("La queratina", "es una proteína estructural del pelo y las uñas"),
   ("El fibrinógeno", "participa en la coagulación")],
  "La hemoglobina contiene hierro, que se une de forma reversible al oxígeno.")

B("media", "¿Cuál es la unidad funcional del riñón, donde se filtra la sangre y se forma la orina?",
  "El nefrón",
  [("La neurona", "es la unidad del sistema nervioso"),
   ("El uréter", "conduce la orina desde el riñón hasta la vejiga"),
   ("La vejiga", "almacena la orina")],
  "Cada riñón tiene alrededor de un millón de nefrones, que filtran la sangre y reabsorben agua y sustancias útiles.")

B("alta", "Una persona está deshidratada. ¿Qué cambio hormonal se espera para conservar agua?",
  "Aumenta la secreción de hormona antidiurética (ADH) y se produce orina más concentrada",
  [("Disminuye la ADH y se produce más orina", "eso aumentaría la pérdida de agua"),
   ("Aumenta la insulina y baja la glucosa en la sangre", "la insulina no regula el balance de agua"),
   ("Aumenta la adrenalina y se detiene la filtración renal", "la filtración no se detiene")],
  "La ADH aumenta la reabsorción de agua en los túbulos del nefrón; así se pierde menos agua por la orina.")

B("media", "¿Qué glándula produce la tiroxina, hormona que regula el metabolismo?",
  "La tiroides",
  [("El páncreas", "produce insulina y glucagón"),
   ("Las glándulas suprarrenales", "producen adrenalina y cortisol"),
   ("La hipófisis", "produce, entre otras, la hormona que estimula a la tiroides")],
  "La tiroxina aumenta la tasa metabólica; su producción la regula la hormona TSH de la hipófisis.")

B("alta", "El glucagón es una hormona que se secreta cuando la glucosa en la sangre baja. ¿Cuál es su efecto?",
  "Estimula al hígado a degradar glucógeno y liberar glucosa a la sangre",
  [("Estimula a las células a captar glucosa de la sangre", "ese es el efecto de la insulina"),
   ("Aumenta la eliminación de glucosa por la orina", "no es su mecanismo"),
   ("Transforma la glucosa en grasa en el tejido adiposo", "eso reduciría aún más la glucosa disponible")],
  "Insulina y glucagón son antagonistas: la insulina baja la glucosa y el glucagón la sube.")

# ---------------- Inmunidad

B("media", "¿Cómo protege una vacuna contra una enfermedad infecciosa?",
  "Estimula al sistema inmune a producir anticuerpos y células de memoria sin causar la enfermedad",
  [("Mata directamente a los microorganismos que ya están en el cuerpo", "eso lo hacen, en el caso de las bacterias, los antibióticos"),
   ("Entrega anticuerpos ya formados que duran toda la vida", "eso describe la inmunidad pasiva, que es transitoria"),
   ("Reemplaza a los glóbulos blancos del organismo", "la vacuna no reemplaza células")],
  "La vacuna presenta antígenos inofensivos; el organismo genera una respuesta y memoria inmunológica, que actúa rápido ante una infección real.")

B("media", "¿Qué son los anticuerpos?",
  "Proteínas producidas por los linfocitos B que reconocen y se unen a antígenos específicos",
  [("Microorganismos que atacan a las bacterias", "no son microorganismos"),
   ("Medicamentos que se usan contra los virus", "son moléculas del propio organismo"),
   ("Glóbulos rojos especializados en defensa", "los glóbulos rojos transportan oxígeno")],
  "Los anticuerpos o inmunoglobulinas neutralizan antígenos y marcan a los patógenos para su destrucción.")

B("alta", "Un recién nacido que toma leche materna recibe anticuerpos de su madre. ¿Qué tipo de inmunidad adquiere?",
  "Inmunidad pasiva natural",
  [("Inmunidad activa natural", "sería activa si el propio bebé produjera los anticuerpos al infectarse"),
   ("Inmunidad activa artificial", "corresponde a la vacunación"),
   ("Inmunidad pasiva artificial", "corresponde, por ejemplo, a la aplicación de un suero")],
  "Es pasiva porque los anticuerpos vienen ya formados y natural porque no hay intervención médica; su efecto es temporal.")

B("media", "¿Por qué los antibióticos no sirven para tratar un resfrío común?",
  "Porque el resfrío es causado por virus y los antibióticos actúan contra bacterias",
  [("Porque el resfrío es causado por hongos", "lo causan virus"),
   ("Porque los antibióticos solo actúan en el estómago", "actúan en todo el cuerpo"),
   ("Porque el sistema inmune impide que los antibióticos funcionen", "no es así")],
  "Los antibióticos atacan estructuras bacterianas, como la pared celular, que los virus no poseen. Su mal uso favorece la resistencia.")

# ---------------- Genética molecular y herencia

B("media", "En la molécula de ADN, ¿con qué base nitrogenada se aparea la adenina?",
  "Con la timina",
  [("Con la guanina", "la guanina se aparea con la citosina"),
   ("Con el uracilo", "el uracilo reemplaza a la timina en el ARN"),
   ("Con la citosina", "la citosina se aparea con la guanina")],
  "En el ADN, A se aparea con T mediante dos puentes de hidrógeno, y G con C mediante tres.")

B("alta", "Si en una molécula de ADN de doble hebra el 30 % de las bases son adenina, ¿qué porcentaje corresponde a guanina?",
  "20 %",
  [("30 %", "es el porcentaje de timina, que iguala al de adenina"),
   ("40 %", "es el porcentaje de guanina y citosina juntas"),
   ("70 %", "es el porcentaje que no es adenina")],
  "A = T = 30 %, así que A + T = 60 %. Queda 40 % para G + C, y como G = C, la guanina es 20 %.")

B("media", "¿Qué proceso produce una molécula de ARN mensajero a partir de un gen del ADN?",
  "La transcripción",
  [("La traducción", "es la síntesis de proteínas a partir del ARN mensajero"),
   ("La replicación", "es la copia del ADN completo antes de la división celular"),
   ("La mutación", "es un cambio en la secuencia del ADN")],
  "El flujo de información es ADN → (transcripción) → ARN → (traducción) → proteína.")

B("alta", "Un codón del ARN mensajero está formado por:",
  "tres nucleótidos que codifican un aminoácido o una señal de término",
  [("un solo nucleótido que codifica una proteína completa", "una proteína está codificada por muchos codones"),
   ("dos aminoácidos unidos por un enlace peptídico", "los codones son secuencias de nucleótidos, no de aminoácidos"),
   ("un gen completo", "un gen contiene muchos codones")],
  "El código genético se lee en tripletes: cada codón corresponde a un aminoácido, salvo los codones de término.")

B("media", "¿Qué es un cariotipo?",
  "El conjunto de cromosomas de una célula, ordenados por tamaño y forma",
  [("La secuencia completa de nucleótidos de un gen", "eso es la secuencia de un gen"),
   ("El fenotipo de un individuo", "el fenotipo son sus características observables"),
   ("Una mutación que afecta a un solo gen", "no es una mutación")],
  "El cariotipo permite detectar alteraciones en el número o la estructura de los cromosomas, como la trisomía 21.")

B("alta", "El síndrome de Down se asocia a la presencia de tres cromosomas 21. ¿Qué proceso suele originarlo?",
  "Una no disyunción de los cromosomas durante la meiosis",
  [("Una mutación puntual en un solo gen", "no afecta el número de cromosomas"),
   ("Una infección viral durante el embarazo", "no es la causa"),
   ("La herencia de un alelo recesivo de ambos padres", "no se hereda como un rasgo mendeliano recesivo")],
  "Si los cromosomas homólogos o las cromátidas no se separan en la meiosis, un gameto puede llevar dos copias del cromosoma 21.")

B("alta", "Una mujer de grupo sanguíneo AB tiene un hijo con un hombre de grupo O. ¿Qué grupos sanguíneos pueden tener sus hijos?",
  "A o B",
  [("AB u O", "el padre solo aporta O y la madre aporta A o B, nunca ambos"),
   ("Solo O", "la madre no tiene alelo O"),
   ("A, B, AB u O", "con estos padres no son posibles AB ni O")],
  "La madre aporta A o B y el padre aporta O: los hijos son AO (grupo A) o BO (grupo B).")

B("media", "¿Qué significa que dos alelos sean codominantes, como los alelos A y B del grupo sanguíneo?",
  "Que en el heterocigoto ambos se expresan completamente",
  [("Que uno oculta completamente al otro", "eso es dominancia completa"),
   ("Que el heterocigoto presenta un fenotipo intermedio", "eso es dominancia incompleta"),
   ("Que ninguno de los dos se expresa", "ambos se expresan")],
  "Una persona AB tiene en sus glóbulos rojos los antígenos A y B a la vez.")

# ---------------- Evolución

B("alta", "Una población de aves queda separada en dos islas durante miles de años y, con el tiempo, ya no pueden reproducirse entre sí. ¿Qué proceso ocurrió?",
  "Especiación por aislamiento geográfico",
  [("Selección artificial", "requiere que los seres humanos elijan a los reproductores"),
   ("Generación espontánea", "es una idea refutada"),
   ("Herencia de caracteres adquiridos", "es la idea de Lamarck")],
  "El aislamiento impide el flujo genético; cada población acumula cambios distintos hasta que surge aislamiento reproductivo.")

B("media", "¿Qué son las estructuras homólogas, como el brazo humano y el ala de un murciélago?",
  "Estructuras con un mismo origen evolutivo, aunque cumplan funciones distintas",
  [("Estructuras con la misma función pero distinto origen", "eso describe a las estructuras análogas"),
   ("Estructuras sin función en el organismo actual", "eso describe a los órganos vestigiales"),
   ("Estructuras idénticas en todas las especies", "no son idénticas")],
  "Las estructuras homólogas comparten un plan óseo semejante heredado de un antepasado común.")

B("media", "¿Qué es la selección artificial?",
  "La elección, por parte del ser humano, de los individuos que se reproducen según características deseadas",
  [("La supervivencia de los individuos mejor adaptados al ambiente natural", "eso es la selección natural"),
   ("La aparición de nuevas especies por mutaciones al azar", "no involucra la acción humana"),
   ("La transmisión de caracteres adquiridos durante la vida", "es la idea de Lamarck")],
  "Las razas de perros y muchas variedades de cultivo son resultado de la selección artificial.")

# ---------------- Ecología

B("media", "¿Qué proceso realizan algunas bacterias del suelo y de las raíces de leguminosas en el ciclo del nitrógeno?",
  "Fijan el nitrógeno atmosférico y lo transforman en compuestos que las plantas pueden usar",
  [("Liberan oxígeno mediante la fotosíntesis", "no corresponde al ciclo del nitrógeno"),
   ("Transforman el nitrógeno en dióxido de carbono", "son elementos distintos"),
   ("Eliminan todo el nitrógeno del suelo", "lo incorporan al suelo")],
  "Las plantas no pueden usar el N₂ del aire; las bacterias fijadoras lo convierten en amonio y otros compuestos.")

B("media", "Tras un incendio que arrasa un bosque, primero aparecen pastos y luego arbustos y árboles. ¿Cómo se llama este proceso?",
  "Sucesión ecológica secundaria",
  [("Sucesión ecológica primaria", "ocurre donde no hay suelo previo, como sobre lava"),
   ("Eutrofización", "es el exceso de nutrientes en un cuerpo de agua"),
   ("Selección artificial", "no interviene el ser humano")],
  "La sucesión secundaria ocurre donde el suelo se conserva tras una perturbación, por lo que avanza más rápido que la primaria.")

B("alta", "El castor fue introducido en Tierra del Fuego y, sin depredadores naturales, sus represas han destruido grandes áreas de bosque nativo. ¿Qué concepto describe a esta especie en ese ecosistema?",
  "Especie exótica invasora",
  [("Especie endémica", "una especie endémica es nativa y exclusiva de un lugar"),
   ("Especie en peligro de extinción", "su población ha crecido"),
   ("Productor primario", "el castor es un herbívoro")],
  "Una especie exótica invasora es introducida fuera de su área natural y causa daños al ecosistema que la recibe.")

B("media", "¿Qué factor es abiótico en un ecosistema?",
  "La temperatura del agua",
  [("Los peces del río", "son seres vivos, factores bióticos"),
   ("Las algas", "son organismos productores"),
   ("Las bacterias descomponedoras", "son seres vivos")],
  "Los factores abióticos son componentes físicos y químicos: luz, temperatura, agua, salinidad o pH.")

B("alta", "En una pirámide de energía, los productores tienen 10.000 kcal. Si se transfiere aproximadamente el 10 % a cada nivel, ¿cuánta energía llega a los consumidores secundarios?",
  "100 kcal",
  [("1.000 kcal", "es la energía de los consumidores primarios"),
   ("10 kcal", "corresponde a los consumidores terciarios"),
   ("9.000 kcal", "es la energía que se pierde entre productores y consumidores primarios")],
  "10.000 → 1.000 (consumidores primarios) → 100 (consumidores secundarios).")

B("media", "¿Qué fenómeno ocurre cuando una sustancia tóxica que no se degrada aumenta su concentración a lo largo de la cadena trófica?",
  "La bioacumulación o biomagnificación",
  [("La fotosíntesis", "es la producción de materia orgánica con luz"),
   ("La sucesión ecológica", "es el reemplazo de comunidades en el tiempo"),
   ("La fijación de nitrógeno", "es parte del ciclo del nitrógeno")],
  "Cada consumidor ingiere muchas presas contaminadas; la sustancia se acumula y alcanza su mayor concentración en los depredadores tope.")

# ---------------- Habilidades científicas

B("alta", "Un estudiante mide el tiempo que tarda en germinar una semilla a distintas temperaturas: 10 °C, 9 días; 20 °C, 5 días; 30 °C, 3 días. ¿Qué conclusión es válida para esas semillas y ese rango?",
  "Al aumentar la temperatura entre 10 °C y 30 °C, disminuye el tiempo de germinación",
  [("A cualquier temperatura, más calor siempre acelera la germinación", "generaliza fuera del rango estudiado"),
   ("La temperatura no influye en la germinación", "los datos muestran una relación"),
   ("A 40 °C la semilla germinará en un día", "no se midió esa temperatura")],
  "Una conclusión debe limitarse a los datos obtenidos; extrapolar fuera del rango medido no está justificado.")

B("media", "En un experimento para evaluar el efecto de un fertilizante, ¿cuál es la función del grupo control?",
  "Servir de comparación, porque recibe el mismo trato excepto el fertilizante",
  [("Recibir el doble de fertilizante", "eso sería otro grupo experimental"),
   ("Confirmar la hipótesis en cualquier caso", "un control no garantiza un resultado"),
   ("Reemplazar las mediciones del grupo experimental", "ambos grupos se miden")],
  "Al comparar con el control, cualquier diferencia se puede atribuir a la variable independiente.")

B("alta", "Un investigador afirma que un nuevo medicamento reduce la presión arterial, pero solo lo probó en cinco personas y sin grupo control. ¿Cuál es la principal debilidad del estudio?",
  "La muestra es muy pequeña y no hay con qué comparar los resultados",
  [("El medicamento se probó en seres humanos", "es necesario para un medicamento humano"),
   ("La presión arterial no se puede medir", "sí se puede medir"),
   ("El estudio tiene una hipótesis", "toda investigación necesita una hipótesis")],
  "Sin control no se descarta que la presión bajara por otros motivos, y con cinco personas los resultados pueden deberse al azar.")

B("media", "¿Qué diferencia una teoría científica de una hipótesis?",
  "La teoría es una explicación amplia respaldada por muchas evidencias; la hipótesis es una explicación provisoria que se pone a prueba",
  [("La teoría es una suposición sin evidencia", "en ciencia, una teoría está ampliamente respaldada"),
   ("La hipótesis es más general que la teoría", "es al revés"),
   ("No hay diferencia, son sinónimos", "son conceptos distintos")],
  "La teoría celular o la teoría de la evolución integran gran cantidad de evidencia; una hipótesis es una predicción comprobable.")
