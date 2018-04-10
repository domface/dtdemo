from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from .serializers import *
import requests
from bs4 import BeautifulSoup
from datetime import datetime

client = Client()


class LookUpTestCase(TestCase):

    def setUp(self):
        self.payload = {
            "query_string": "https://www.amazon.com/Smart-For-Mobile-WhatsChat/dp/B012IU3HL8/"
        }
        session = requests.Session()
        session.trust_env = False
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
            'From': 'foo@domain.com'
        }
        page = session.get(self.payload["query_string"], headers=headers)
        self.soup = soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')

    def test_create_query(self):
        response = client.post(
            reverse('query'),
            data=json.dumps(self.payload),
            content_type='application/json'

        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session(self):
        page = LookUpSerializer.create_session(self.payload["query_string"])

        self.assertEqual(page.status_code, 200)


    def test_get_change_log(self):
        change_log = LookUpSerializer.get_change_log(self.soup)

        self.assertEqual([], change_log)

    def test_get_title(self):
        title = LookUpSerializer.get_title(self.soup)

        self.assertEqual('WhatsChat', title)

    def test_get_version(self):
        version = LookUpSerializer.get_version(self.soup)

        self.assertEqual('0.1', version)

    def test_get_version(self):
        original_release_date, latest_release_date = LookUpSerializer.get_release_dates(self.soup)

        self.assertEqual(datetime(2015, 7, 25, 0, 0), original_release_date)
        self.assertEqual(datetime(2015, 7, 25, 0, 0), latest_release_date)
