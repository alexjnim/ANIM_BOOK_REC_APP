from resources.RunDataLoader import run_data_loader
from surprise import KNNBasic

import numpy as np
import pickle
import pandas as pd

ml = run_data_loader()
no_ratings = len(ml.ratings_df)
no_ratings = 5000000

print('Number of ratings:'+str(no_ratings))
data = ml.loadData(no_ratings)
trainSet = data.build_full_trainset()

sim_options = {'name': 'cosine',
                       'user_based': False
                       }
model = KNNBasic(sim_options=sim_options)
model.fit(trainSet)
similarity_matrix = model.compute_similarities()


# mlPath = 'data/ml.pkl'
# with open(mlPath, 'wb') as file:
#     pickle.dump(ml, file)

np.save('data/similarity_matrix', similarity_matrix)

trainSetPath = 'data/trainSet.pkl'
with open(trainSetPath, 'wb') as file:
    pickle.dump(trainSet, file)
