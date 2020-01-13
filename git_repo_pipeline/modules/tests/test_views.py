from django.test import TestCase
from ddt import ddt, data

import json


@ddt
class SimpleTest(TestCase):
    """
    Tests that the /main/ endpoint returns the correct response
    """

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

    @data(('apache', 'hadoop', '2019-01-01', '2019-01-05'), ('apache', 'hadoop', '2019-01-01', None))
    def test_details_valid_input(self, values):
        """
        Tests valid inputs for the /main/ endpoint: valid end_date and empty end_date
        """
        p = self.format_input(values[0], values[1], values[2], values[3])
        response = self.client.post(
            "/main/", p, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @data(('apache', 'hadoop', '2019--01', '2019-01-05'), ('', 'hadoop', '2019-01-01', None), ('apache', 'hadoop', '', '2019-01-05'))
    def test_details_invalid_input(self, values):
        """
        Tests invalid inputs for the /main/ endpoint:
        invalid date format, missing repository and owner
        """
        p = self.format_input(values[0], values[1], values[2], values[3])
        response = self.client.post(
            "/main/", p, content_type='application/json')
        self.assertEqual(response.status_code, 400)
