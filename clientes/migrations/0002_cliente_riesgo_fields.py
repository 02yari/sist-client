from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="probabilidad_abandono",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="nivel_riesgo",
            field=models.CharField(
                choices=[("Bajo", "Bajo"), ("Medio", "Medio"), ("Alto", "Alto")],
                default="Bajo",
                max_length=10,
            ),
        ),
    ]
