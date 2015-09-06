import json
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from grade_parser.views import KeywordsNotFoundException

from .models import FBUser, UserKeyword


BLUEMIX_URL = 'http://grupo1-nodered.mybluemix.net/keywords/'


def get_keywords_text(text):
    return requests.post(BLUEMIX_URL, data=text, headers={"charset": "utf-8"}).content.strip().lower()


def parse_keywords_and_relevancies(keywords_text):
    if keywords_text == ";":
        raise KeywordsNotFoundException()

    keywords_raw, relevancies_raw = keywords_text.split(";")

    keywords = map(lambda k: k.strip(), keywords_raw.split(","))
    relevancies = map(lambda k: float(k.strip()), relevancies_raw.split(","))

    return keywords, relevancies


def save_keywords(user, keywords, relevancies):
    for keyword, relevancy in zip(keywords, relevancies):
        UserKeyword.objects.create(user=user, text=keyword, relevancy=relevancy)


@csrf_exempt
def create_user_preferences(request, fb_id):
    content = json.loads(request.body)

    user, created = FBUser.objects.get_or_create(fb_id=fb_id)

    if created and content:
        text = get_keywords_text(content['fb_content'])
        keywords, relevancies = parse_keywords_and_relevancies(text)
        save_keywords(user, keywords, relevancies)

    return HttpResponse(content=json.dumps({"status": "OK"}), content_type="application/json")
