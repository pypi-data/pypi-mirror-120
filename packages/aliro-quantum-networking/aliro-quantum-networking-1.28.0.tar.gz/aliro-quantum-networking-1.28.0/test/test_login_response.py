# coding: utf-8

"""
    Aliro Q.Network

    This is an api for the Aliro Q.Network  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aliro_quantum_networking
from aliro_quantum_networking.models.login_response import LoginResponse  # noqa: E501
from aliro_quantum_networking.rest import ApiException

class TestLoginResponse(unittest.TestCase):
    """LoginResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test LoginResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum_networking.models.login_response.LoginResponse()  # noqa: E501
        if include_optional :
            return LoginResponse(
                data = aliro_quantum_networking.models.user_info.UserInfo(
                    email = '0', 
                    first_name = '0', 
                    last_name = '0', 
                    phone = '0', 
                    roles = [
                        '0'
                        ], 
                    token = '0', )
            )
        else :
            return LoginResponse(
        )

    def testLoginResponse(self):
        """Test LoginResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
