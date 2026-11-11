export const PRUEBAS = [
  { nivel: 'CL', nombre: 'Competencia Lectora', sigla: 'CL', color: '#0ea5e9' },
  { nivel: 'M1', nombre: 'Matemática 1', sigla: 'M1', color: '#4f46e5' },
  { nivel: 'M2', nombre: 'Matemática 2', sigla: 'M2', color: '#7c3aed' },
  { nivel: 'CIENCIAS', nombre: 'Ciencias', sigla: 'CS', color: '#059669' },
  { nivel: 'HCS', nombre: 'Historia y Cs. Sociales', sigla: 'HI', color: '#d97706' },
]

export const NIVELES = PRUEBAS.map((p) => p.nivel)

export function datosPrueba(nivel) {
  return PRUEBAS.find((p) => p.nivel === nivel) ?? { nivel, nombre: nivel, sigla: nivel, color: '#6b7280' }
}

export const CANTIDADES = [5, 10, 15, 20, 30, 40, 55, 65, 80]

export const EJES = [
  { valor: 'numeros', etiqueta: 'Números', niveles: ['M1', 'M2'] },
  { valor: 'algebra_funciones', etiqueta: 'Álgebra y funciones', niveles: ['M1', 'M2'] },
  { valor: 'geometria', etiqueta: 'Geometría', niveles: ['M1', 'M2'] },
  { valor: 'probabilidad_estadistica', etiqueta: 'Probabilidad y estadística', niveles: ['M1', 'M2'] },
  { valor: 'localizar', etiqueta: 'Localizar', niveles: ['CL'] },
  { valor: 'interpretar', etiqueta: 'Interpretar', niveles: ['CL'] },
  { valor: 'evaluar', etiqueta: 'Evaluar', niveles: ['CL'] },
  { valor: 'biologia', etiqueta: 'Biología', niveles: ['CIENCIAS'] },
  { valor: 'fisica', etiqueta: 'Física', niveles: ['CIENCIAS'] },
  { valor: 'quimica', etiqueta: 'Química', niveles: ['CIENCIAS'] },
  { valor: 'historia', etiqueta: 'Historia', niveles: ['HCS'] },
  { valor: 'formacion_ciudadana', etiqueta: 'Formación ciudadana', niveles: ['HCS'] },
  { valor: 'sistema_economico', etiqueta: 'Sistema económico', niveles: ['HCS'] },
]

export function ejesDe(nivel) {
  return EJES.filter((e) => e.niveles.includes(nivel))
}

export function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

export const MODOS = [
  { valor: 'practica', etiqueta: 'Práctica', ayuda: 'Revisás cada pregunta al responderla, con su explicación.' },
  { valor: 'simulacro', etiqueta: 'Simulacro', ayuda: 'Con el tiempo oficial prorrateado y la corrección al final.' },
  { valor: 'libre', etiqueta: 'Libre', ayuda: 'Sin tiempo y con la corrección al final.' },
]

export const DIFICULTADES = [
  { valor: 'baja', etiqueta: 'Baja' },
  { valor: 'media', etiqueta: 'Media' },
  { valor: 'alta', etiqueta: 'Alta' },
]

export const TIPOS_EXAMEN = [
  { valor: 'PAES_Regular', etiqueta: 'PAES Regular' },
  { valor: 'PAES_Invierno', etiqueta: 'PAES Invierno' },
  { valor: 'PDT', etiqueta: 'PDT' },
]

export const ESTADOS_ITEM = [
  { valor: 'borrador', etiqueta: 'Borrador' },
  { valor: 'publicado', etiqueta: 'Publicado' },
  { valor: 'oculto', etiqueta: 'Oculto' },
]

export const MENU_POR_ROL = {
  estudiante: [
    { etiqueta: 'Practicar', ruta: '/', icono: 'inicio', disponible: true },
    { etiqueta: 'Progreso', ruta: '/dashboard', icono: 'progreso', disponible: true },
    { etiqueta: 'Meta', ruta: '/meta', icono: 'meta', disponible: true },
    { etiqueta: 'Grupos', ruta: '/mis-grupos', icono: 'grupos', disponible: true },
  ],
  profesor: [{ etiqueta: 'Grupos', ruta: '/grupos', icono: 'grupos', disponible: true }],
  admin: [
    { etiqueta: 'Preguntas', ruta: '/banco/items', icono: 'banco', disponible: true },
    { etiqueta: 'Textos', ruta: '/banco/textos', icono: 'texto', disponible: true },
    { etiqueta: 'Exámenes', ruta: '/banco/examenes', icono: 'examenes', disponible: true },
    { etiqueta: 'Usuarios', ruta: '/admin/usuarios', icono: 'grupos', disponible: true },
  ],
  editor: [
    { etiqueta: 'Preguntas', ruta: '/banco/items', icono: 'banco', disponible: true },
    { etiqueta: 'Textos', ruta: '/banco/textos', icono: 'texto', disponible: true },
    { etiqueta: 'Exámenes', ruta: '/banco/examenes', icono: 'examenes', disponible: true },
  ],
  apoderado: [{ etiqueta: 'Estudiantes', ruta: '/pupilos', icono: 'progreso', disponible: true }],
  institucion: [{ etiqueta: 'Institución', ruta: '/institucion', icono: 'grupos', disponible: true }],
}

export const ETIQUETA_ROL = {
  estudiante: 'Estudiante',
  profesor: 'Profesor',
  admin: 'Admin',
  editor: 'Editor',
  apoderado: 'Apoderado',
  institucion: 'Institución',
}

export const ROLES_ASIGNABLES = ['estudiante', 'profesor', 'apoderado', 'institucion', 'editor']
