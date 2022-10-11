from math import fabs
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from flask import jsonify
import json
import openpyxl
import pprint


r_cols = ['user_id', 'item_id', 'rating']
uuCF = 1
k = 2
dist_func = cosine_similarity
Y_data = pd.read_excel('CF\data.xlsx', names=r_cols).values
Ybar_data = Y_data.copy()
n_users = int(np.max(Y_data[:, 0])) + 1
n_items = int(np.max(Y_data[:, 1])) + 1

mu = np.zeros((n_users,))

Ybar = sparse.coo_matrix((Ybar_data[:, 2],
                          (Ybar_data[:, 1], Ybar_data[:, 0])), (n_items, n_users)).tocsr()

S = dist_func(Ybar.T, Ybar.T)


def add(new_data):
    Y_data = np.concatenate((Y_data, new_data), axis=0)


def normalize_Y():
    users = Y_data[:, 0]
    for n in range(n_users):
        ids = np.where(users == n)[0].astype(np.int32)
        item_ids = Y_data[ids, 1]
        ratings = Y_data[ids, 2]
        mu[n] = np.mean(ratings)
        Ybar_data[ids, 2] = ratings - mu[n]

    Ybar = sparse.coo_matrix((Ybar_data[:, 2],
                              (Ybar_data[:, 1], Ybar_data[:, 0])), (n_items, n_users))
    Ybar = Ybar.tocsr()


def similarity():
    S = dist_func(Ybar.T, Ybar.T)


def fit():
    normalize_Y()
    similarity()


def pred(u, i, normalized=1):
    ids = np.where(Y_data[:, 1] == i)[0].astype(np.int32)
    users_rated_i = (Y_data[ids, 0]).astype(np.int32)
    sim = S[u, users_rated_i]
    a = np.argsort(sim)[-k:]
    nearest_s = sim[a]
    r = Ybar[i, users_rated_i[a]]
    if normalized:
        return (r*nearest_s)[0]/np.abs(nearest_s).sum()

    return (r*nearest_s)[0]/np.abs(nearest_s).sum() + mu[n]


def recommend(u):
    ids = np.where(Y_data[:, 0] == u)[0]
    items_rated_by_u = Y_data[ids, 1].tolist()
    recommended_items = []
    for i in range(n_items):
        if i not in items_rated_by_u:
            rating = pred(u, i)
            if rating > 0:
                recommended_items.append(i)

    return recommended_items


def print_recommendation():
    fit()
    print('Recommendation: ')
    for u in range(n_users):
        recommended_items = recommend(u)
        print('    for user ', u, ': ', recommended_items)


class RV(object):
    def __init__(self, user_id, array_film_id):
        self.user_id = user_id
        self.array_film_id = array_film_id


def get_recommendation():
    fit()
    arr = []
    for u in range(n_users):
        recommended_items = RV(u, array_film_id=recommend(u))
        arr.append(recommended_items)
    return json.dumps([item.__dict__ for item in arr])


def update_data(user_id, item_id, rating):
    path = 'CF\data.xlsx'
    Y_data = pd.read_excel(path, names=r_cols).values
    max_row = len(Y_data)
    max_column = 3
    wb_obj = openpyxl.load_workbook(path)
    sheet = wb_obj['Sheet1']
    sheet_obj = wb_obj.active
    isExisted = False
    for i in range(1, max_row + 1):
        for j in range(1, max_column + 1):
            USER_ID = sheet_obj.cell(row=i, column=1)
            ITEM_ID = sheet_obj.cell(row=i, column=2)
            if USER_ID == user_id and ITEM_ID == item_id:
                sheet.cell(row=i, column=3, value=rating)
                isExisted = True
                break
    if isExisted:
        sheet.cell(row=max_row + 1, column=1, value=user_id)
        sheet.cell(row=max_row+1, column=2, value=item_id)
        sheet.cell(row=max_row+1, column=3, value=rating)
    wb_obj.save(path)

# get_recommendation()
# print_recommendation()
