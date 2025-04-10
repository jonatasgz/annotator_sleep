from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Episode, Highlight, Predictions
from .serializers import EpisodeSerializer, HighlightSerializer, PredictionSerializer
import logging
from transformers import pipeline
import csv
from .tools import get_entities
from joblib import load

logger = logging.getLogger(__name__)

ner_pipeline = pipeline('ner', model="portugueseNLP/medialbertina_pt-pt_900m_NER", aggregation_strategy='average')

classifiers = {
    "depression": load("nlp/classifiers/depressao.joblib"),
    "pacemaker": load("nlp/classifiers/pacemaker.joblib"),
    "defibrillator": load("nlp/classifiers/cdi.joblib"),
    "arrhythmia": load("nlp/classifiers/arritmiafa.joblib"),
    "heart_failure": load("nlp/classifiers/icc.joblib"),
    "arterial_hypertension": load("nlp/classifiers/hta.joblib"),
    "ischemic_heart": load("nlp/classifiers/eam.joblib"),
    "cerebrovascular": load("nlp/classifiers/avcait.joblib"),
    "asthma": load("nlp/classifiers/asma.joblib"),
    "copd": load("nlp/classifiers/dpoc.joblib"),
    "diabetes": load("nlp/classifiers/dm.joblib"),
    "dyslipidemia": load("nlp/classifiers/dislipidemia.joblib"),
    "suffocation_waking": load("nlp/classifiers/sufocaçãoyesno.joblib"),
    "suffocation_waking_levels": load("nlp/classifiers/sufocaçãoniveis.joblib"),
    "snoring": load("nlp/classifiers/roncopatiayesno.joblib"),
    "snoring_levels": load("nlp/classifiers/roncopatianiveis.joblib"),
    "apneas": load("nlp/classifiers/apneiaspreyesno.joblib"),
    "apneas_levels": load("nlp/classifiers/apneiaspreniveis.joblib"),
    "insomnia": load("nlp/classifiers/insoniayesno.joblib"),
    "insomnia_levels": load("nlp/classifiers/insonianiveis.joblib")
}

TYPE_CHOICES = {
        "Diagnostico": "Diagnostic",
        "Sintoma": "Symptom",
        "Medicamento": "Drug",
        "ProcedimentoMedico": "Procedure",
        "SinalVital": "Vitals",
        "Progresso": "Outcome"
    }

@api_view(["POST"])
@permission_classes([AllowAny])
def get_episode(request):
    episode_data = request.data

    try:
        episode = Episode.objects.get(
            patient_id=episode_data["patient_id"],
            episode_date=episode_data["episode_date"],
        )
        message = "Existing episode loaded"

    except Episode.DoesNotExist:
        try:
            serializer = EpisodeSerializer(data=episode_data)
            serializer.is_valid(raise_exception=True)
            episode = serializer.save()
            message = "New episode created"
        except:
            return Response({"error": "Duplicate entry conflict"}, status=400)

    respose_data = EpisodeSerializer(episode).data

    return Response({'data': respose_data, "message": message})

@api_view(["POST"])
@permission_classes([AllowAny])
def submit_episode(request):
    episode_data = request.data
    episode = Episode.objects.get(patient_id = episode_data['patient_id'],
                                  episode_date = episode_data['episode_date'])
    serializer = EpisodeSerializer(instance=episode, data=episode_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Episode data saved"}, status=status.HTTP_202_ACCEPTED)

@api_view(["GET"])
@permission_classes([AllowAny])
def download_db(request):
    episodes = Episode.objects.all().order_by('patient_id', 'episode_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="episodes.csv"'

    writer = csv.writer(response)

    fields = [field.name for field in Episode._meta.fields if field]
    fields.remove('id')

    writer.writerow(fields)

    # Write data rows
    for episode in episodes:
        row = []
        for field in fields:
            value = getattr(episode, field)
            row.append(value)
        row = [getattr(episode, field) for field in fields]
        writer.writerow(row)

    return response

@api_view(["GET"])
@permission_classes([AllowAny])
def download_predictions(request):
    predictions = Predictions.objects.all().order_by('episode', 'creation_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predictions.csv"'

    writer = csv.writer(response)

    fields = [field.name for field in Predictions._meta.fields if field]
    fields.remove('id')

    writer.writerow(fields)

    # Write data rows
    for prediction in predictions:
        row = []
        for field in fields:
            if field == "episode":
                value = prediction.episode.patient_id
                row.append(value)
            else:
                value = getattr(prediction, field)
                row.append(value)
        writer.writerow(row)

    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def ner(request):
    free_text = request.data['text']
    automated_highlights = get_entities(free_text, ner_pipeline)
    return Response(automated_highlights)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def predict(request):
    if request.method == "POST":
        free_text = request.data['text']
        episode_id = request.data["episode"]
        episode = Episode.objects.get(pk = episode_id)
        prediction_fields = [f.name for f in Predictions._meta.get_fields()]
        for field in ["id", "episode", "creation_date"]:
            prediction_fields.remove(field)
        prediction_data = {"episode": episode}
        for field in prediction_fields:
            try:
                this_prediction = classifiers[field].predict([free_text])
                prediction_data[field] = this_prediction[0]
            except:
                logger.error(f"Could not predict {field} for episode {episode_id}")
        prediction, created = Predictions.objects.get_or_create(**prediction_data)
        if not created:
            logger.info(f"A repeated prediction was made for episode {episode_id}")
        serializer = PredictionSerializer(prediction)

        return Response(serializer.data)
    
    if request.method == "GET":
        episode_id = request.query_params.get("episode")
        print(episode_id)

        try:
            prediction = Predictions.objects.filter(episode=episode_id).order_by('-creation_date').first()
        
            if prediction:
                serializer = PredictionSerializer(prediction)
                return Response(serializer.data)
            else:
                return Response({})

        except Exception as e:
            logger.error(f"Error retrieving prediction for episode {episode_id}: {str(e)}")
            return Response({"detail": "Internal server error."}, status=500)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def highlights(request):
    if request.method == "GET":
        highlights_list = Highlight.objects.all()
        serializer = HighlightSerializer(highlights_list, many = True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = HighlightSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_highlight(request, pk):
    try:
        highlight = Highlight.objects.get(pk=pk)
    except Highlight.DoesNotExist:
        return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    highlight.delete()
    
    return Response(status=status.HTTP_204_NO_CONTENT)