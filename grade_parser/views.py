# coding: utf-8
import requests
import json

from django.http.response import HttpResponse, Http404
from grade_parser.models import Program, Keyword

from recommender import Recommender


class KeywordsNotFoundException(Exception):
    pass


def _get_slots_from_globo_api(url):
    str_content = requests.get(url).content
    content = json.loads(str_content)
    slots = content['gradeProgramacao']['slots']

    fields = ["resumo", "id", "id_programa"]

    for slot in slots:
        for key in slot.keys():
            if key not in fields:
                del slot[key]

    return slots


def get_keywords_text_of_slot(slot, post_url):
    data = slot["resumo"].lower().strip().encode('utf-8', 'ignore')
    return requests.post(post_url, data=data, headers={"charset": "utf-8"}).content.strip().lower()


def parse_keywords_and_relevancies(keywords_text):
    if keywords_text == ";":
        raise KeywordsNotFoundException()

    keywords_raw, relevancies_raw = keywords_text.split(";")

    keywords = map(lambda k: k.strip(), keywords_raw.split(","))
    relevancies = map(lambda k: float(k.strip()), relevancies_raw.split(","))

    return keywords, relevancies


def save_keywords(program, keywords, relevancies):
    for keyword, relevancy in zip(keywords, relevancies):
        Keyword.objects.create(program=program, text=keyword, relevancy=relevancy)


def fetch_api(request):
    api_url = request.GET.get("api_url")
    post_url = request.GET.get("post_url")

    if api_url is None or post_url is None:
        raise Http404()

    slots = _get_slots_from_globo_api(api_url)

    for slot in slots:
        program, created = Program.objects.get_or_create(key=slot["id"])

        if not created:
            print "program %d passed" % slot["id"]
            continue

        keywords_text = get_keywords_text_of_slot(slot, post_url)

        try:
            keywords, relevancies = parse_keywords_and_relevancies(keywords_text)
            save_keywords(program, keywords, relevancies)
        except KeywordsNotFoundException as e:
            print "keywords not found for slot %d" % slot['id']

    return HttpResponse(content="OK", content_type="text/plain")


def _load_api_data():
    dia = 1
    while dia <= 31:
        api_url = "http://redeglobo.globo.com/programacao/grade/2015-09-01/grade.json"
        post_url = "http://grupo1-nodered.mybluemix.net/keywords/"
        slots = _get_slots_from_globo_api(api_url)

        for slot in slots:
            program, created = Program.objects.get_or_create(key=slot["id"])

            if not created:
                print "program %d passed" % slot["id"]
                continue

            keywords_text = get_keywords_text_of_slot(slot, post_url)

            try:
                keywords, relevancies = parse_keywords_and_relevancies(keywords_text)
                save_keywords(program, keywords, relevancies)
            except KeywordsNotFoundException as e:
                print "keywords not found for slot %d" % slot['id']

        dia += 1



def set_keywords(request):
    _recommender = Recommender()
    _recommender.set_keywords(Keyword.objects.keyword_array())

    for program in Program.objects.all():
        keyword_map = {}
        map(lambda (k, r): keyword_map.update({k: r}), program.keyword_set.values_list('text', 'relevancy'))
        _recommender.add_content_vector(program.key, keyword_map)

    return HttpResponse(content="OK")


def get_keywords(request):
    _recommender = Recommender()
    vec = _recommender.get_keywords()
    return HttpResponse(content=str(vec))
