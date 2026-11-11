const TRAZOS = {
  inicio: 'M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z',
  progreso: 'M4 20V10M10 20V4M16 20v-7M22 20H2',
  grupos: 'M16 19v-1a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v1M9 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM22 19v-1a4 4 0 0 0-3-3.87M16 4.13a3 3 0 0 1 0 5.75',
  cuenta: 'M20 21v-1a5 5 0 0 0-5-5H9a5 5 0 0 0-5 5v1M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
  banco: 'M4 6h16M4 12h16M4 18h10',
  examenes: 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6',
  cerrar: 'M6 6l12 12M18 6 6 18',
  atras: 'M15 18l-6-6 6-6',
  adelante: 'M9 18l6-6-6-6',
  grilla: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z',
  bandera: 'M5 21V4M5 4h11l-2 4 2 4H5',
  tachar: 'M5 12h14M8 7l8 10',
  reloj: 'M12 7v5l3 2M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z',
  texto: 'M5 5h14M5 10h14M5 15h9M5 20h6',
  ok: 'M5 12.5 10 17l9-10',
  mal: 'M7 7l10 10M17 7 7 17',
  luna: 'M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z',
  letra: 'M4 20 9.5 5h1L16 20M6.5 14h7M17 20l2.5-7h.5l2.5 7',
}

export default function Icono({ nombre, tam = 22, relleno = false, titulo }) {
  return (
    <svg
      width={tam}
      height={tam}
      viewBox="0 0 24 24"
      fill={relleno ? 'currentColor' : 'none'}
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden={titulo ? undefined : true}
      role={titulo ? 'img' : undefined}
    >
      {titulo && <title>{titulo}</title>}
      <path d={TRAZOS[nombre] ?? ''} />
    </svg>
  )
}
