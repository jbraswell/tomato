import csv
import json
import io
from django.test import TransactionTestCase
from django.urls import reverse
from xml.etree import ElementTree as ET
from .views import meeting_field_map


class GetSearchResultsTests(TransactionTestCase):
    fixtures = ['testdata']

    def test_get_search_results_json(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        response = json.loads(response.content)
        self.assertEqual(len(response), 10)
        meeting = response[0]
        for key in meeting.keys():
            self.assertIn(key, meeting_field_map.keys())

    def test_get_search_results_xml(self):
        url = reverse('semantic-query', kwargs={'format': 'xml'})
        url += '?switcher=GetSearchResults'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        response = ET.fromstring(response.content)
        self.assertEqual(len(response.findall('./row')), 10)

    def test_get_search_results_csv(self):
        url = reverse('semantic-query', kwargs={'format': 'csv'})
        url += '?switcher=GetSearchResults'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        s = io.StringIO(response.content.decode(response.charset))
        try:
            reader = csv.DictReader(s)
            for field_name in reader.fieldnames:
                self.assertIn(field_name, meeting_field_map.keys())
            num_rows = 0
            for row in reader:
                num_rows += 1
            self.assertEqual(num_rows, 10)
        finally:
            s.close()

    def test_get_search_results_with_formats(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults&get_used_formats=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue('formats' in response)
        self.assertTrue('meetings' in response)
        self.assertEqual(len(response['meetings']), 10)
        for meeting in response['meetings']:
            for meeting_format in meeting['formats'].split(','):
                if meeting_format == '':
                    continue
                for format in response['formats']:
                    if format['key_string'] == meeting_format:
                        break
                else:
                    self.fail('Meeting format {} not found'.format(meeting_format))
        for format in response['formats']:
            for meeting in response['meetings']:
                found = False
                for meeting_format in meeting['formats'].split(','):
                    if meeting_format == '':
                        continue
                    if format['key_string'] == meeting_format:
                        found = True
                        break
                if found:
                    break
            else:
                self.fail('Format {} not found with a meeting'.format(format))

    def test_get_search_results_formats_only_with_formats_not_specified(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults&get_formats_only=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(isinstance(response, list))

    def test_get_search_results_with_formats_formats_only(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults&get_used_formats=1&get_formats_only=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue('formats' in response)
        self.assertFalse('meetings' in response)
        self.assertTrue(len(response['formats']), 12)

    def test_get_search_results_weekdays_single(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults&weekdays=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(len(response) > 1)
        for meeting in response:
            self.assertEqual(meeting['weekday_tinyint'], '2')

    def test_get_search_results_weekdays_multiple(self):
        url = reverse('semantic-query', kwargs={'format': 'json'})
        url += '?switcher=GetSearchResults&weekdays[]=1&weekdays[]=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(len(response) > 1)
        found_one = False
        found_two = False
        for meeting in response:
            if meeting['weekday_tinyint'] == '1':
                found_one = True
            elif meeting['weekday_tinyint'] == '2':
                found_two = True
            else:
                self.fail('Unexpected weekday found')
        self.assertTrue(found_one)
        self.assertTrue(found_two)
