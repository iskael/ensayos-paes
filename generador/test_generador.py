import json
import random
import shutil
import subprocess
import unittest
from collections import Counter
from pathlib import Path

import generar
from nucleo import DIFICULTADES, EJES, EJES_POR_NIVEL, ETIQUETAS, REGISTRO, Descartar, armar_item, validar

KATEX = Path(__file__).parent.parent / "frontend" / "node_modules" / "katex"
SORTEOS = 400

SCRIPT_KATEX = """
const katex = require(process.argv[1]);
const textos = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const patron = /\\$\\$(.+?)\\$\\$|\\$(.+?)\\$/g;
let malos = [];
for (const t of textos) {
  for (const mt of t.matchAll(patron)) {
    try { katex.renderToString(mt[1] ?? mt[2], { throwOnError: true, strict: 'error' }); }
    catch (e) { malos.push(t + ' -> ' + e.message); }
  }
}
console.log(JSON.stringify(malos));
"""


class TestPlantillas(unittest.TestCase):
    def test_cada_plantilla_solo_produce_items_validos(self):
        for pl in REGISTRO:
            rng = random.Random(pl.nombre)
            aprobados = 0
            for _ in range(SORTEOS):
                try:
                    propuesta = pl.funcion(rng)
                except Descartar:
                    continue
                fallas = validar(propuesta)
                if any("valores repetidos" in f for f in fallas):
                    continue
                self.assertEqual(fallas, [], f"{pl.nombre}: {propuesta.enunciado}")
                aprobados += 1
            self.assertGreater(aprobados, SORTEOS // 20, f"{pl.nombre} descarta casi todo")

    def test_metadatos_de_plantillas(self):
        nombres = [pl.nombre for pl in REGISTRO]
        self.assertEqual(len(nombres), len(set(nombres)))
        for pl in REGISTRO:
            self.assertIn(pl.eje, EJES_POR_NIVEL[pl.nivel])
        for eje in EJES:
            self.assertGreaterEqual(sum(1 for pl in REGISTRO if pl.eje == eje), 5)

    def test_items_fijos(self):
        from nucleo import FIJOS, propuesta_fija
        claves = Counter((f.enunciado, f.estimulo.clave if f.estimulo else None) for f in FIJOS)
        self.assertEqual([k for k, n in claves.items() if n > 1], [])
        for f in FIJOS:
            self.assertEqual(validar(propuesta_fija(f)), [], f.enunciado)
        por_estimulo = {}
        for f in FIJOS:
            if f.estimulo:
                por_estimulo.setdefault(f.estimulo.clave, []).append(f.orden)
        for clave, ordenes in por_estimulo.items():
            self.assertEqual(sorted(ordenes), list(range(1, len(ordenes) + 1)), clave)


class TestLote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items, cls.fallas, _ = generar.generar()

    def test_sin_fallas_y_reproducible(self):
        self.assertEqual(self.fallas, [])
        otra, _, _ = generar.generar()
        self.assertEqual(json.dumps(self.items), json.dumps(otra))

    def test_estructura_del_item(self):
        claves = Counter((i["enunciado"], i["imagen_url"], (i["estimulo"] or {}).get("clave")) for i in self.items)
        self.assertEqual(max(claves.values()), 1)
        for it in self.items:
            n = len(it["alternativas"])
            self.assertIn(n, (4, 5))
            self.assertEqual([a["etiqueta"] for a in it["alternativas"]], ETIQUETAS[:n])
            self.assertEqual(sum(a["es_correcta"] for a in it["alternativas"]), 1)
            self.assertEqual(len({a["texto"] for a in it["alternativas"]}), n)
            self.assertIn(it["dificultad"], DIFICULTADES)
            self.assertEqual((it["origen"], it["estado"]), ("generado", "borrador"))
            self.assertRegex(it["explicacion"], "Errores frecuentes:|Las demás alternativas:")
            self.assertNotIn("\n", it["enunciado"])
            for texto in [it["enunciado"], it["explicacion"]]:
                fuera_de_formulas = "".join(texto.split("$")[0::2])
                self.assertNotIn("{", fuera_de_formulas, texto)

    def test_figuras(self):
        con_figura = [it for it in self.items if it["imagen_url"]]
        self.assertGreater(len(con_figura), 100)
        for it in self.items:
            self.assertEqual(bool(it["imagen_url"]), bool(it["figura_svg"]))
            if it["imagen_url"]:
                self.assertRegex(it["imagen_url"], r"^/uploads/gen-[0-9a-f]{16}\.png$")
                self.assertTrue(it["figura_svg"].startswith("<svg "))

    def test_ningun_eje_ni_plantilla_domina(self):
        por_eje = Counter(i["eje"] for i in self.items)
        self.assertGreaterEqual(min(por_eje[e] for e in EJES), 60)
        self.assertGreaterEqual(min(n for e, n in por_eje.items() if e not in EJES), 10)
        por_plantilla = Counter(i["plantilla"] for i in self.items)
        self.assertLessEqual(max(n for p, n in por_plantilla.items() if not p.startswith("fijo_")), generar.OBJETIVO_POR_PLANTILLA)

    def test_sql_tiene_un_insert_por_item(self):
        sql = generar.a_sql(self.items)
        self.assertEqual(sql.count("INSERT INTO items"), len(self.items))
        self.assertTrue(sql.startswith("BEGIN;") and sql.rstrip().endswith("COMMIT;"))

    @unittest.skipUnless(shutil.which("node") and KATEX.exists(), "requiere node y frontend/node_modules/katex")
    def test_todas_las_formulas_renderizan_en_katex(self):
        textos = []
        for it in self.items:
            textos += [it["enunciado"], it["explicacion"]] + [a["texto"] for a in it["alternativas"]]
        salida = subprocess.run(["node", "-e", SCRIPT_KATEX, str(KATEX)], input=json.dumps(textos),
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(salida.stdout), [])


if __name__ == "__main__":
    unittest.main()
