from flask import Flask, request
from flask_testing import TestCase
from api_copiloto.main import *
from werkzeug.datastructures import ImmutableMultiDict


        
class MyTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    # def test_Get_values(self):
    #     with self.app.test_request_context():
    #         checkbox_names_var = ['var1', 'var2', 'var3']
    #         form_data = {
    #             '1': 'value1',
    #             '2': '',
    #             '3': 'value3'
    #         }
    #         expected_result = {'var1': 'value1', 'var3': 'value3'}
    #         with app.test_client() as client:
    #             response = client.post('/', data=form_data)
    #         result = Get_values(checkbox_names_var)
            # self.assertEqual(result, expected_result)

    def test_Get_values(self):
        with self.app.test_request_context():
            checkbox_names_var = ['var1', 'var2', 'var3']
            form_data = ImmutableMultiDict([('input_1', 'value1'), ('input_2', ''), ('input_3', 'value3')])
            expected_result = {'var1': 'value1', 'var3': 'value3'}
            request = self.app.test_request_context('/',
                                                    method='POST',
                                                    data=form_data)
            breakpoint()
            print(request)
            request.form = form_data
            self.app.preprocess_request()
            result = Get_values(checkbox_names_var)
            self.assertEqual(result, expected_result)