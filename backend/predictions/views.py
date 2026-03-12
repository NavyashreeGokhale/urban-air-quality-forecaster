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
        
@csrf_exempt
def predict_network(request):

    if request.method == "GET":

        # Example node feature inputs
        nodes = {
            "node1": [10,20,30,40,50,60],
            "node2": [12,18,28,38,48,58],
            "node3": [14,16,26,36,46,56],
            "node4": [20,25,35,45,55,65],
            "node5": [30,35,40,45,50,55]
        }

        results = {}

        for node, features in nodes.items():
            results[node] = predict_aqi(features)

        return JsonResponse(results)
        

def test_page(request):
    return render(request, "test.html")

import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from mlcore.model_loader import predict_aqi


def pollution_graph(request):

    # Example node features
    nodes = {
        "node1": [10,20,30,40,50,60],
        "node2": [12,18,28,38,48,58],
        "node3": [14,16,26,36,46,56],
        "node4": [20,25,35,45,55,65],
        "node5": [30,35,40,45,50,55]
    }

    predictions = {}

    for node, features in nodes.items():
        predictions[node] = predict_aqi(features)

    # Create network
    G = nx.Graph()

    for node in predictions:
        G.add_node(node, aqi=predictions[node])

    # Example connections
    edges = [
        ("node1","node2"),
        ("node1","node3"),
        ("node2","node4"),
        ("node3","node4"),
        ("node4","node5")
    ]

    G.add_edges_from(edges)

    pos = nx.spring_layout(G)

    values = [predictions[n] for n in G.nodes]

    plt.figure(figsize=(6,6))
    nx.draw(G, pos,
            with_labels=True,
            node_color=values,
            cmap=plt.cm.Reds,
            node_size=1200)

    plt.title("Urban AQI Pollution Network")

    # Convert plot to image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode("utf-8")

    return JsonResponse({
        "graph": graph
    })
