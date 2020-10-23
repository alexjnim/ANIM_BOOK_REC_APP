import pandas as pd


def get_request_variables(request, items):
    selected_titles_ids = []
    selected_titles = []
    not_titles = []
    for i in range(15):
        if request.form['title'+str(i+1)]:
            title = request.form['title'+str(i+1)]
            if len(items[items['title'] == title]):
                # select title with the author
                author = list(items[items['title'] == title]['authors'].iloc[0].split(","))[0]
                book_id = items[items['title'] == title]['book_id'].iloc[0]
                title_author = title+' by '+author
                if title_author not in selected_titles:
                    selected_titles.append(title_author)
                    selected_titles_ids.append(book_id)
            else:
                not_titles.append(title)

    no_recs = int(request.form['no_recs'])

    return selected_titles, selected_titles_ids, not_titles, no_recs
