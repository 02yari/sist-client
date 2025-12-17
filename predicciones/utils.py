# utils.py para predicciones

def explicar_riesgo(nivel_riesgo):
    """
    Devuelve una explicación simple del nivel de riesgo.
    """
    explicaciones = {
        'bajo': 'El cliente tiene bajo riesgo de abandono.',
        'medio': 'El cliente tiene un riesgo moderado de abandono.',
        'alto': 'El cliente tiene alto riesgo de abandono.',
    }
    return explicaciones.get(nivel_riesgo, 'Nivel de riesgo desconocido.')
