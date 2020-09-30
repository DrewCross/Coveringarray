# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class Coveringarray:
    '''
    Module Name:
    Coveringarray

    Module Description:
    A KBase module: Coveringarray
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/DrewCross/Coveringarray"
    GIT_COMMIT_HASH = "1e1cdbb52210cb384ee78040e112b5438eb544f3"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_Coveringarray(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_Coveringarray


        # for each 'container_object' iterate for each option, sum object options and number of objects to create strength, and factors numbers
        int strength = 2
        int factors
        str pairs
        int value

        #container_object is a list due to 'allow multiple' = true 
        #each entry in container_object list has its own grouping of settings 1,2,3
        #all entry forms are free form text boxes associated with a known id
        # of measuring strenth and factors through volume of known id, and pairs through combinations of known id,
        #user input never is used in the program
        # after coveringarray output is obtained, the container object list is used to swap id with text form entries.
        # strength = params["strength"]
       for x in params["container_object"]:
        # records number of objects with settings",

        factors++
        value  = 0
        for y in params["container_object"][x]:
            if y != "empty":
                value++
        pairs = pairs + value + '1\n'


            #records number of settings in each object",

            

            # ? how to sum of pair sequence?


        formattedParams = strength + '\n' + factors + '\n' + pairs
        #formattedParams = params["strength"] +'\n'+ params["factors"] +'\n'+ params["pairs"]

       # formattedParams = "2\n4\n3 1 \n3 1\n3 1\n2 1" ################### Legacy test string, example of formatted input


        inputfile = open("inputfile.txt",'w')

        inputfile.write(formattedParams)

        inputfile.close()

        os.system('/kb/module/./cover inputfile.txt -F')

        outputfile = open("anneal.out",'r')

        outputText = outputfile.read()

        

       # print("This is the print text of annealing: "+outputText)

        
        
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': outputText},
                                                'workspace_name': params['workspace_name']

                                                })
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }
        #END run_Coveringarray

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_Coveringarray return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
