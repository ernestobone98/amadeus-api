from joblib import dump
from sklearn import ensemble
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd


def train_model():
    data = pd.read_csv('flight_offers.csv')

    # Variable X contains all the features
    X = data.drop(['total'], axis=1)
    # Variable y contains the target variable
    y = data['total']

    # Considering that the dataset is already cleaned, we split the dataset into train and test
    # We use 70% of the dataset for training and 30% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0) # Is not necessary to stratify the dataset

    # We will use a regression model to predict the total price of the flight
    model = ensemble.RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    dump(model, "Regression.joblib")

    mse = mean_squared_error(y_test, y_predict)
    print("Mean Squared Error:", mse)
    print(r2_score(y_test, y_predict))

if __name__ == "__main__":
    train_model()