# Generated by Django 5.2.3 on 2025-06-15 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_richiestaprenotazioneserata_stato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biglietto',
            name='tipo',
            field=models.CharField(choices=[('S', 'Standard'), ('T', 'Tavolo')], default='S', max_length=1),
        ),
    ]
