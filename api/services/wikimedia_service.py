import requests

from api.services import date_service

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def get_article_page_views_between(article_name, date_range):
    start_date = date_range['start']
    end_date = date_range['end']

    response = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_name}/daily/{start_date.strftime('%Y%m%d')}/{end_date.strftime('%Y%m%d')}", headers=headers)

    data = response.json().get('items') if response.status_code == 200 else None

    return { 'response': response, 'data': data }

def get_aggregated_article_page_views_between(article_name, date_range):
    fetched = get_article_page_views_between(article_name, date_range)

    if fetched['response'].status_code != 200:
        return {'response': fetched['response'], 'data': None}
    
    data = {}
    for item in fetched['data']:
        if item['article'] not in data:
            data[item['article']] = 0
        data[item['article']] += item['views']

    return { 'response': fetched['response'], 'data': data }

def get_top_pageviews_for_month(date):
    yyyy_mm = date.strftime('%Y/%m')
    response = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikisource/all-access/{yyyy_mm}/all-days", headers=headers)
    data = response.json().get('items') if response.status_code == 200 else None
    return { 'response': response, 'data': data }

def make_multiple_top_pageview_calls(date_range):
    start_date = date_range['start']
    end_date = date_range['end']

    aggregated_response = {}
    # Iterate over the single day responses that wikimedia provides, and aggregate the article/viewership data into a dict
    # This either adds a new key value pair (article: viewership) or adds the viewership from another day to the existing value of an article
    for single_date in date_service.daterange(start_date, end_date):
        yyyy_mm_dd = single_date.strftime('%Y/%m/%d')
        day_result = requests.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yyyy_mm_dd}", headers=headers)
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
