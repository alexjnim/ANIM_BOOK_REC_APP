# +
from resources.GetRequestVariables import get_request_variables
from resources.CreateNewUser import create_new_user
from resources.CF_cached import item_based_rec_loader_cached_2
from resources.RunDataLoader import run_data_loader
from resources.ShuffleResults import shuffle_recs
#
import pickle
import os
import pandas as pd
from flask import Flask, render_template, request, json

# +
# Initialise the Flask app
app = Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        # Just render the initial form, to get input
        return(render_template('index.html'))

    if request.method == 'POST':

        ml = run_data_loader()
        items = ml.items_df
        selected_titles, selected_titles_ids, not_titles, no_recs = get_request_variables(request, items)
        if len(selected_titles_ids) == 0:
            message = '*please enter some book titles that you like'
            return render_template('index.html', result=message)

        new_rows = create_new_user(selected_titles_ids, items)
        print(new_rows)
        recommendations, itemIDs, recommended_itemIDs = item_based_rec_loader_cached_2(ml, no_recs, new_rows)

        return render_template('results.html', results = recommendations, selected_titles = selected_titles, not_titles = not_titles, itemIDs = itemIDs, recommended_itemIDs = recommended_itemIDs, no_recs = no_recs)

@app.route('/results.html', methods=['POST'])
def shuffle():
    if request.method == 'POST':

        recommendations, itemIDs, no_recs, recommended_itemIDs = shuffle_recs(request)

        selected_titles = request.form['selected_titles']
        not_titles = request.form['not_titles']
        print(selected_titles)
        selected_titles = selected_titles[1:-1].replace(", #", " #").replace("'", "").replace("\"", "").split(",")
        not_titles = not_titles[1:-1].replace("'", "").split(",")


        print(not_titles[0])
        if len(not_titles) == 1 and not_titles[0] == "":
            not_titles = []


        return render_template('results.html', results = recommendations, selected_titles = selected_titles, not_titles = not_titles, itemIDs = itemIDs, recommended_itemIDs = recommended_itemIDs, no_recs = no_recs)
# -

if __name__ == "__main__":
    app.run(host='0.0.0.0')
