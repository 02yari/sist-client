from ml.predict import predict_churn

def chatbot_response(message):
    message = message.lower()

    # intención simple
    if "riesgo" in message or "churn" in message:
        # datos de ejemplo (luego serán dinámicos)
        data = [30, 12, 3, 1, 0]
        resultado, prob = predict_churn(data)

        if resultado == 1:
            return f"El cliente parece ACTIVO. Riesgo bajo ({prob:.2f})"
        else:
            return f"El cliente está en RIESGO DE CHURN ({prob:.2f})"

    return "Puedo ayudarte a predecir riesgo de churn. Pregunta algo relacionado."
