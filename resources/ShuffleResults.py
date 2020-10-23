import pandas
import pickle
import random
import re
from operator import itemgetter
from random import randrange
from resources.RunDataLoader import run_data_loader

def shuffle_recs(request):

    itemIDs = request.form['itemIDs']
    previous_itemIDs = request.form['recommended_itemIDs']
    no_recs = int(request.form['no_recs'])
    ml = run_data_loader()

    trainSetPath = 'data/trainSet.pkl'
    with open(trainSetPath, 'rb') as file:
        trainSet = pickle.load(file)

    itemIDs = itemIDs[1:-1].replace(" ", "").split(",")
    itemIDs = list(map(int, itemIDs))
    previous_itemIDs = previous_itemIDs[1:-1].replace(" ", "").split(",")
    previous_itemIDs = list(map(int, previous_itemIDs))

    print(previous_itemIDs)

    random_number = randrange(100)
    random.Random(random_number).shuffle(itemIDs)
    candidates = {}
    maxval = 10
    for i in itemIDs:
        candidates[i] = maxval

    results = []
    recommended_itemIDs = []
    pos = 0
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if itemID not in previous_itemIDs:
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
    print(recommended_itemIDs)
    return results, itemIDs, no_recs, recommended_itemIDs
