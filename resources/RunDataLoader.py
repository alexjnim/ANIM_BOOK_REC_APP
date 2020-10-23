import pickle
from resources.DataLoader import DataLoader

def run_data_loader():
    items_path = 'data/books.csv'
    ratings_path = 'data/ratings.csv'
    itemID_column = 'book_id'
    userID_column = 'user_id'
    ratings_column = 'rating'
    itemName_column = 'title'
    rating_scale_min = 1
    rating_scale_max = 5

    # Load our data set and compute the user similarity matrix
    model = DataLoader(items_path, ratings_path, userID_column, itemID_column, ratings_column, itemName_column, rating_scale_min, rating_scale_max)

    return model
