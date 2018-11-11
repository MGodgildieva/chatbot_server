import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from appserver import services


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = services.register_user(body['username'], body['email'],
                                          body['password'], body['lang'])
    else:
        response = JsonResponse({"error": "Wrong method!"})

    return response


@csrf_exempt
def register_child(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = services.register_child(body['firstname'], body['parent_id'],
                                           body['birthday'])
    else:
        response = JsonResponse({"error": "Wrong method!"})
    return response


@csrf_exempt
def login(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = services.login_user(body['email'], body['password'])
    else:
        response = JsonResponse({"error": "Wrong method!"})
    return response


@csrf_exempt
def get_results(request):
    if request.method == "GET":
        response = services.start_conversation(request.GET.get('child_id'))
    else:
        response = {"error": "Wrong method!"}
    return JsonResponse(response)


@csrf_exempt
def get_all_results(request):
    if request.method == "GET":
        response = services.get_all_results(request.GET.get('parent_id'))
    else:
        response = {"error": "Wrong method!"}
    return JsonResponse(response)


@csrf_exempt
def add_result(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = services.add_result(body['child_id'], body['test_id'], body['value'])
    else:
        response = {"error": "Wrong method!"}
    return JsonResponse(response, safe=False)

@csrf_exempt
def process_message(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response = services.process_message(body['test_id'], body['child_id'], body['text'])
    else:
        response = {"error": "Wrong method!"}
    return JsonResponse(response)
