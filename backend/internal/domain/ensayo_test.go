package domain

import "testing"

func TestDistribuirCantidad_EquitativoConStock(t *testing.T) {
	ejes := []Eje{EjeNumeros, EjeAlgebraFunciones}
	disp := map[Eje]int{EjeNumeros: 100, EjeAlgebraFunciones: 100}
	sel, faltante := DistribuirCantidad(10, ejes, disp)
	if faltante != 0 {
		t.Fatalf("faltante esperado 0, obtuve %d", faltante)
	}
	if sel[EjeNumeros] != 5 || sel[EjeAlgebraFunciones] != 5 {
		t.Fatalf("distribución inesperada: %+v", sel)
	}
}

func TestDistribuirCantidad_RestoATresEjes(t *testing.T) {
	ejes := []Eje{EjeNumeros, EjeAlgebraFunciones, EjeGeometria}
	disp := map[Eje]int{EjeNumeros: 100, EjeAlgebraFunciones: 100, EjeGeometria: 100}
	sel, faltante := DistribuirCantidad(10, ejes, disp)
	if faltante != 0 {
		t.Fatalf("faltante esperado 0, obtuve %d", faltante)
	}
	total := sel[EjeNumeros] + sel[EjeAlgebraFunciones] + sel[EjeGeometria]
	if total != 10 {
		t.Fatalf("total esperado 10, obtuve %d (%+v)", total, sel)
	}
}

func TestDistribuirCantidad_CompletaConCapacidadExtra(t *testing.T) {
	ejes := []Eje{EjeNumeros, EjeAlgebraFunciones}
	disp := map[Eje]int{EjeNumeros: 2, EjeAlgebraFunciones: 100}
	sel, faltante := DistribuirCantidad(10, ejes, disp)
	if faltante != 0 {
		t.Fatalf("faltante esperado 0, obtuve %d", faltante)
	}
	if sel[EjeNumeros] != 2 {
		t.Fatalf("numeros debería usar todo su stock (2), obtuve %d", sel[EjeNumeros])
	}
	if sel[EjeAlgebraFunciones] != 8 {
		t.Fatalf("algebra debería absorber el remanente (8), obtuve %d", sel[EjeAlgebraFunciones])
	}
}

func TestDistribuirCantidad_StockTotalInsuficiente(t *testing.T) {
	ejes := []Eje{EjeNumeros}
	disp := map[Eje]int{EjeNumeros: 5}
	sel, faltante := DistribuirCantidad(10, ejes, disp)
	if faltante != 5 {
		t.Fatalf("faltante esperado 5, obtuve %d", faltante)
	}
	if sel[EjeNumeros] != 5 {
		t.Fatalf("selección esperada 5, obtuve %d", sel[EjeNumeros])
	}
}

func TestCalcularDesglosePorEje(t *testing.T) {
	items := []ItemResultado{
		{Eje: EjeNumeros, EsCorrecta: true, PesoSnapshot: 100},
		{Eje: EjeNumeros, EsCorrecta: false, PesoSnapshot: 50},
		{Eje: EjeAlgebraFunciones, EsCorrecta: true, PesoSnapshot: 200},
	}
	out := CalcularDesglosePorEje(items)
	if len(out) != 2 {
		t.Fatalf("esperaba 2 ejes en el desglose, obtuve %d", len(out))
	}
	if out[0].Eje != EjeNumeros || out[0].Correctas != 1 || out[0].Total != 2 || out[0].PuntosObtenidos != 100 || out[0].PuntosPosibles != 150 {
		t.Fatalf("desglose numeros inesperado: %+v", out[0])
	}
	if out[1].Eje != EjeAlgebraFunciones || out[1].Correctas != 1 || out[1].Total != 1 || out[1].PuntosObtenidos != 200 || out[1].PuntosPosibles != 200 {
		t.Fatalf("desglose algebra inesperado: %+v", out[1])
	}
}

func TestObjetivoCiencias(t *testing.T) {
	o := ObjetivoCiencias(80, EjeBiologia)
	if o[EjeBiologia] != 44 || o[EjeFisica] != 18 || o[EjeQuimica] != 18 {
		t.Fatalf("80 preguntas con electivo Biología deberían ser 44/18/18, obtuve %v", o)
	}
	o = ObjetivoCiencias(20, EjeQuimica)
	if o[EjeBiologia]+o[EjeFisica]+o[EjeQuimica] != 20 || o[EjeQuimica] <= o[EjeFisica] {
		t.Fatalf("reparto inválido para 20 preguntas: %v", o)
	}
}

func TestElegirGruposExactos(t *testing.T) {
	elegidos := ElegirGruposExactos(10, []int{6, 5, 4, 5})
	suma := 0
	for _, i := range elegidos {
		suma += []int{6, 5, 4, 5}[i]
	}
	if suma != 10 {
		t.Fatalf("esperaba suma 10, obtuve %d (%v)", suma, elegidos)
	}
	if ElegirGruposExactos(7, []int{5, 5, 4}) != nil {
		t.Fatal("7 no se puede formar con 5, 5 y 4")
	}
}

func TestLimiteMinutosProrrateado(t *testing.T) {
	if got := LimiteMinutos(NivelCL, 65); got != 150 {
		t.Fatalf("Lectora completa debería durar 150 min, obtuve %d", got)
	}
	if got := LimiteMinutos(NivelM1, 10); got != 22 {
		t.Fatalf("10 preguntas de M1 deberían durar 22 min, obtuve %d", got)
	}
}

func TestEjesValidosSegunPrueba(t *testing.T) {
	if !EjesValidos(NivelCiencias, []Eje{EjeBiologia, EjeQuimica}) {
		t.Fatal("biología y química son ejes de Ciencias")
	}
	if EjesValidos(NivelM1, []Eje{EjeBiologia}) {
		t.Fatal("biología no es un eje de M1")
	}
}
