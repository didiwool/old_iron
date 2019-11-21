import pickle

import pandas as pd
import numpy as np
from sklearn import preprocessing, metrics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
# import xgboost as xgb


dtype = {'suburb': str}

data = pd.read_csv("vic_property.csv", low_memory=False)
df = data[["latitude","longitude","bedrooms","bathrooms","parkingSpaces","propertyType","price"]]

df = df.dropna()
df["price"].replace('[$,]*', '', regex=True, inplace=True)
df["price"].replace('[A-z]', 0, regex=True, inplace=True)
df = df[df.price != 0]
df["price"] = df["price"].astype(int)
df.loc[df["propertyType"] == 'house', "propertyType"] = 0
df.loc[df["propertyType"] == 'apartment', "propertyType"] = 1
df.loc[df["propertyType"] == 'unit', "propertyType"] = 2
df.loc[df["propertyType"] == 'townhouse', "propertyType"] = 3
df["propertyType"].replace('[A-z]', 4, regex=True, inplace=True)
# print(df)
df["propertyType"] = df["propertyType"].astype(int)
print(type(df["propertyType"].values))
df = df[df.propertyType < 4]
df = df.dropna()
print(df.head())



X = df[["latitude","longitude","bedrooms","bathrooms","parkingSpaces","propertyType"]]

y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
lm = RandomForestRegressor()
# lm = LinearRegression()
lm.fit(X_train, y_train)
# lm.fit(X_train, y_train)
predicts = lm.predict(X_test)
filename = 'finalized_model.sav'
pickle.dump(lm, open(filename, 'wb'))
loaded_model = pickle.load(open(filename, 'rb'))

result = loaded_model.predict([[-38.238159,144.545576, 4, 2, 2, 0]])
print(result)
print("""
        Mean Squared Error: {}
        R2 Score: {}
        Mean Absolute Error: {}
     """.format(
        np.sqrt(metrics.mean_squared_error(y_test, predicts)),
        r2_score(y_test,predicts) * 100,
        mean_absolute_error(y_test,predicts)
        ))

print(lm.score(X_test,y_test))
