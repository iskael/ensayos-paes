export const NIVELES = ['M1', 'M2']

export const CANTIDADES = [10, 20, 30]

export const EJES = [
  { valor: 'numeros', etiqueta: 'Números' },
  { valor: 'algebra_funciones', etiqueta: 'Álgebra y funciones' },
  { valor: 'geometria', etiqueta: 'Geometría' },
  { valor: 'probabilidad_estadistica', etiqueta: 'Probabilidad y estadística' },
]

export const MENU_POR_ROL = {
  estudiante: [
    { etiqueta: 'Configurar ensayo', ruta: '/', disponible: true },
    { etiqueta: 'Mi progreso', ruta: '/dashboard', disponible: true },
  ],
  profesor: [{ etiqueta: 'Mis grupos', ruta: null, disponible: false }],
  admin: [{ etiqueta: 'Banco de preguntas', ruta: null, disponible: false }],
}

export const ETIQUETA_ROL = {
  estudiante: 'Estudiante',
  profesor: 'Profesor',
  admin: 'Admin',
}
