from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from mlcore.model_loader import predict_aqi
from django.shortcuts import render



@csrf_exempt
def predict(request):

    if request.method == "GET":
        return JsonResponse({
            "message": "AQI Prediction API running. Send POST request with features."
        })

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            features = data.get("features")

            if not features:
                return JsonResponse({"error": "Features missing"}, status=400)

            result = predict_aqi(features)

            return JsonResponse({
                "predicted_aqi": result
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

def test_page(request):
    return render(request, "test.html")