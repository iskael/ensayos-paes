import json
import random
import shutil
import subprocess
import unittest
from collections import Counter
from pathlib import Path

import generar
from nucleo import DIFICULTADES, EJES, ETIQUETAS, REGISTRO, Descartar, armar_item, validar

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
            self.assertIn(pl.eje, EJES)
        for eje in EJES:
            self.assertGreaterEqual(sum(1 for pl in REGISTRO if pl.eje == eje), 5)


class TestLote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items, cls.fallas, _ = generar.generar()

    def test_sin_fallas_y_reproducible(self):
        self.assertEqual(self.fallas, [])
        otra, _, _ = generar.generar()
        self.assertEqual(json.dumps(self.items), json.dumps(otra))

    def test_estructura_del_item(self):
        enunciados = Counter(i["enunciado"] for i in self.items)
        self.assertEqual(max(enunciados.values()), 1)
        for it in self.items:
            self.assertEqual([a["etiqueta"] for a in it["alternativas"]], ETIQUETAS)
            self.assertEqual(sum(a["es_correcta"] for a in it["alternativas"]), 1)
            self.assertEqual(len({a["texto"] for a in it["alternativas"]}), 4)
            self.assertIn(it["dificultad"], DIFICULTADES)
            self.assertEqual((it["origen"], it["estado"]), ("generado", "borrador"))
            self.assertRegex(it["explicacion"], "Errores frecuentes:|Las demás alternativas:")
            self.assertNotIn("\n", it["enunciado"])

    def test_ningun_eje_ni_plantilla_domina(self):
        por_eje = Counter(i["eje"] for i in self.items)
        self.assertGreaterEqual(min(por_eje.values()), 60)
        por_plantilla = Counter(i["plantilla"] for i in self.items)
        self.assertLessEqual(max(por_plantilla.values()), generar.OBJETIVO_POR_PLANTILLA)

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
