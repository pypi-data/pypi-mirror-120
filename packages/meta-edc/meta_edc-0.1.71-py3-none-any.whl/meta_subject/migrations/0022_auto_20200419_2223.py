# Generated by Django 3.0.4 on 2020-04-19 19:23

import django.core.validators
import edc_vitals.models.fields.blood_pressure
import edc_vitals.models.fields.height
import edc_vitals.models.fields.weight
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0021_auto_20200417_0332"),
    ]

    operations = [
        migrations.AddField(
            model_name="coronakap",
            name="dia_blood_pressure",
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(
                blank=True, null=True
            ),
        ),
        migrations.AddField(
            model_name="coronakap",
            name="diabetic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have diabetes?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coronakap",
            name="height",
            field=edc_vitals.models.fields.height.HeightField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="coronakap",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have HIV infection?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coronakap",
            name="hypertensive",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have hypertension?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coronakap",
            name="months_on_art",
            field=models.IntegerField(
                blank=True,
                help_text="in months",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="If yes, for how many months has the patient been on antiretroviral therapy?",
            ),
        ),
        migrations.AddField(
            model_name="coronakap",
            name="sys_blood_pressure",
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(
                blank=True, null=True
            ),
        ),
        migrations.AddField(
            model_name="coronakap",
            name="weight",
            field=edc_vitals.models.fields.weight.WeightField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="dia_blood_pressure",
            field=edc_vitals.models.fields.blood_pressure.DiastolicPressureField(
                blank=True, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="diabetic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have diabetes?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="height",
            field=edc_vitals.models.fields.height.HeightField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="hiv_pos",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have HIV infection?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="hypertensive",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                default="No",
                max_length=25,
                verbose_name="Does the patient have hypertension?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="months_on_art",
            field=models.IntegerField(
                blank=True,
                help_text="in months",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="If yes, for how many months has the patient been on antiretroviral therapy?",
            ),
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="sys_blood_pressure",
            field=edc_vitals.models.fields.blood_pressure.SystolicPressureField(
                blank=True, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalcoronakap",
            name="weight",
            field=edc_vitals.models.fields.weight.WeightField(blank=True, null=True),
        ),
    ]
