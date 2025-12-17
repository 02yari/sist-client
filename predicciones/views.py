from django.shortcuts import render

# Protección de vistas con login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from clientes.models import Cliente
@login_required
def home(request):
    return render(request, 'predicciones/inicio.html')

@login_required
def entrenar_modelo(request):
    if request.user.rol != 'admin':
        return HttpResponseForbidden("No tienes permiso para entrenar el modelo")

    
    # 1. Preparar dataset
    
    clientes = Cliente.objects.all().values(
        'estado', 'nivel_riesgo', 'telefono'  # ajusta según tus features
    )
    df = pd.DataFrame(clientes)

    # Convertir variables categóricas si es necesario
    df = pd.get_dummies(df, columns=['estado', 'nivel_riesgo'], drop_first=True)

    # 2. Definir X y y (ejemplo: predecir abandono por estado)
    # Supongamos que abandono = estado_inactivo (1) / activo (0)
    if 'estado_inactivo' in df.columns:
        y = df['estado_inactivo']
        X = df.drop(columns=['estado_inactivo'])
    else:
        return JsonResponse({'error': 'No hay clientes inactivos para entrenar'}, status=400)

    # 3. Separar train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4. Entrenar modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # 5. Evaluar métricas
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    roc = roc_auc_score(y_test, modelo.predict_proba(X_test)[:, 1])

    # 6. Guardar modelo
    joblib.dump(modelo, 'prediccion/modelo_cliente.pkl')

    return JsonResponse({
        'accuracy': acc,
        'roc_auc': roc,
        'report': report
    })


@login_required
def predecir_abandono(request, cliente_id):
    if request.user.rol != 'admin':
        return HttpResponseForbidden("No tienes permiso para hacer predicciones")
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    # Cargar modelo
    try:
        modelo = joblib.load('predicciones/modelo_cliente.pkl')
    except FileNotFoundError:
        return JsonResponse({'error': 'Modelo no entrenado'}, status=400)

    # Preparar datos del cliente como dataframe
    df = pd.DataFrame([{
        'telefono': cliente.telefono,
        'estado': cliente.estado,
        'nivel_riesgo': cliente.nivel_riesgo,
    }])

    # Convertir variables categóricas igual que en entrenamiento
    df = pd.get_dummies(df, columns=['estado', 'nivel_riesgo'], drop_first=True)

    # Asegurarse que las columnas coincidan con el modelo
    modelo_cols = modelo.feature_names_in_
    for col in modelo_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[modelo_cols]

    # Hacer predicción
    probabilidad = modelo.predict_proba(df)[:, 1][0]

    return JsonResponse({
        'cliente': cliente.nombre,
        'probabilidad_abandono': round(probabilidad * 100, 2)
    })