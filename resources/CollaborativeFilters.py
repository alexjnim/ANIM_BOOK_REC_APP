# -*- coding: utf-8 -*-
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
import pandas as pd

def get_recommendations(ml, no_recs, trainSet, similarity_matrix, kNeighbours, userIDInnerID, rec_type):
    # candidates will hold all possible items and combined rating from all k users
    # defaultdict will make all values in dictionary 0 by default
    candidates = defaultdict(float)

    # appearance = defaultdict(float)
    # Get similar items to stuff we liked (weighted by rating)
    if rec_type == 'item':
        for itemID, rating in kNeighbours:
            similarity_row = similarity_matrix[itemID]
            for innerID, similarityScore in enumerate(similarity_row):
                candidates[innerID] += similarityScore * (rating / 5.0)
    elif rec_type == 'user':
        # Get the stuff the k users rated, and add up ratings for each item, weighted by user similarity
        for similarUser in kNeighbours:
            innerID = similarUser[0]
            userSimilarityScore = similarUser[1]
            # this will hold all the items they've rated and the ratings for each of those items
            theirRatings = trainSet.ur[innerID]
            for rating in theirRatings:
                # weight the neighbouring ratings with the similarity score
                candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore

    # Build a dictionary of stuff the user has already seen
    excluded = {}
    for itemID, rating in trainSet.ur[userIDInnerID]:
        excluded[itemID] = 1

    results = []
    # Get top-rated items from similar users:
    pos = 0
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in excluded:
            rec_item = []
            bookID = trainSet.to_raw_iid(itemID)
            rec_item.append(ml.getItemName(int(bookID)))
            rec_item.append(ratingSum)
            rec_item.append(list(ml.getItemAuthors(int(bookID)).split(","))[0])
            rec_item.append(ml.getItemImage_URL(int(bookID)))

            tagged_search = ml.getItemName(int(bookID)).replace(" ", "+").replace("#", "") + "+by+" + list(ml.getItemAuthors(int(bookID)).split(","))[0].replace(" ", "+").replace("#", "")
            search_link = "http://www.google.com/search?q="+tagged_search
            rec_item.append(search_link)

            results.append(rec_item)
            pos += 1
            if (pos > no_recs -1):
                break
    return results

def item_based_rec_loader(data, ml, userID, no_recs):

    trainSet = data.build_full_trainset()
    # note that user_base: False here, thus we are telling KNN that
    # we want to generate an item-item based similarity matrix
    sim_options = {'name': 'cosine',
                   'user_based': False
                   }
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainSet)
    similarity_matrix = model.compute_similarities()
    userIDInnerID = trainSet.to_inner_uid(userID)

    # Get the top K items we rated
    k = 15
    userIDRatings = trainSet.ur[userIDInnerID]
    kNeighbours = heapq.nlargest(k, userIDRatings, key=lambda t: t[1])

    # kNeighbours = []
    # userIDRatings = trainSet.ur[userIDInnerID]
    # for rating in userIDRatings:
    #    if rating[1] > 4.0:
    #        kNeighbours.append(rating)

    results = get_recommendations(ml, no_recs, trainSet, similarity_matrix, kNeighbours, userIDInnerID, rec_type = 'item')
    return results

def user_based_rec_loader(data, ml, userID, no_recs):
    trainSet = data.build_full_trainset()
    sim_options = {'name': 'cosine',
               'user_based': True
               }
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainSet)
    similarity_matrix = model.compute_similarities()
    userIDInnerID = trainSet.to_inner_uid(userID)
    similiarty_row = similarity_matrix[userIDInnerID]

    # removing the testUser from the similiarty_row
    similarUsers = []
    for innerID, score in enumerate(similiarty_row):
        if (innerID != userIDInnerID):
            similarUsers.append( (innerID, score))

    # find the k users largest similarities
    k = 15
    kNeighbours = heapq.nlargest(k, similarUsers, key=lambda t: t[1])

#     or can tune for ratings > threshold
#     kNeighbours = []
#     for rating in similarUsers:
#        if rating[1] > 4.0:
#            kNeighbours.append(rating)

    results = get_recommendations(ml, no_recs, trainSet, similarity_matrix, kNeighbours, userIDInnerID, rec_type = 'user')
    return results
