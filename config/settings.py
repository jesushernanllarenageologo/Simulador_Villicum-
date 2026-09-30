# Configuración general y parámetros por defecto

ESCENARIOS = {
    "Sequía": {
        "aporte_inicial": 50,
        "aporte_glaciar": 30
    },
    "Normal": {
        "aporte_inicial": 100,
        "aporte_glaciar": 50
    },
    "Húmedo": {
        "aporte_inicial": 150,
        "aporte_glaciar": 80
    }
}

DEFAULT_MINA_DEMANDA = 10
DEFAULT_MINA_RECIRCULACION = 50

DEFAULT_AGRICULTURA_DEMANDA = 60
DEFAULT_AGRICULTURA_EFICIENCIA = 40

DEFAULT_URBANO_DEMANDA = 20
DEFAULT_INDUSTRIAL_DEMANDA = 10

ESTADOS_SIMULACION = {
    0: "Preparación",
    1: "Alta cordillera",
    2: "Mina",
    3: "Mina → Cuenca media",
    4: "Embalses",
    5: "Embalses → Ullum → Valle",
    6: "Distribución del agua",
    7: "Resultado final"
}
