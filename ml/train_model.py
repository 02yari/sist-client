import os
import sys
import django
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Agregar la raíz del proyecto al PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


# Configurar Django para usar los modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churn_prediction.settings')
django.setup()

from clientes.models import Cliente

# Leer datos desde la base de datos
clientes = Cliente.objects.all().values(
    'edad',
    'antiguedad_meses',
    'frecuencia_uso',
    'reclamos',
    'pagos_atrasados',
    'activo'
)

# Convertir a DataFrame
df = pd.DataFrame(clientes)

# Convertir activo a 0 y 1
df['activo'] = df['activo'].astype(int)

print("Dataset generado:")
print(df)
# -----------------------------------------
# Preparar datos
# -----------------------------------------
X = df[["edad", "antiguedad_meses", "frecuencia_uso", "reclamos", "pagos_atrasados"]]
y = df["activo"]

# -----------------------------------------
#  Dividir datos
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------------
# Entrenar modelo
# -----------------------------------------
model = LogisticRegression()
model.fit(X_train, y_train)

# -----------------------------------------
# Evaluar modelo
# -----------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy del modelo: {accuracy:.2f}")

# -----------------------------------------
# Guardar modelo
# -----------------------------------------
joblib.dump(model, "ml/model.pkl")

print("Modelo entrenado y guardado correctamente")