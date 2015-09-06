import numpy as np
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cosine


class Recommender:
    features_vec = None
    content_id_vec = None
    content_matrix = None
    user_id_vec = None
    user_pref_vec = None
    FEATURES_VEC_DUMP = 'features_vec.dat'

    def create_features_vec(self, db_keywords):
        self.features_vec = np.array(db_keywords)
        self.features_vec.dump(self.FEATURES_VEC_DUMP)

    def get_features_vec(self):
        if self.features_vec is None:
            self.features_vec = np.load(self.FEATURES_VEC_DUMP)
        return self.features_vec

    def get_features_vec_as_list(self):
        return self.get_features_vec().tolist()

    def recommend_from_vec(self, userid):
        recommendations = {}
        i = 0
        for content in content_matrix:
            cos = cosine(user_pref_vec[userid], content)
            i = i + 1
            recommendations[self.content_id_vec[i]] = cos
        return recommendations

