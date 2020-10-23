# FLASK BOOK RECOMMENDER APPLICATION 

Find more info about this app and see it running [here](https://alexnim.com/coding-projects-book-rec-app.html).

Here contains code for a book recommender application built in Flask. This will include the following features:
- selecting book titles for the recommender system
- select the number of recommendations to retrieve
- shuffle results
- results shown with image and link to google search for more info

# Prerequisites 
The following skills and methods were used:
- Familiarity with recommender systems
- Python, SQL and Flask
- HTML, CSS, JavaScript and Jinja
- Google BigQuery (SQL database)

# Data
The raw data for this project has been included in the data folder, however, the source location can be found [here](https://github.com/zygmuntz/goodbooks-10k).

# Files and File Structure Details
- data/ : this contains the base data used to build the similarity matrix 
- resources/ : this contains all the classes and functions used in the application
- static/ : this contains all the CSS and JavaScript code required to render the frontend. 
- templates/ : this contains the frontend HTML

The following files were written for the purpose of deploying the API on Heroku's server. 
- requirements.txt : this contains all the python libraries that need to be installed in order to run the app
- runtime.txt : this tells Heroku the version of Python you are using
- Procfile : this will give instructions to Heroku to run the app using gunicorn

# Helpful Resources
- [Recommender Systems blog post](https://alexnim.com/coding-projects-book-recommenders.html)
- [Pandas GBQ Documentation](https://pandas-gbq.readthedocs.io/en/latest/)
- [Jinja Documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/#expressions)
- [Getting started with Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Comprehensive Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

