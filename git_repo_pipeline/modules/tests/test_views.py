from django.test import TestCase
from ddt import ddt, data

import json


@ddt
class SimpleTest(TestCase):
    """
    Tests that the /main/ endpoint returns the correct response
    """
    fixtures = ['test_data_commit.json',
                'test_data_repository.json', 'test_data_user.json']

    def format_input_pipeline(self, owner, repository):
        """
        Formats the request body for the post request used by all test methods
        """
        return {
            "owner": owner,
            "repository": repository
        }

    def format_input(self, owner, repository, start_date, end_date=None):
        """
        Formats the request body for the post request used by all test methods
        """
        return {
            "owner": owner,
            "repository": repository,
            "start_date": start_date,
            "end_date": end_date
        }

    @data(('apache', 'hadoop'))
    def test_store_valid_input(self, values):
        """
        Tests valid inputs for the /main/ endpoint
        """
        p = self.format_input_pipeline(values[0], values[1])
        response = self.client.post(
            "/store/", p, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @data(('apache', ''))
    def test_store_invalid_input(self, values):
        """
        Tests empty string for the /main/ endpoint
        """
        p = self.format_input_pipeline(values[0], values[1])
        response = self.client.post(
            "/store/", p, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @data(('/authors/top/', 'apache', 'hadoop', None, None), ('/authors/top/', 'apache', '', '2020-01-12', '2020-01-13'),
          ('/authors/contribution/', 'apache', 'hadoop', None, None), ('/heatmap/', 'apache', 'hadoop', None, None))
    def test_endpoints_invalid_input(self, values):
        """
        Tests invalid inputs for the 3 endpoints: /authors/top/, /authors/contribution/
        and /heatmap. Ensures that
        first result returned has the highest number of commits
        """
        p = self.format_input(values[1], values[2], values[3], values[4])
        response = self.client.post(
            values[0], p, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @data(('apache', 'hadoop', '2020-01-10', None), ('apache', 'hadoop', '2020-01-12', '2020-01-13'))
    def test_top_authors_valid_input(self, values):
        """
        Tests valid inputs for the /authors/top/ endpoint. Ensures that
        first result returned has the highest number of commits
        """
        p = self.format_input(values[0], values[1], values[2], values[3])
        response = self.client.post(
            "/authors/top/", p, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)

        self.assertTrue(len(response_json) <= 3)
        self.assertTrue(response_json[0]['commits']
                        >= response_json[1]['commits'])
        if len(response_json) == 3:
            self.assertTrue(
                response_json[1]['commits'] >= response_json[2]['commits'])

    @data(('apache', 'hadoop', '2020-01-10', None), ('apache', 'hadoop', '2020-01-12', '2020-01-13'))
    def test_most_contribution_valid_input(self, values):
        """
        Tests valid inputs for the /authors/contribution/ endpoint. Ensures that
        first result returned has the highest number of commits
        """
        p = self.format_input(values[0], values[1], values[2], values[3])
        response = self.client.post(
            "/authors/contribution/", p, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)

        self.assertTrue(type(response_json) == dict)
        self.assertTrue(set(response_json.keys()) == set(
            ['id', 'username', 'name', 'email', 'contribution_window_days']))

    @data(('apache', 'hadoop', '2020-01-08', None))
    def test_heatmap_valid_input(self, values):
        """
        Tests valid inputs for the /heatmap/ endpoint. Ensures there
        are only 8 rows (8 time frames), and that each row has no more than
        8 columns (1 column is the time, and the next 7 columns are the days)
        """
        p = self.format_input(values[0], values[1], values[2], values[3])
        response = self.client.post(
            "/heatmap/", p, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)

        self.assertTrue(type(response_json) == list)
        self.assertTrue(len(response_json) <= 8)
        if len(response_json) > 0:
            self.assertTrue(len(response_json[0]) <= 8)
