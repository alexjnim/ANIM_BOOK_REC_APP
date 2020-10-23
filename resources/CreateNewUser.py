import pandas as pd


def create_new_user(selected_items, items):
    selected_ratings = []

    for i in range(0, len(selected_items)):
        selected_items[i] = int(selected_items[i])

    mockUserID = 0
    max_rating = 5
    itemID_column = 'book_id'
    userID_column = 'user_id'
    ratings_column = 'rating'
    itemName_column = 'title'
    rating_scale_min = 1
    rating_scale_max = 5

    new_rows = {userID_column:[], itemID_column:[], ratings_column:[]}
    if selected_ratings or len(selected_ratings) != 0:
        for num, values in enumerate(zip(selected_items, selected_ratings)):
            new_rows[userID_column].append(mockUserID)
            new_rows[itemID_column].append(values[0])
            new_rows[ratings_column].append(values[1])
    else:
        for values in enumerate(selected_items):
            new_rows[userID_column].append(mockUserID)
            new_rows[itemID_column].append(values[1])
            new_rows[ratings_column].append(max_rating)

    new_rows = pd.DataFrame(new_rows)

    new_rows = pd.merge(new_rows, items[[itemID_column, itemName_column]], how='left', on=[itemID_column])
    return new_rows
