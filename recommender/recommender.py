import numpy as np
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cosine

features_vec = None
content_id_vec = None
content_matrix = None
user_id_vec = None
user_pref_vec = None

FEATURES_VEC_DUMP = 'features_vec.dat'

def create_features_vec(db_keywords):
    features_vec = np.array(db_keywords)
    features_vec.dump(FEATURES_VEC_DUMP)

def get_features_vec()
    if features_vec is None:
        features_vec = np.load(FEATURES_VEC_DUMP)

def get_features_vec_as_list():
    return features_vec.tolist()

def recommend_from_vec(userid):
    recommendations = {}
    i = 0
    for content in content_matrix:
        cos = cosine(user_pref_vec[userid], content)
        i = i + 1
        recommendations[content_id_vec[i]] = cos
    return recommendations

