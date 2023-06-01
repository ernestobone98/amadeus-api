import pickle
from sklearn.preprocessing import LabelEncoder

class Encoder:
    def __init__(self):
        self.encoder = None

    def create_new_encoder(self):
        self.encoder = LabelEncoder()
        with open('encoder.pkl', 'wb') as f:
            pickle.dump(self.encoder, f)

    def get_encoder(self):
        with open('encoder.pkl', 'rb') as f:
            self.encoder = pickle.load(f)
        return self.encoder
