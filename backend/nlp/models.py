from django.db import models

# Model for the user specific words
class Highlight(models.Model):
    TYPE_CHOICES = {
        "Diagnostico": "Diagnóstico",
        "Sintoma": "Sintoma",
        "Medicamento": "Medicamento",
        "ProcedimentoMedico": "Procedimento Médico",
        "SinalVital": "Sinal Vital",
        "Progresso": "Progresso"
    }

    expression = models.CharField(null = False, blank = False, verbose_name = "Expression", unique = True)
    color = models.CharField(null = False, blank = False, verbose_name = "Highlight color")
    type = models.CharField(null = False, blank=False, choices = TYPE_CHOICES, verbose_name = "Type of entity")

    class Meta:
        verbose_name = 'Highlight'
        verbose_name_plural = 'Highlights'

    def str(self):
        return f"{self.expression}"

# Each entry in the database represents a patient episode.
# All data will be stored in the same model
class Episode(models.Model):
    patient_id = models.IntegerField(blank = False, null = False)
    episode_date = models.DateField(blank = False, null = False)
    creation_date = models.DateTimeField(auto_now_add=True, blank = False, null= False)
    gender = models.CharField(blank=True)
    birth_date = models.DateField(blank = True, null = True)
    weight = models.IntegerField(blank = True, null = True)
    height = models.IntegerField(blank = True, null = True)
    medication_list = models.TextField(blank = True)
    alcohol = models.CharField(blank = True)
    tobacco = models.CharField(blank = True)
    bariatric_surgery = models.CharField(blank = True)
    depression = models.CharField(blank = True)
    anxiety = models.CharField(blank = True)
    pacemaker = models.CharField(blank = True)
    defibrillator = models.CharField(blank = True)
    arrhythmia = models.CharField(blank = True)
    heart_failure = models.CharField(blank = True)
    arterial_hypertension = models.CharField(blank = True)
    ischemic_heart = models.CharField(blank = True)
    cerebrovascular = models.CharField(blank = True)
    asthma = models.CharField(blank = True)
    copd = models.CharField(blank = True)
    diabetes = models.CharField(blank = True)
    dyslipidemia = models.CharField(blank = True)
    renal_failure = models.CharField(blank = True)
    thyroid_disease = models.CharField(blank = True)
    dementia = models.CharField(blank = True)
    cancer = models.CharField(blank = True)
    ge_reflux = models.CharField(blank = True)
    glaucoma = models.CharField(blank = True)
    epworth_scale = models.IntegerField(blank = True, null = True)
    suffocation_waking = models.CharField(blank = True)
    suffocation_waking_levels = models.CharField(blank = True)
    snoring = models.CharField(blank = True)
    snoring_levels = models.CharField(blank = True)
    apneas = models.CharField(blank = True)
    apneas_levels = models.CharField(blank = True)
    insomnia = models.CharField(blank = True)
    insomnia_levels = models.CharField(blank = True)
    complete = models.BooleanField(blank = True, null = True)

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'
        unique_together = ['patient_id', 'episode_date']

    def str(self):
        return f"{self.patient_id} - {self.episode_date}"

class Predictions(models.Model):
    episode = models.ForeignKey(Episode, on_delete = models.CASCADE, related_name = "predictions", verbose_name = "Predictions")
    creation_date = models.DateTimeField(auto_now_add=True, blank = False, null= False)
    depression = models.CharField(blank = True)
    pacemaker = models.CharField(blank = True)
    defibrillator = models.CharField(blank = True)
    arrhythmia = models.CharField(blank = True)
    heart_failure = models.CharField(blank = True)
    arterial_hypertension = models.CharField(blank = True)
    ischemic_heart = models.CharField(blank = True)
    cerebrovascular = models.CharField(blank = True)
    asthma = models.CharField(blank = True)
    copd = models.CharField(blank = True)
    diabetes = models.CharField(blank = True)
    dyslipidemia = models.CharField(blank = True)
    suffocation_waking = models.CharField(blank = True)
    suffocation_waking_levels = models.CharField(blank = True)
    snoring = models.CharField(blank = True)
    snoring_levels = models.CharField(blank = True)
    apneas = models.CharField(blank = True)
    apneas_levels = models.CharField(blank = True)
    insomnia = models.CharField(blank = True)
    insomnia_levels = models.CharField(blank = True)

    class Meta:
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def str(self):
        return f"{self.episode}"
