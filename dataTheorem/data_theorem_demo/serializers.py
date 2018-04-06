from rest_framework import serializers
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class LookUpSerializer(serializers.Serializer):

    query_string = serializers.CharField(max_length=500)
    app_name = serializers.CharField(max_length=100, required=False)
    app_version = serializers.CharField(max_length=20, required=False)
    change_log = serializers.ListField(required=False)
    original_release_date = serializers.DateTimeField(required=False)
    latest_release_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        page = self.create_session(url_string=validated_data['query_string'])

        # cache the parsed HTML
        soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
        app_name = self.get_title(soup)
        app_version = self.get_version(soup)
        change_log = self.get_change_log(soup)
        original_release_date, latest_release_date = self.get_release_dates(soup)

        return {
            'query_string': validated_data['query_string'],
            'app_name': app_name,
            'app_version': app_version,
            'change_log': change_log,
            'original_release_date': original_release_date,
            'latest_release_date': latest_release_date
        }

    @classmethod
    def create_session(self, url_string):
        # Create a Session and pull HTML Data
        session = requests.Session()
        session.trust_env = False
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
            'From': 'foo@domain.com'
        }
        page = session.get(url_string, headers=headers)

        # Return Error
        if page.status_code == 200:
            return page
        else:
            return

    @classmethod
    def get_change_log(self, soup):
        # Find Change Log visa vie Latest Updates tag
        updates = soup.find_all('div', class_="bucket")
        updates_tag = None
        # Find div index where updates reside
        for i in range(len(updates)):
            return_list = updates[i].find_all(text="Latest updates")
            if len(return_list) > 0:
                updates_tag = updates[i]
                break

        change_log = []
        if updates_tag:
            for item in updates_tag.find_all('li'):
                change_log.append(item.text)

        return change_log

    @classmethod
    def get_title(self, soup):
        title = soup.find_all(id="btAsinTitle")[0].text
        return title

    @classmethod
    def get_version(self, soup):
        technical_details = soup.find_all(id='mas-technical-details')[0]

        tech_detes_parsed = technical_details.find_all('div', class_="a-section")

        version_tag = None

        for i in range(len(tech_detes_parsed)):
            return_list = tech_detes_parsed[i].find_all(text="Version:")
            if len(return_list) > 0:
                version_tag = tech_detes_parsed[i]
                break
        if version_tag:
            version = version_tag.text.split('Version:')[1][1:]
        return version

    @classmethod
    def get_release_dates(self, soup):
        # Get Release Dates
        product_details = soup.find_all(id="productDetailsTable")[0]
        content = product_details.find_all('div', class_="content")[0]

        for item in content.find_all('li'):
            if len(item.find_all(text="Original Release Date:")) > 0:
                original_release_date = item.text.split("Original Release Date:")[1][1:]
            elif len(item.find_all(text=" Latest Developer Update:")) > 0:
                latest_release_date = item.text.split(" Latest Developer Update:")[1][1:-1]

        return datetime.strptime(original_release_date, '%B %d, %Y'), datetime.strptime(latest_release_date, '%B %d, %Y')
