# coding : utf-8
import json
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from grade_parser.models import Program
from grade_parser.views import KeywordsNotFoundException

from .models import FBUser, UserKeyword
from recommender import Recommender


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

    if content:
        text = get_keywords_text(u"Apresentadora tambem faz um passeio com o Sacerdote em um carro antigo. Veja fotos!")
        keywords, relevancies = parse_keywords_and_relevancies(text)
        keyword_map = {}
        map(lambda (k, r): keyword_map.update({k: r}), zip(keywords, relevancies))
        Recommender().update_user_preference_vector(fb_id, keyword_map)

    return HttpResponse(content=json.dumps({"status": "OK"}), content_type="application/json")


def recommend(request, fb_id):
    recommendations = Recommender().recommend(fb_id)
    return HttpResponse(content_type='application/json', content=json.dumps(recommendations))


def like(request, fb_id, content_id):
    Recommender().recommend(fb_id)

    program = Program.objects.get(key=content_id)
    keyword_map = {}
    map(lambda (k, r): keyword_map.update({k: r}), program.keyword_set.values_list('text', 'relevancy'))
    Recommender().update_user_preference_vector(fb_id, keyword_map, content_id=content_id)

    return HttpResponse(status=200)


def unlike(request, fb_id, content_id):
    _recommender = Recommender()
    visited_content = _recommender.get_user_visited_content()
    print visited_content
    visited_content[fb_id].append(content_id)
    _recommender.save_user_visited_content(visited_content)
    return HttpResponse(status=200)
