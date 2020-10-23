import os
import csv
import sys
import re
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
import numpy as np
import pandas as pd

class DataLoader:

    def __init__(self, items_path, ratings_path, userID_column, itemID_column, ratings_column, itemName_column, rating_scale_min, rating_scale_max):
        self.itemsPath = items_path
        self.ratingsPath = ratings_path
        self.itemID_column = itemID_column
        self.userID_column = userID_column
        self.ratings_column = ratings_column
        self.itemName_column = itemName_column
        self.rating_scale_min = rating_scale_min
        self.rating_scale_max = rating_scale_max
        self.items_df = pd.read_csv(self.itemsPath)
        self.ratings_df = pd.read_csv(self.ratingsPath)

    def loadData(self, size_of_data):
        ratings_extracted = self.ratings_df.sample(n=size_of_data)
        ratings_extracted = ratings_extracted[[self.userID_column, self.itemID_column, self.ratings_column]]
        reader = Reader(rating_scale=(self.rating_scale_min, self.rating_scale_max))
        self.ratingsDataset = Dataset.load_from_df(ratings_extracted, reader)

        return self.ratingsDataset

    def addUserLoadData(self, new_rows, size_of_data):
        #get random sample of the data
        ratings_extracted = self.ratings_df.sample(n=size_of_data)
        ratings_extracted = pd.concat([ratings_extracted, new_rows], ignore_index=True)
        ratings_extracted = ratings_extracted[[self.userID_column, self.itemID_column, self.ratings_column]]
        print('number of ratings used: '+str(len(ratings_extracted)))
        reader = Reader(rating_scale=(self.rating_scale_min, self.rating_scale_max))
        self.ratingsDataset = Dataset.load_from_df(ratings_extracted, reader)

        return self.ratingsDataset

    def getUserRatings(self, user):
        userRatings = self.ratings_df[self.ratings_df[self.userID_column] == 1][[self.itemID_column, self.ratings_column]]
        return userRatings

    def getPopularityRanks(self):
        popularity_rankings = self.ratings_df[self.itemID_column].value_counts()
        rankings = pd.Series(range(1, len(popularity_rankings) +1, 1), index = popularity_rankings.index)
        return rankings

    def getItemName(self, itemID):
        if itemID in list(self.items_df[self.itemID_column]):
            return self.items_df[self.itemName_column][self.items_df[self.itemID_column] == itemID].iloc[0]
        else:
            return "Not available"

    def getItemID(self, itemName):
        if itemName in list(self.items_df[self.itemName_column]):
            return self.items_df[self.itemID_column][self.items_df[self.itemName_column] == itemName].iloc[0]
        else:
            return "Not available"

    def getItemAuthorsByTitle(self, itemTitle):
        if itemID in list(self.items_df[self.itemID_column]):
            return self.items_df['authors'][self.items_df[self.itemName_column] == itemTitle].iloc[0]
        else:
            return "Not available"

    def getItemAuthors(self, itemID):
        if itemID in list(self.items_df[self.itemID_column]):
            return self.items_df['authors'][self.items_df[self.itemID_column] == itemID].iloc[0]
        else:
            return "Not available"

    def getItemImage_URL(self, itemID):
        if itemID in list(self.items_df[self.itemID_column]):
            return self.items_df['image_url'][self.items_df[self.itemID_column] == itemID].iloc[0]
        else:
            return "Not available"
