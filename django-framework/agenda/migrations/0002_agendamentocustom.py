# Generated by Django 4.2.4 on 2023-09-04 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendamentoCustom',
            fields=[
                ('agendamento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='agenda.agendamento')),
                ('prestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('agenda.agendamento',),
        ),
    ]
