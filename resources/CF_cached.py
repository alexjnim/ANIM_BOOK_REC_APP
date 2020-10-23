# -*- coding: utf-8 -*-
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
from google.oauth2 import service_account
import pandas_gbq
import pandas as pd
import numpy as np
import pickle
import re
import random
from random import randrange


def get_top_recommendations(ml, trainSet, no_recs, excluded, candidates):

    #sort the list of books by descending rating score
    c2 = sorted(candidates.items(), key=lambda item: item[1], reverse=True)
    maxval = c2[0][1]
    print('maxval: '+str(maxval))
    #count the numbero f candidates with maxval
    count_max_values = 0
    for itemID, ratingSum in c2:
        if ratingSum == maxval:
            count_max_values = count_max_values + 1
    print('number of candidates with max value: '+str(count_max_values))
    #put the top 60 candidates in dictionary, and exclude candidate if it is in excluded list
    track = 0
    if no_recs < 11:
        track_max = 60
    else:
        track_max = round((no_recs/10) * 55)
    maxval_candidates = {}

    if count_max_values < 60:
        for itemID, ratingSum in c2:
            if not itemID in excluded:
                track = track + 1
                maxval_candidates[itemID] = ratingSum
            else:
                continue
            if track == track_max:
                break
    else:
    #if there are more than 60 maxvals - add then all to dictionary
        for itemID, ratingSum in c2:
            if ratingSum == maxval:
                if not itemID in excluded:
                    maxval_candidates[itemID] = ratingSum
                else:
                    continue

    #shuffle the order of the top candiates
    itemIDs = list(maxval_candidates.keys())
    print('the number of max values are greater than desired recommendation : ' + str(len(itemIDs)))
    random_number = randrange(100)
    random.Random(random_number).shuffle(itemIDs)
    candidates = {}
    for i in itemIDs:
        candidates[i] = maxval
    #here get the top n recommendations and their details
    results = []
    recommended_itemIDs = []
    pos = 0

    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        recommended_itemIDs.append(itemID)
        rec_item = []
        bookID = trainSet.to_raw_iid(itemID)
        rec_item.append(ml.getItemName(int(bookID)))
        rec_item.append(ratingSum)
        rec_item.append(list(ml.getItemAuthors(int(bookID)).split(","))[0])
        rec_item.append(ml.getItemImage_URL(int(bookID)))

        itemName = ml.getItemName(int(bookID))
        itemName = re.sub(r'\([^)]*\)', '', itemName)
        tagged_search = itemName.replace(" ", "+").replace("#", "") + "+by+" + list(ml.getItemAuthors(int(bookID)).split(","))[0].replace(" ", "+").replace("#", "")
        search_link = "http://www.google.com/search?q="+tagged_search
        rec_item.append(search_link)
        results.append(rec_item)
        pos += 1
        if (pos > no_recs -1):
            break
    return results, itemIDs, recommended_itemIDs

def get_recommendations_cached(ml, no_recs, trainSet, kNeighbours):

    similarity_matrix = np.load('data/similarity_matrix.npy')

    candidates = defaultdict(float)
    appear = defaultdict(float)
    for itemID, rating in kNeighbours:
        similarity_row = similarity_matrix[itemID]
        for innerID, similarityScore in enumerate(similarity_row):
            candidates[innerID] += similarityScore * (rating / 5.0)
            appear[innerID] += 1.0

    # average out the ratings if they appear more than once
    for i in range(len(candidates)):
        candidates[i] = candidates[i]/(appear[i]-0.5)

    excluded = {}
    for itemID, rating in kNeighbours:
        excluded[itemID] = 1
    # Get top-rated items from similar users:
    results, itemIDs, recommended_itemIDs = get_top_recommendations(ml, trainSet, no_recs, excluded, candidates)
    return results, itemIDs

def get_recommendations_gbq(ml, no_recs, trainSet, kNeighbours):
    # get the recommendations by pulling simlarity rows from SQL database instead of cached data
    innerbookIDs = []
    for innerbookID, rating in kNeighbours:
        innerbookIDs.append(innerbookID)

    placeholders= ', '.join(str(innerbookID) for innerbookID in innerbookIDs)
    query= 'SELECT * FROM data.similarity_matrix_w_rownumber WHERE row IN (%s)' % placeholders

    credentials = service_account.Credentials.from_service_account_file(
        'data/public-viewer-book-rec-app-2-15084ef3a6b9.json',)

    df = pandas_gbq.read_gbq(query, project_id="book-rec-app-2", credentials=credentials)
    df = df.drop(columns=['row'])
    similarity_rows = df.to_numpy()

    #get the scores of all items and add them together with similarityScore weighting
    candidates = defaultdict(float)
    appear = defaultdict(float)
    for similarity_row in similarity_rows:
        for innerID, similarityScore in enumerate(similarity_row):
            candidates[innerID] += similarityScore * (rating / 5.0)
            appear[innerID] += 1.0

    #here divide the scores by the number of times they come up - 0.5
    for i in range(len(candidates)):
        candidates[i] = candidates[i]/(appear[i]-0.5)
    #get the itemID of books entered so we don't give recommendations of books that the user entered
    excluded = {}
    for itemID, rating in kNeighbours:
        excluded[itemID] = 1
    # Get top-rated items from similar users:
    results, itemIDs, recommended_itemIDs = get_top_recommendations(ml, trainSet, no_recs, excluded, candidates)

    return results, itemIDs, recommended_itemIDs


def item_based_rec_loader_cached_2(ml, no_recs, new_rows):

        trainSetPath = 'data/trainSet.pkl'
        with open(trainSetPath, 'rb') as file:
            trainSet = pickle.load(file)
        print('number of ratings:' + str(trainSet.n_ratings))

        kNeighbours = []
        for i in range(len(new_rows)):
            bookID = new_rows['book_id'][i]
            inner_itemID = trainSet.to_inner_iid(bookID)
            kNeighbours.append((inner_itemID, 5.0))

        # results, keys = get_recommendations_cached(ml, no_recs, trainSet, kNeighbours)
        results, itemIDs, recommended_itemIDs = get_recommendations_gbq(ml, no_recs, trainSet, kNeighbours)

        return results, itemIDs, recommended_itemIDs
