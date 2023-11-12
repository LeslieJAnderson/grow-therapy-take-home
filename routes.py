from flask import Flask
from flask_selfdoc import Autodoc

from api.services import date_service, wikimedia_service
from api.services.validation_service import validate_and_convert_to_week_range, validate_and_convert_to_month_range

app = Flask(__name__)
auto = Autodoc(app)

@app.route("/")
def documentation():
    return auto.html()

@app.route('/pageviews/top-articles/week-of/<string:date>', methods=['GET'])
@auto.doc()
@validate_and_convert_to_week_range('date')
def pageviews_top_week_of(date: str):
    """
    Returns a list of top wikipedia articles, from each day in the week of the provided date, sorted by aggregate views.
    - date: YYYYMMDD (example: '20231110')
    """
    fetched = wikimedia_service.make_multiple_top_pageview_calls(date['week_range'])

    if (fetched['error']):
        return fetched, 500

    return {
        'meta': {'date': date},
        'data': wikimedia_service.sort_and_rank_results(fetched['data'])
    }

@app.route('/pageviews/top-articles/month-of/<string:date>', methods=['GET'])
@auto.doc()
@validate_and_convert_to_month_range('date')
def pageviews_top_month_of(date: str):
    """
    Returns a list of top wikipedia articles, from each day in the month of the provided date, sorted by aggregate views.
    - date: YYYYMMDD (example: '20231110')
    """

    fetched = wikimedia_service.get_top_pageviews_for_month(date['month_range']['start'])
    
    if fetched['response'].status_code != 200:
        return {"error": True, "response": fetched['response'].json()}, 500

    return {
        'meta': {'date': date},
        'data': fetched['data'][0]['articles']
    }

@app.route('/pageviews/for/<string:article_name>/week-of/<string:date>', methods=['GET'])
@auto.doc()
@validate_and_convert_to_week_range('date')
def pageviews_for_week_of(article_name: str, date: str):
    """
    Returns the number of views for an article, from each day in the week of the provided date.
    - date: YYYYMMDD (example: '20231110')
    """

    fetched = wikimedia_service.get_aggregated_article_page_views_between(article_name, date['week_range'])

    if fetched['response'].status_code != 200:
        return {"error": True, "response": fetched['response'].json()}, 500

    return {
        'meta': {'date': date},
        'data': fetched['data']
    }

@app.route('/pageviews/for/<string:article_name>/month-of/<string:date>', methods=['GET'])
@auto.doc()
@validate_and_convert_to_month_range('date')
def pageviews_for_month_of(article_name: str, date: str):
    """
    Returns the number of views for an article, from each day in the month of the provided date.
    - date: YYYYMMDD (example: '20231110')
    """

    fetched = wikimedia_service.get_aggregated_article_page_views_between(article_name, date['month_range'])

    if fetched['response'].status_code != 200:
        return {"error": True, "response": fetched['response'].json()}, 500

    return {
        'meta': {'date': date},
        'data': fetched['data']
    }

# Retrieve the day of the month where an article got the most views
@app.route('/pageviews/for/<string:article_name>/month-of/<string:date>/best-day', methods=['GET'])
@auto.doc()
@validate_and_convert_to_month_range('date')
def pageviews_for_month_of_best_day(article_name: str, date: str):
    """
    Returns the day where an article had the most views in the month of the provided date.
    - date: YYYYMMDD (example: '20231110')
    """

    fetched = wikimedia_service.get_article_page_views_between(article_name, date['month_range'])

    if fetched['response'].status_code != 200:
        return {"error": True, "response": fetched['response'].json()}, 500
    
    most_viewed = {"timestamp": "", "views": 0}
    for item in fetched['data']:
        if (item["views"] > most_viewed["views"]):
            most_viewed = item

    return {
        "meta": {"date": most_viewed["timestamp"]},
        "data": {"article": article_name, "views": most_viewed["views"]}
    }

# Generic but hopefully helpful catch-all for bad routes
@app.errorhandler(404)
def handle_404(e):
    return f"""
        Whoops, this isn't an endpoint. Check out your options:
        {auto.html()}
    """, 404
