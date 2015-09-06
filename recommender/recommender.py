import numpy as np
import pickle
from scipy.spatial.distance import cosine


class Recommender:

    keywords = None
    content_vectors = None
    user_preference_vectors = None
    KEYWORDS_DUMP = 'keywords_vec.dat'
    CONTENT_VEC_DUMP = 'content_vec.dat'
    USER_PREF_VEC_DUMP = 'user_pref_vec.dat'

    def set_keywords(self, keywords_list):
        self.keywords = keywords_list
        pickle.dump(self.keywords, open(self.KEYWORDS_DUMP, "wb"))

    def get_keywords(self):
        if self.keywords is None:
            try:
                self.keywords = pickle.load(open(self.KEYWORDS_DUMP, "rb"))
            except pickle.PickleError:
                self.keywords = []

    def get_content_vectors(self):
        if self.content_vectors is None:
            try:
                self.content_vectors = pickle.load(open(self.CONTENT_VEC_DUMP, "rb"))
            except pickle.PickleError:
                self.content_vectors = {}
        return self.content_vectors

    def get_user_preference_vectors(self):
        if self.user_preference_vectors is None:
            try:
                self.user_preference_vectors = pickle.load(open(self.USER_PREF_VEC_DUMP, "rb"))
            except pickle.PickleError:
                self.user_preference_vectors = {}
        return self.user_preference_vectors

    def save_user_preference_vector(self, user_preference_vectors):
        self.user_preference_vectors = user_preference_vectors
        pickle.dump(self.user_preference_vectors, open(self.USER_PREF_VEC_DUMP, "wb"))

    def save_content_vectors(self, content_vectors):
        self.content_vectors = content_vectors
        pickle.dump(self.content_vectors, open(self.CONTENT_VEC_DUMP, "wb"))

    def create_content_vector(self, content_keywords):
        keywords = self.get_keywords()
        content_vector = np.zeros(len(keywords))
        for keyword in keywords:
            content_vector[keyword] = content_keywords.get(keyword, 0.0)
        return content_vector

    def add_content_vector(self, content_id, content_keywords):
        content_vector = self.create_content_vector(content_keywords)
        content_vectors = self.get_content_vectors()
        content_vectors[content_id] = content_vector
        self.save_content_vectors(content_vectors)

    def update_user_preference_vector(self, user_id, content_keywords):
        user_pref_vec = self.get_user_preference_vectors()[user_id]
        content_vector = self.create_content_vector(content_keywords)
        user_pref_vec = user_pref_vec.add(content_vector)/2
        self.get_user_preference_vectors()[user_id] = user_pref_vec

    def recommend(self, user_id):
        recommendations = {}
        user_pref_vec = self.get_user_preference_vectors()[user_id]
        for content_id, content_vec in self.get_content_vectors():
            similarity = cosine(user_pref_vec, content_vec)
            recommendations[content_id] = similarity
        return recommendations
