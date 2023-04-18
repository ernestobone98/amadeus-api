import pickle
from sklearn.preprocessing import LabelEncoder

def create_new_encoder():
    label_encoder = LabelEncoder()
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    return label_encoder

def get_encoder():
    with open('encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    return label_encoder
