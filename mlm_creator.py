from joblib import dump
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.neural_network import MLPClassifier


def train_model():
    data = pd.read_csv('flight_offers.csv')

    # Variable X contains all the features
    X = data.drop(['total'], axis=1)
    # Variable y contains the target variable
    y = data['total']

    # Considering that the dataset is already cleaned, we split the dataset into train and test
    # We use 70% of the dataset for training and 30% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0) # Is not necessary to stratify the dataset

    # We will use MLPClassifier to train the model
    model = MLPClassifier(hidden_layer_sizes=(200,))
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    dump(model, "MLPC.joblib")

    print(accuracy_score(y_test, y_predict))
    print(classification_report(y_test, y_predict))

if __name__ == "__main__":
    train_model()