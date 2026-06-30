# Prototipo de generación de ítems (v2)

Genera ítems PAES por plantillas parametrizadas y los valida (estructural + simbólico con sympy).
La correctitud está garantizada por construcción; este prototipo sirve para medir calidad
antes de implementar el módulo real (ver `../docs/diseno_generacion_ia_v2.md`).

## Uso
```bash
pip install sympy
python3 genera_preguntas.py
```

## Salida
- `preguntas_generadas.json` — ítems aprobados (formato alineado al modelo del MVP).
- `reporte_calidad.txt` — métricas (tasa de aprobación, rechazos).
