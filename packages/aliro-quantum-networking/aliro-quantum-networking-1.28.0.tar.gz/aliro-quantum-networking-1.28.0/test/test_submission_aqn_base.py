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
from aliro_quantum_networking.models.submission_aqn_base import SubmissionAqnBase  # noqa: E501
from aliro_quantum_networking.rest import ApiException

class TestSubmissionAqnBase(unittest.TestCase):
    """SubmissionAqnBase unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SubmissionAqnBase
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum_networking.models.submission_aqn_base.SubmissionAqnBase()  # noqa: E501
        if include_optional :
            return SubmissionAqnBase(
                classical_channels = [
                    aliro_quantum_networking.models.classical_channel.ClassicalChannel(
                        delay = 0, 
                        distance = 0, 
                        node_from = '0', 
                        node_to = '0', )
                    ], 
                global_settings = aliro_quantum_networking.models.submission_aqn_base_global_settings.SubmissionAqnBase_globalSettings(
                    excitation_rate = 0, 
                    purification_protocol_name = 'BBPSSW_X', ), 
                nodes = [
                    aliro_quantum_networking.models.node.Node(
                        measurement_error_probability = 0, 
                        memories = [
                            null
                            ], 
                        name = '0', 
                        operation_errors = {
                            'key' : aliro_quantum_networking.models.node_operation_errors.Node_operationErrors(
                                error_models = [
                                    aliro_quantum_networking.models.error_model.ErrorModel(
                                        error_model_name = 'bitflip', 
                                        probability = 0, )
                                    ], 
                                gate_name = 'CNOT', )
                            }, )
                    ], 
                quantum_connections = [
                    aliro_quantum_networking.models.quantum_connection.QuantumConnection(
                        attenuation = 0, 
                        dark_count_rate = 0, 
                        distance = 0, 
                        efficiency = 0, 
                        error_models = [
                            aliro_quantum_networking.models.error_model.ErrorModel(
                                error_model_name = 'bitflip', 
                                probability = 0, )
                            ], 
                        name = '0', 
                        node_from = '0', 
                        node_to = '0', )
                    ], 
                request = aliro_quantum_networking.models.request.Request(
                    memory_size = 56, 
                    node_from = '0', 
                    node_to = '0', 
                    target_fidelity = 0, 
                    time_beginning = 0, 
                    time_end = 1.337, )
            )
        else :
            return SubmissionAqnBase(
                nodes = [
                    aliro_quantum_networking.models.node.Node(
                        measurement_error_probability = 0, 
                        memories = [
                            null
                            ], 
                        name = '0', 
                        operation_errors = {
                            'key' : aliro_quantum_networking.models.node_operation_errors.Node_operationErrors(
                                error_models = [
                                    aliro_quantum_networking.models.error_model.ErrorModel(
                                        error_model_name = 'bitflip', 
                                        probability = 0, )
                                    ], 
                                gate_name = 'CNOT', )
                            }, )
                    ],
                quantum_connections = [
                    aliro_quantum_networking.models.quantum_connection.QuantumConnection(
                        attenuation = 0, 
                        dark_count_rate = 0, 
                        distance = 0, 
                        efficiency = 0, 
                        error_models = [
                            aliro_quantum_networking.models.error_model.ErrorModel(
                                error_model_name = 'bitflip', 
                                probability = 0, )
                            ], 
                        name = '0', 
                        node_from = '0', 
                        node_to = '0', )
                    ],
                request = aliro_quantum_networking.models.request.Request(
                    memory_size = 56, 
                    node_from = '0', 
                    node_to = '0', 
                    target_fidelity = 0, 
                    time_beginning = 0, 
                    time_end = 1.337, ),
        )

    def testSubmissionAqnBase(self):
        """Test SubmissionAqnBase"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
