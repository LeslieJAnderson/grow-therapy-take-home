from pathlib import Path
import pytest
import vcr

from routes import app
from tests.helpers.response_assertions import assert_data

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config['TESTING'] = True

    with app.app_context():
        # do any setup here
        yield app.test_client()  # tests run here
        # do any teardown here

def test_index(client):
    response = client.get('/', content_type='html/text')

    print(response.data) # Only prints to screen if assertion fails
    assert response.status_code == 200

def test_404(client):
    with vcr.use_cassette('tests/cassettes/404/page-doesnt-exist/cassette.yaml'):
        response = client.get('/404/page-doesnt-exist', content_type='html/text')

    print(response.data)
    assert response.status_code == 404

def test_pageviews_top_articles_week_of_200(client):
    with vcr.use_cassette('tests/cassettes/pageviews/top-articles/week-of/20231001/cassette.yaml'):
        response = client.get('/pageviews/top-articles/week-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/top-articles/week-of/20231001/', response)
    assert response.status_code == 200

def test_pageviews_top_articles_week_of_500(client):
    with vcr.use_cassette('tests/cassettes/pageviews/top-articles/week-of/20231001/cassette-(wikimedia-failure).yaml'):
        response = client.get('/pageviews/top-articles/week-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/top-articles/week-of/20231001/(wikimedia-failure)', response)
    assert response.status_code == 500

def test_pageviews_top_articles_week_of_400(client):
    with vcr.use_cassette('tests/cassettes/pageviews/top-articles/week-of/19999999/cassette.yaml'):
        response = client.get('/pageviews/top-articles/week-of/19999999', content_type='html/text')

    assert_data('tests/expected/pageviews/top-articles/week-of/19999999/', response)
    assert response.status_code == 400

def test_pageviews_top_articles_month_of_200(client):
    with vcr.use_cassette('tests/cassettes/pageviews/top-articles/month-of/20231001/cassette.yaml'):
        response = client.get('/pageviews/top-articles/month-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/top-articles/month-of/20231001/', response)
    assert response.status_code == 200

def test_pageviews_top_articles_month_of_400(client):
    with vcr.use_cassette('tests/cassettes/pageviews/top-articles/month-of/19999999/cassette.yaml'):
        response = client.get('/pageviews/top-articles/month-of/19999999', content_type='html/text')

    assert_data('tests/expected/pageviews/top-articles/month-of/19999999/', response)
    assert response.status_code == 400

def test_pageviews_for_week_of_200(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/week-of/20231001/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/week-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/week-of/20231001/', response)
    assert response.status_code == 200

def test_pageviews_for_week_of_500(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/week-of/20231001/cassette-(wikimedia-failure).yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/week-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/week-of/20231001/(wikimedia-failure)', response)
    assert response.status_code == 500

def test_pageviews_for_week_of_400(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/week-of/19999999/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/week-of/19999999', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/week-of/19999999/', response)
    assert response.status_code == 400

def test_pageviews_for_month_of_200(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/month-of/20231001/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/month-of/20231001', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/month-of/20231001/', response)
    assert response.status_code == 200

def test_pageviews_for_month_of_400(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/month-of/19999999/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/month-of/19999999', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/month-of/19999999/', response)
    assert response.status_code == 400

def test_pageviews_for_month_of_best_day_200(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/month-of/20231001/best-day/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/month-of/20231001/best-day', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/month-of/20231001/best-day', response)
    assert response.status_code == 200

def test_pageviews_for_month_of_best_day_400(client):
    with vcr.use_cassette('tests/cassettes/pageviews/for/Albert_Einstein/month-of/19999999/best-day/cassette.yaml'):
        response = client.get('/pageviews/for/Albert_Einstein/month-of/19999999/best-day', content_type='html/text')

    assert_data('tests/expected/pageviews/for/Albert_Einstein/month-of/19999999/best-day', response)
    assert response.status_code == 400
