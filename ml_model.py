import pickle

import pandas as pd
import numpy as np
from sklearn import preprocessing, metrics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
# import xgboost as xgb

from sklearn.tree import DecisionTreeRegressor

dtype = {'suburb': str}

data = pd.read_csv("Melbourne_housing_FULL.csv", low_memory=False)
df = data[['Rooms','Type','Price','Lattitude','Longtitude','Bedroom2','Bathroom','Car','YearBuilt', 'Landsize']]
# print(df1.head(5))

df = df.dropna()
df = df[df.Price != 0]
df = df[df.YearBuilt <= 2019]
df['YearBuilt'] = df['YearBuilt'].apply(lambda x: 2019-x)
# df = df[df.BuildingArea < 2230]
df = df[df.Landsize < 22000]
df = df[df.Bedroom2 < 7]
df = df[df.Bathroom < 5]

le = preprocessing.LabelEncoder()
le.fit(df['Type'])
df['Type'] = le.transform(df['Type'])

# le = preprocessing.LabelEncoder()
# le.fit(df['Method'])
# df['Method'] = le.transform(df['Method'])

# df.loc[df['property_type'] == 'Apartment', 'property_type'] = 0
# df.loc[df['property_type'] == 'House', 'property_type'] = 1
# df.loc[df['property_type'] == 'Townhouse', 'property_type'] = 2
# df['property_type'] = df['property_type'].replace('[A-z()]+', 3, regex=True)


df.sort_values(by='Price', ascending=True, inplace=True)
print(df)

lm = LinearRegression()

X = df[['Rooms','Type','Lattitude','Longtitude','Bedroom2','Bathroom','Car','YearBuilt', 'Landsize']]

y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
lm = GradientBoostingRegressor()
lm.fit(X_train, y_train)
# lm.fit(X_train, y_train)
predicts = lm.predict(X_test)
filename = 'finalized_model.sav'
pickle.dump(lm, open(filename, 'wb'))
print(X_test)
loaded_model = pickle.load(open(filename, 'rb'))

result = loaded_model.predict([[5, 0, -37.3, 145, 3, 2, 2, 8, 500]])
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

# predicts2 = lm.predict(X_test)
#
# print("""
#         Mean Squared Error: {}
#         R2 Score: {}
#         Mean Absolute Error: {}
#      """.format(
#         np.sqrt(metrics.mean_squared_error(y_test, predicts2)),
#         r2_score(y_test,predicts2) * 100,
#         mean_absolute_error(y_test,predicts2)
#         ))
#
error_airbnb = pd.DataFrame({
        'Actual Values': np.array(y_test).flatten(),
        'Predicted Values': predicts.flatten()}).head(20)

print(error_airbnb)
print(lm.score(X_test,y_test))


# import pickle
#
# import pandas as pd
# import numpy as np
# from sklearn import preprocessing, metrics
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
# from sklearn.externals import joblib
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_absolute_error, r2_score
# from sklearn.model_selection import train_test_split
# import xgboost as xgb
# # import xgboost as xgb
#
# from sklearn.tree import DecisionTreeRegressor
#
# dtype = {'suburb': str}
#
# data = pd.read_csv("Melbourne_housing_FULL.csv", low_memory=False)
# df = data[['Rooms','Type','Price','Lattitude','Longtitude','Bedroom2','Bathroom','Car','YearBuilt', 'BuildingArea']]
# # print(df1.head(5))
#
# df = df.dropna()
# df = df[df.Price != 0]
# df = df[df.YearBuilt <= 2019]
# df['YearBuilt'] = df['YearBuilt'].apply(lambda x: 2019-x)
# df = df[df.BuildingArea < 2230]
# # df = df[df.Landsize < 22000]
# df = df[df.Bedroom2 < 7]
# df = df[df.Bathroom < 5]
#
# le = preprocessing.LabelEncoder()
# le.fit(df['Type'])
# df['Type'] = le.transform(df['Type'])
# #
# # le = preprocessing.LabelEncoder()
# # le.fit(df['Method'])
# # df['Method'] = le.transform(df['Method'])
#
# # df.loc[df['property_type'] == 'Apartment', 'property_type'] = 0
# # df.loc[df['property_type'] == 'House', 'property_type'] = 1
# # df.loc[df['property_type'] == 'Townhouse', 'property_type'] = 2
# # df['property_type'] = df['property_type'].replace('[A-z()]+', 3, regex=True)
#
#
# df.sort_values(by='Price', ascending=True, inplace=True)
# print(df)
#
# lm = LinearRegression()
#
# X = df[['Rooms','Type','Lattitude','Longtitude','Bedroom2','Bathroom','Car','YearBuilt', 'BuildingArea']]
#
# y = df['Price']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)
# xgb_params = {
#     'eta': 0.05,
#     'max_depth': 5,
#     'subsample': 0.7,
#     'colsample_bytree': 0.7,
#     'objective': 'reg:linear',
#     'eval_metric': 'rmse',
#     'silent': 1
# }
# dtrain = xgb.DMatrix(X_train, y_train)
# num_boost_rounds = len(xgb.cv(xgb_params, dtrain, num_boost_round=1000, early_stopping_rounds=20,
#     verbose_eval=50, show_stdv=False))
# lm = xgb.train(dict(xgb_params, silent=0), dtrain, num_boost_round=num_boost_rounds)
# # lm.fit(X_train, y_train)
# # lm.fit(X_train, y_train)
# # predicts = lm.predict(X_test)
# dtest=xgb.DMatrix(X_test)
# y_predict = lm.predict(dtest)
# filename = 'finalized_model.sav'
# pickle.dump(lm, open(filename, 'wb'))
# print(X_test)
# loaded_model = pickle.load(open(filename, 'rb'))
#
# # result = loaded_model.predict([[-37.3, 145, 2, 1, 20, 3, 5, 3, 2]])
# # print(result)
# print("""
#         Mean Squared Error: {}
#         R2 Score: {}
#         Mean Absolute Error: {}
#      """.format(
#         np.sqrt(metrics.mean_squared_error(y_test, y_predict)),
#         r2_score(y_test,y_predict) * 100,
#         mean_absolute_error(y_test,y_predict)
#         ))
#
# # predicts2 = lm.predict(X_test)
# #
# # print("""
# #         Mean Squared Error: {}
# #         R2 Score: {}
# #         Mean Absolute Error: {}
# #      """.format(
# #         np.sqrt(metrics.mean_squared_error(y_test, predicts2)),
# #         r2_score(y_test,predicts2) * 100,
# #         mean_absolute_error(y_test,predicts2)
# #         ))
# #
# error_airbnb = pd.DataFrame({
#         'Actual Values': np.array(y_test).flatten(),
#         'Predicted Values': y_predict.flatten()}).head(20)
#
# print(error_airbnb)
# # print(lm.score(X_test,y_test))
