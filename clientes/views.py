import pandas as pd
from django.contrib import messages
from .forms import UploadFileForm
from django.shortcuts import render, redirect
from ml.predict import predict_churn
from ml.chatbot import chatbot_response
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cliente

# ----------------------------
# Predicción de churn
# ----------------------------
def predecir_churn(request):
    resultado = None
    probabilidad = None

    if request.method == "POST":
        data = [
            int(request.POST["edad"]),
            int(request.POST["antiguedad_meses"]),
            int(request.POST["frecuencia_uso"]),
            int(request.POST["reclamos"]),
            int(request.POST["pagos_atrasados"]),
        ]

        resultado, probabilidad = predict_churn(data)

        # Guardar en la base de datos si seleccionamos un cliente existente
        cliente_id = request.POST.get("cliente_id")
        if cliente_id:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.churn_probabilidad = probabilidad
            cliente.churn_riesgo = "Alto" if probabilidad > 70 else "Medio" if probabilidad > 40 else "Bajo"
            cliente.save()


# ----------------------------
# Chatbot básico
# ----------------------------
@login_required
def chat_churn(request):
    respuesta = None
    empresa_usuario = getattr(request.user, "empresa", None)

    if request.method == "POST":
        mensaje = request.POST.get("mensaje")
        respuesta = chatbot_response(mensaje)

    return render(request, "clientes/chat.html", {
        "respuesta": respuesta
    })


# ----------------------------
# Verificar rol Analista o admin
# ----------------------------
def es_analista_o_admin(user):
    return user.groups.filter(name='Analista').exists() or user.is_superuser


# ----------------------------
# Dashboard
# ----------------------------
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Analista').exists() or u.is_superuser)
def dashboard(request):
    # Empresa del usuario logueado
    empresa_usuario = request.user.empresa  # esto viene del modelo UserProfile o User extendido
    
    # Filtrar clientes por empresa
    clientes = Cliente.objects.filter(empresa=empresa_usuario)
    
    total_clientes = clientes.count()
    clientes_activos = clientes.filter(activo=True).count()
    clientes_en_riesgo = clientes.filter(activo=True, frecuencia_uso__lte=2).count()  # ejemplo simple de riesgo
    porcentaje_churn = round((clientes_en_riesgo / total_clientes) * 100, 2) if total_clientes else 0

    context = {
        "total_clientes": total_clientes,
        "clientes_activos": clientes_activos,
        "clientes_en_riesgo": clientes_en_riesgo,
        "porcentaje_churn": porcentaje_churn,
    }

    return render(request, "clientes/dashboard.html", context)


# ----------------------------
# Subida de clientes desde CSV/Excel
# ----------------------------
@login_required
@user_passes_test(es_analista_o_admin)
def subir_clientes(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Soporte para CSV y Excel
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, "Formato no soportado. Solo CSV o Excel.")
                    return redirect('subir_clientes')

                # Validar columnas obligatorias
                required_columns = ['nombre', 'email', 'edad', 'antiguedad_meses', 'frecuencia_uso', 'reclamos', 'pagos_atrasados']
                for col in required_columns:
                    if col not in df.columns:
                        messages.error(request, f"Falta la columna requerida: {col}")
                        return redirect('subir_clientes')

                empresa_usuario = getattr(request.user, "empresa", None)

                # Guardar clientes en la base de datos
                for _, row in df.iterrows():
                    Cliente.objects.update_or_create(
                        email=row['email'],
                        defaults={
                            'nombre': row['nombre'],
                            'edad': row['edad'],
                            'antiguedad_meses': row['antiguedad_meses'],
                            'frecuencia_uso': row['frecuencia_uso'],
                            'reclamos': row['reclamos'],
                            'pagos_atrasados': row['pagos_atrasados'],
                            'activo': row.get('activo', True),
                            'empresa': empresa_usuario
                        }
                    )

                messages.success(request, "Clientes cargados correctamente.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
    else:
        form = UploadFileForm()

    return render(request, 'clientes/subir_clientes.html', {'form': form})
