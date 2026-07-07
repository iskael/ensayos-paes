export const NIVELES = ['M1', 'M2']

export const CANTIDADES = [10, 20, 30]

export const EJES = [
  { valor: 'numeros', etiqueta: 'Números' },
  { valor: 'algebra_funciones', etiqueta: 'Álgebra y funciones' },
  { valor: 'geometria', etiqueta: 'Geometría' },
  { valor: 'probabilidad_estadistica', etiqueta: 'Probabilidad y estadística' },
]

export function etiquetaEje(valor) {
  return EJES.find((e) => e.valor === valor)?.etiqueta ?? valor
}

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
    { etiqueta: 'Configurar ensayo', ruta: '/', disponible: true },
    { etiqueta: 'Mi progreso', ruta: '/dashboard', disponible: true },
  ],
  profesor: [{ etiqueta: 'Mis grupos', ruta: null, disponible: false }],
  admin: [{ etiqueta: 'Banco de preguntas', ruta: '/banco/items', disponible: true }],
}

export const ETIQUETA_ROL = {
  estudiante: 'Estudiante',
  profesor: 'Profesor',
  admin: 'Admin',
}
