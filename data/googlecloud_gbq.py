
from google.oauth2 import service_account
import pandas_gbq

import numpy as np
import pickle
import pandas as pd
# -

# # LOAD 500000 array into GBQ

# +
sm = np.load('similarity_matrix.npy')

n, m = sm.shape

from random import choice
from string import ascii_lowercase, digits

chars = ascii_lowercase
lst = [''.join(choice(chars) for _ in range(15)) for _ in range(m)]

sm_df = pd.DataFrame(data=sm, columns=lst)

# +
sm_df_row = sm_df

sm_df_row['row'] = list(range(n))
sm_df_row

# +
from google.oauth2 import service_account
import pandas_gbq

credentials = service_account.Credentials.from_service_account_file(
    'admin-book-rec-app-2-73ea95bae98e.json',)

pandas_gbq.to_gbq(sm_df_row, 'data.similarity_matrix_w_rownumber', project_id="book-rec-app-2", if_exists = 'replace', credentials=credentials)
# -

# # pull data from google gbq

# +
l = [1,2,3]

placeholders= ', '.join(str(number) for number in l)
query= 'SELECT * FROM data.similarity_matrix_w_rownumber WHERE row IN (%s)' % placeholders
query

# +
credentials = service_account.Credentials.from_service_account_file(
    'viewer-book-rec-app-2-f4ff71f92a3e.json',)

sql = 'SELECT * FROM data.similarity_matrix_w_rownumber WHERE row in (1,2)'

df = pandas_gbq.read_gbq(query, project_id="book-rec-app-2", credentials=credentials)
# -

df

# # extra test

df.to_numpy()

d = [21,22,23,24,25,26,27]
for i, m in enumerate(d):
    print(i)
    print(m)

# +
kNeighbours = [(72, 5.0), (2, 5.0), (892, 5.0)]

innerbookIDs = []
for innerbookID, rating in kNeighbours:
    innerbookIDs.append(innerbookID)

placeholders= ', '.join(str(innerbookID) for innerbookID in innerbookIDs)
query= 'SELECT * FROM data.similarity_matrix_w_rownumber WHERE row IN (%s)' % placeholders

credentials = service_account.Credentials.from_service_account_file(
    'book-rec-project-fba85c625dd8.json',)

df = pandas_gbq.read_gbq(query, project_id="book-rec-project", credentials=credentials)
df = df.drop(columns=['row'])
similarity_rows = df.to_numpy()

# +
from collections import defaultdict

candidates = defaultdict(float)
appear = defaultdict(float)

for similarity_row in similarity_rows:
    for innerID, similarityScore in enumerate(similarity_row):
        candidates[innerID] += similarityScore * (rating / 5.0)
        appear[innerID] += 1.0
# -

    for itemID, rating in kNeighbours:
        similarity_row = similarity_matrix[itemID]
        print(itemID)
        print(len(similarity_row))
        print(similarity_row)
        for innerID, similarityScore in enumerate(similarity_row):
            candidates[innerID] += similarityScore * (rating / 5.0)
            appear[innerID] += 1.0

a = [1,2,3,4]
b = [1,3,3,4]
a == b

similarity_rows[[1,2]]
