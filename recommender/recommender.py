import numpy as np
import pickle
from scipy.spatial.distance import cosine
from numpy.linalg import norm
from scipy.sparse import csr_matrix


class Recommender:

    keywords = None
    content_vectors = None
    user_preference_vectors = None
    user_visited_content = None
    USER_CONTENT_DUMP = 'user_content.dat'
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
            except Exception:
                self.keywords = []
        return self.keywords

    def get_content_vectors(self):
        if self.content_vectors is None:
            try:
                self.content_vectors = pickle.load(open(self.CONTENT_VEC_DUMP, "rb"))
            except Exception:
                self.content_vectors = {}
        return self.content_vectors

    def get_user_preference_vectors(self):
        if self.user_preference_vectors is None:
            try:
                self.user_preference_vectors = pickle.load(open(self.USER_PREF_VEC_DUMP, "rb"))
            except Exception:
                self.user_preference_vectors = {}
        return self.user_preference_vectors

    def get_user_visited_content(self):
        if self.user_visited_content is None:
            try:
                self.user_visited_content = pickle.load(open(self.USER_CONTENT_DUMP, "rb"))
            except Exception:
                self.user_visited_content = {}
        return self.user_visited_content

    def save_user_preference_vector(self, user_preference_vectors):
        self.user_preference_vectors = user_preference_vectors
        pickle.dump(self.user_preference_vectors, open(self.USER_PREF_VEC_DUMP, "wb"))

    def save_content_vectors(self, content_vectors):
        self.content_vectors = content_vectors
        pickle.dump(self.content_vectors, open(self.CONTENT_VEC_DUMP, "wb"))

    def save_user_visited_content(self, user_visited_content):
        self.user_visited_content = user_visited_content
        pickle.dump(self.user_visited_content, open(self.USER_CONTENT_DUMP, "wb"))

    def create_content_vector(self, content_keywords):
        keywords = self.get_keywords()
        content_vector = np.zeros(len(keywords))
        for i, keyword in enumerate(keywords):
            content_vector[i] = content_keywords.get(keyword, 0.0)
        return content_vector

    def add_content_vector(self, content_id, content_keywords):
        content_vector = self.create_content_vector(content_keywords)
        content_vectors = self.get_content_vectors()
        content_vectors[content_id] = content_vector
        self.save_content_vectors(content_vectors)

    def update_user_preference_vector(self, user_id, content_keywords, content_id=None):
        user_visited_content = self.get_user_visited_content()
        preference_vectors = self.get_user_preference_vectors()

        has_index = user_id in user_visited_content

        if not has_index or content_id is None:
            user_visited_content[user_id] = []

            if content_id is not None:
                user_visited_content[user_id].append(content_id)

            user_pref_vec = []
            # content_vector = self.create_content_vector(content_keywords)
            content_vector = self.create_content_vector({u'carro velho': 0.1})
            user_pref_vec.append(content_vector)
            preference_vectors[user_id] = user_pref_vec
        elif content_id not in user_visited_content[user_id]:
            user_visited_content[user_id].append(content_id)

            user_pref_vec = preference_vectors[user_id]

            content_vector = self.create_content_vector(content_keywords)
            user_pref_vec = user_pref_vec.add(content_vector) / 2
            preference_vectors[user_id] = user_pref_vec

        self.save_user_visited_content(user_visited_content)
        self.save_user_preference_vector(preference_vectors)

    def recommend(self, user_id):
        recommendations = {'recommendations': []}
        user_pref_vecs = self.get_user_preference_vectors()
        if user_id in user_pref_vecs:
            user_pref_vec = np.array(user_pref_vecs[user_id])
            user_visited_content = self.get_user_visited_content()
            for content_id, content_vec in self.get_content_vectors().iteritems():
                if (user_pref_vec.sum() != 0.0) and (content_vec.sum() != 0.0) and str(content_id) not in user_visited_content[user_id]:
                    similarity = user_pref_vec.dot(content_vec) / (norm(user_pref_vec) * norm(content_vec))
                    print 'sim2: %f' % similarity
                    if similarity > 0.0:
                        recommendations['recommendations'].append({'globo_id': content_id, 'weight': similarity[0]})
        return recommendations
