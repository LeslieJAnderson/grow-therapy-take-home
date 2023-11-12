# Disclaimers
    - I have not worked in Python in 5+ years, but as Grow Therapy is a Python shop I thought it made sense to solve the problem in Python. I'm sure there are places where things aren't quite "the Python way"--I hope you'll indulge me these oversights
    - Test coverage is at 98%. Mocking calls would have taken me to 100%, but it proved difficult. I figure in the real world, you sometimes have to trade off coverage for expediency. The bases are pretty well covered, so I'm comfortable making this trade off
    - A snapshot library would probably be preferable to my `assert_data` method, but for an interview prompt this gets the job done

# Assumptions Made
    - The request for data "for a week or a month" means a calendar week or month, not an arbitrary 7 or 28-31 days
    - Sunday is the first day of the week
    - There should be no limit to the number of articles returned for for the "Top Articles" endpoint

# Focus on future-proofing and flexibility
    - If my assumption about what "for a week or a month" means is incorrect, `make_multiple_date_calls` is flexible enough to use with any date range; either tweaking my existing endpoints to accept a `start_date` and an `end_date`, or creating a new endpoint that accepts those parameters, should take minimal effort

# Installation & Setup
    - Install venv in project after you clone repo with `python3 -m venv .venv`
    - Get into venv with `. .venv/bin/activate`
    - While in venv:
        - Save installed dependencies with `pip freeze > requirements.txt`
        - Install dependencies with `pip install -r requirements.txt`    
        - Start the app with `flask --app routes.py run --debug`
        - Run tests from venv with `pytest`
        - Get test coverage with missing lines using `pytest --cov-report term-missing --cov=. tests/`

# Documentation
    - Documented via autodoc
    - To see documentation, visit http://127.0.0.1:5000/


# Example endpoints:
    - http://127.0.0.1:5000/pageviews/top-articles/week-of/20151010
    - http://127.0.0.1:5000/pageviews/top-articles/month-of/20151010
    - http://127.0.0.1:5000/pageviews/for/List_of_craters_on_Mars:_O–Z/week-of/20231002
    - http://127.0.0.1:5000/pageviews/for/Lisa_Frank/month-of/20231002
    - http://127.0.0.1:5000//pageviews/for/Asimina/month-of/20231030/best-day

TODO:
https://flask.palletsprojects.com/en/3.0.x/testing/
https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/
