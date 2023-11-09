from flask import Flask
from flask_selfdoc import Autodoc
import requests
import json
import datetime
import calendar

def daterange(start_date, end_date):
    print(start_date)
    print(end_date)
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def calc_first_and_last_day_of_week(date):
    one_week = datetime.timedelta(days=6)
    # turns day into weekly position; sunday into 0, monday into 1, etc.
    day_idx = (date.weekday() + 1) % 7  
    sunday = date - datetime.timedelta(days=day_idx)
    date = sunday
    date += one_week
    return [sunday, date]

def calc_first_and_last_day_of_month(date):
    first_and_last_day = calendar.monthrange(2015, 10)
    first_day = datetime.datetime(int(date.strftime('%Y')), int(date.strftime('%m')), first_and_last_day[0])
    last_day = datetime.datetime(int(date.strftime('%Y')), int(date.strftime('%m')), first_and_last_day[1])
    return [first_day, last_day]

def make_multiple_date_calls(start_date, end_date):
    aggregated_response = {}
    # Iterate over the single day responses that wikimedia provides, and aggregate the article/viewership data into a dict
    # This either adds a new key value pair (article: viewership) or adds the viewership from another day to the existing value of an article
    for single_date in daterange(start_date, end_date):
        day_result = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{single_date.strftime('%Y/%m/%d')}", headers=headers)
        r = day_result.json().get('items')
        if day_result.status_code == 200:
            for item in r[0]["articles"]:
                if item["article"] in aggregated_response:
                    aggregated_response[item["article"]] = aggregated_response[item["article"]] + item["views"]
                else:
                    aggregated_response[item["article"]] = item["views"]
        else:
            return {"error": True, "response": day_result.json()}
    return {"error": False, "data": aggregated_response}

def sort_and_rank_results(aggregated_response):
    # Turn the dict into a list of tuples (article, viewership)
    unsorted_list = list(aggregated_response.items())     
    # Sort in descending order based on the second value (viewership) in the tuple
    sorted_list = sorted(unsorted_list, key=lambda tup: tup[1], reverse=True)

    # Iterate over the list, adding article, viewership, and a new key of 'rank' as a dict to a new list
    final_response = []
    i = 0
    for value in sorted_list:
        i += 1
        final_response.append({'article': value[0], 'rank': i, 'views': value[1]})
    return final_response

def simplify_response_of_time_range_calls(response):
    aggregated_response = {}
    response_items = response.get('items')
    for item in response_items:
        if item["article"] in aggregated_response:
            aggregated_response[item["article"]] = aggregated_response[item["article"]] + item["views"]
        else:
            aggregated_response[item["article"]] = item["views"]
    return aggregated_response

def validate_and_format_date(date):
    try:
        date_format = '%Y%m%d'
        thing = datetime.datetime.strptime(date, date_format)
        return {"valid": True, "data": thing}
    except ValueError:
        return {"valid": False, "message": "Enter a valid date in the format of YYYYMMDD"}

app = Flask(__name__)
auto = Autodoc(app)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

@app.route("/")
def documentation():
    return auto.html()

# Retrieve a list of the most viewed articles for a week or a month
@app.route('/pageviews/top/<string:time_period>/<string:start_date>', methods=['GET'])
@auto.doc()
def top_pageviews(start_date: str, time_period: str):
    formatted_start_date = validate_and_format_date(start_date)
    if not formatted_start_date["valid"]:
        return formatted_start_date
    formatted_start_date = formatted_start_date["data"]

    dates = []
    aggregated_response = {}
    data = {}
    if (time_period.lower() == "week-of"):
        dates = calc_first_and_last_day_of_week(formatted_start_date)
        aggregated_response = make_multiple_date_calls(dates[0], dates[1])
        if (aggregated_response["error"]):
            return aggregated_response
        data = sort_and_rank_results(aggregated_response["data"])
        print(data)
    elif (time_period.lower() == "month-of"):
        dates = calc_first_and_last_day_of_month(formatted_start_date)
        month_result = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikisource/all-access/{formatted_start_date.strftime('%Y/%m')}/all-days", headers=headers)
        if not month_result.status_code == 200:
            return {"error": True, "response": month_result.json()}

        month_result_items = month_result.json().get('items')
        data = month_result_items[0]["articles"]
    else:
        return "Use month-of or week-of for time period"

    return {
        'meta': {"start_date": dates[0].strftime('%Y%m%d'), "end_date": dates[1].strftime('%Y%m%d')},
        'data': data
    }

# Retrieve the view count of a specific article for a week or month
@app.route('/pageviews/per-article/<string:article_name>/<string:time_period>/<string:start_date>', methods=['GET'])
@auto.doc()
def pageviews_per_article(article_name: str, start_date: str, time_period: str):
    formatted_start_date = validate_and_format_date(start_date)
    if not formatted_start_date["valid"]:
        return formatted_start_date
    formatted_start_date = formatted_start_date["data"]

    dates = []
    simplified_response = {}
    if (time_period.lower() == "week-of"):
        dates = calc_first_and_last_day_of_week(formatted_start_date)
        response = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_name}/daily/{dates[0].strftime('%Y%m%d')}/{dates[1].strftime('%Y%m%d')}", headers=headers)
    elif (time_period.lower() == "month-of"):
        dates = calc_first_and_last_day_of_month(formatted_start_date)
        response = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_name}/daily/{dates[0].strftime('%Y%m%d')}/{dates[1].strftime('%Y%m%d')}", headers=headers)
        
    else:
        return "pick month or week"

    if not response.status_code == 200:
        return {"error": True, "response": response.json()}
    simplified_response = simplify_response_of_time_range_calls(response.json())

    return {
        'meta': {"start_date": dates[0].strftime('%Y%m%d'), "end_date": dates[1].strftime('%Y%m%d')},
        'data': simplified_response
    }

# Retrieve the daty of the month where an article got the most views
@app.route('/day_of_month_with_most_page_views/<string:article_name>/<string:start_date>', methods=['GET'])
@auto.doc()
def day_of_month_with_most_page_views(article_name: str, start_date: str):
    formatted_start_date = validate_and_format_date(start_date)
    if not formatted_start_date["valid"]:
        return formatted_start_date
    formatted_start_date = formatted_start_date["data"]

    dates = calc_first_and_last_day_of_month(formatted_start_date)
    response = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_name}/daily/{dates[0].strftime('%Y%m%d')}/{dates[1].strftime('%Y%m%d')}", headers=headers)

    if not response.status_code == 200:
        return {"error": True, "response": response.json()}

    response = response.json().get('items')

    most_viewed = {"views": 0}
    for item in response:
        if (item["views"] > most_viewed["views"]):
            most_viewed = item

    simplified_response = {"article": article_name, "views": most_viewed["views"]}
    return {
        "meta": {"date": most_viewed["timestamp"]},
        "data": simplified_response
    }

# Generic but hopefully helpful catch-all for bad routes
@app.errorhandler(404)
def handle_404(e):
    return f"""
        Whoops, this isn't an endpoint. Check out your options:
        {auto.html()}
    """






# These are being deleted:

@app.route('/pageviews/top/between/<string:start_date>/<string:end_date>', methods=['GET'])
def most_viewed(start_date: str, end_date: str):
    # Turn strings in the URL into dates
    date_format = '%Y%m%d'
    s_d_1 = datetime.datetime.strptime(start_date, date_format)
    s_d_2 = datetime.datetime.strptime(end_date, date_format)

    # Return an warning saying the user is requesting too many or too few days to prevent confusion
    delta = (s_d_2 - s_d_1).days
    if delta > 31:
        return "TOo many days, bruh"
    elif delta < 1:
        return "Too few days, bruh"

    aggregated_response = make_multiple_date_calls(s_d_1, s_d_2)
    final_response = sort_and_rank_results(aggregated_response)

    final_response.insert(0, {"start_date": start_date, "end_date": end_date})
    return final_response

@app.route('/pageviews/per-article/<string:article_name>/<string:start_date>/<string:end_date>', methods=['GET'])
def views_by_article(article_name: str, start_date: str, end_date: str):
    # Turn strings in the URL into dates
    date_format = '%Y%m%d'
    formatted_start_date = datetime.datetime.strptime(start_date, date_format)
    formatted_end_date = datetime.datetime.strptime(end_date, date_format)

    # Return an warning saying the user is requesting too many or too few days to prevent confusion
    delta = (formatted_end_date - formatted_start_date).days
    if delta > 31:
        return "Too many days, bruh"
    elif delta < 1:
        return "Too few days, bruh"

    aggregated_response = {}

    day_result = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_name}/daily/{start_date}/{end_date}", headers=headers)
    return day_result.json()


