# -*- coding: utf-8 -*-
import os
import subprocess
import time
import unittest
from configparser import ConfigParser

from Coveringarray.CoveringarrayImpl import Coveringarray
from Coveringarray.CoveringarrayServer import MethodContext
from Coveringarray.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class CoveringarrayTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('Coveringarray'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'Coveringarray',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = Coveringarray(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "_test_Cover_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_Cover_"+str(suffix)
        ret = self.getWsClient().create_workspace({'workspace':wsName})
        self.__class__.wsName = wsName
        return wsName
    def getImpl(self):
        return self.__class__.serviceImpl
    def getContext(self):
        return self.__class__.ctx


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    
    def testManualInput(self):

        testMedia = {"__VERSION__":1,"id":"kb|media.664","isDefined":0,"isMinimal":0,"mediacompounds":[{"compound_ref":"kbase/default/compounds/id/cpd00205",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00242","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00048","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00009",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00007","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00013","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00971",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00067","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00001","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00036",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00100","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00023","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00027",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd10516","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00058","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00099",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00137","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00063","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00254",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00030","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00034","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00149",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00244","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd10515","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd11574",
        "concentration":0.001,"maxFlux":100,"minFlux":-100}],"name":"7H9","source_id":"7H9","type":"unspecified"}

        #weka has the object saved in the setupclass method
        mediaObject = self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'name':'Mediain',
                                                                    'type':'KBaseBiochem.Media',
                                                                    'data':testMedia }]
                                                                    })[0]
        # Prepare test objects in workspace if needed using
       
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        ret = self.serviceImpl.run_Coveringarray(self.ctx, {'workspace_name': self.wsName,'option_0':"2",
                                                            'container_object': [{"option_1":"Firefox", "option_2":["on","off"]},
                                                                {"option_1":"Network", "option_2":["on","off"]},
                                                                {"option_1":"Feature", "option_2":["ready","unready","unsure"]},{"option_1":"os", "option_2":["low","medium","high","very high"]}
                                                                ],
                                                            'input_media':'','inclusive_toggle':0})

        arrayValid = int(subprocess.check_output(['/kb/module/./checkpairs','/kb/module/anneal.out']))
        self.assertEqual(arrayValid,0,"Produced incorrect coverage array")
    def testMediaInput(self):
        testMedia = {"__VERSION__":1,"id":"kb|media.664","isDefined":0,"isMinimal":0,"mediacompounds":[{"compound_ref":"kbase/default/compounds/id/cpd00205",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00242","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00048","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00009",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00007","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00013","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00971",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00067","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00001","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00036",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00100","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00023","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00027",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd10516","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00058","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00099",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00137","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00063","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00254",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00030","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00034","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00149",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00244","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd10515","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd11574",
        "concentration":0.001,"maxFlux":100,"minFlux":-100}],"name":"7H9","source_id":"7H9","type":"unspecified"}
        #weka has the object saved in the setupclass method
        mediaObject = self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'name':'Mediain',
                                                                    'type':'KBaseBiochem.Media',
                                                                    'data':testMedia }]
                                                                    })[0]

        
        ret = self.serviceImpl.run_Coveringarray(self.ctx, {'workspace_name': self.wsName, 'container_object':[{'option_1':'','option_2':''}],'option_0':"2",'input_media':mediaObject,'inclusive_toggle':1})
        arrayValid = int(subprocess.check_output(['/kb/module/./checkpairs','/kb/module/anneal.out']))
        self.assertEqual(arrayValid,0,"Produced incorrect coverage array")
        #identify consistent member of tool output that indicates success
        #self.assertEqual(ret, "OK")
    def testManualandMediaInputExclusive(self):
        testMedia = {"__VERSION__":1,"id":"kb|media.664","isDefined":0,"isMinimal":0,"mediacompounds":[{"compound_ref":"kbase/default/compounds/id/cpd00205",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00242","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00048","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00009",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00007","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00013","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00971",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00067","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00001","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00036",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00100","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00023","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00027",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd10516","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00058","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00099",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00137","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00063","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00254",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00030","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00034","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00149",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00244","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd10515","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd11574",
        "concentration":0.001,"maxFlux":100,"minFlux":-100}],"name":"7H9","source_id":"7H9","type":"unspecified"}
        #weka has the object saved in the setupclass method
        mediaObject = self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'name':'Mediain',
                                                                    'type':'KBaseBiochem.Media',
                                                                    'data':testMedia }]
                                                                    })[0]

        ret = self.serviceImpl.run_Coveringarray(self.ctx, {'workspace_name': self.wsName,'option_0':"2",
                                                            'container_object': [{"option_1":"cpd00007", "option_2":["100","0"]},
                                                                {"option_1":"cpd00009", "option_2":["100","0"]}
                                                                ],
                                                            'input_media':mediaObject,'inclusive_toggle':0})
        arrayValid = int(subprocess.check_output(['/kb/module/./checkpairs','/kb/module/anneal.out']))
        self.assertEqual(arrayValid,0,"Produced incorrect coverage array")
        



    def testManualandMediaInputInclusive(self):
        testMedia = {"__VERSION__":1,"id":"kb|media.664","isDefined":0,"isMinimal":0,"mediacompounds":[{"compound_ref":"kbase/default/compounds/id/cpd00205",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00242","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00048","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00009",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00007","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00013","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00971",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00067","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00001","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00036",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00100","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00023","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00027",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd10516","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00058","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00099",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00137","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00063","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00254",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00030","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd00034","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00149",
        "concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd00244","concentration":0.001,"maxFlux":100,"minFlux":-100},
        {"compound_ref":"kbase/default/compounds/id/cpd10515","concentration":0.001,"maxFlux":100,"minFlux":-100},{"compound_ref":"kbase/default/compounds/id/cpd11574",
        "concentration":0.001,"maxFlux":100,"minFlux":-100}],"name":"7H9","source_id":"7H9","type":"unspecified"}
        #weka has the object saved in the setupclass method
        mediaObject = self.getWsClient().save_objects({'workspace': self.getWsName(),'objects': [{'name':'Mediain',
                                                                    'type':'KBaseBiochem.Media',
                                                                    'data':testMedia }]
                                                                    })[0]


        ret = self.serviceImpl.run_Coveringarray(self.ctx, {'workspace_name': self.wsName,'option_0':"2",
                                                            'container_object': [{"option_1":"cpd00009", "option_2":["90","80"]},
                                                                {"option_1":"cpd00007", "option_2":["70","60"]}
                                                                ],
                                                            'input_media':mediaObject, 'inclusive_toggle':1})
        arrayValid = int(subprocess.check_output(['/kb/module/./checkpairs','/kb/module/anneal.out']))
        self.assertEqual(arrayValid,0,"Produced incorrect coverage array")
        #sef.assertEqual(ret, "OK")




                                                             
