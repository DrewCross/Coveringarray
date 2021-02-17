#-*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os


from installed_clients.DataFileUtilClient import DataFileUtil
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
    GIT_COMMIT_HASH = "8e42fea9bbb2ec3455a32cec1bdc7d3cd4980195"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
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

        # for each 'container_object' iterate for each option,
        # sum object options and number of objects to create strength, and factors numbers
        strength = 2
        valueList = []
        nameList = {}
        sampleSize = 0
        # turn namelist into a dict, assign name with value of len(opt2) at assignment time

        # [params]
        #   [container_object]
        #       [variable length x1,x2,xn]
        #           [name]
        #           [values]
        #               [variable length x1,x2,xn]
        # container_object is a list due to 'allow multiple' = true
        # each entry in container_object list has its own grouping of settings 1,2,3
        # all entry forms are free form text boxes associated with a known id
        # of measuring strenth and factors through volume of known id,
        # and pairs through combinations of known id,
        # user input never is used in the program to keep track of order
        # after coveringarray output is obtained, the container object list is used
        # to swap id with text form entries.
        # strength = params["strength"]
        strength = int(params['option_0'])

        if params['input_media'] == "" or params['input_media'] is None:  # flake8 change

            for setting in params['container_object']:
                if setting['option_1'] != "empty":
                    nameList[setting['option_1']] = len(setting['option_2'])
                    for option in setting['option_2']:
                        valueList.append(option)

            # each params["container_object"][x] is a has a list with a name
            # and another list of strings
        else:
            medianame = params['workspace_name']+"/"+str(params['input_media'][0])

            media = self.dfu.get_objects({'object_refs': [medianame]})['data'][0]['data']

            # print('\n\n ======' + str(media.items()) + '=======\n\n')
            # for modnames in params['container_object']
            #     if modnames['option_0'] == compound['name']
            #         compo
            print(media['id'])

            mediaComps = media.get("mediacompounds")

            # print('\n\n ======' + str(mediaComps.items()) + '=======\n\n')
            crefMatch = 0
            print("\n\n==cref match init"+"==\n\n")

            if params['inclusive_toggle'] == 1:
                print("\n\n== Toggle=1 recognized ==\n\n")
                for compound in mediaComps:
                    crefMatch = 0
                    cref = compound['compound_ref'].split("/")[-1]

                    for setting in params['container_object']:
                        if cref == setting['option_1']:
                            crefMatch = 1
                            nameList[cref] = len(setting['option_2'])
                            for value in setting['option_2']:
                                valueList.append(value)

                    if crefMatch == 0:
                        nameList[cref] = 2
                        valueList.append(compound['maxFlux'])
                        valueList.append(0)

            elif params['inclusive_toggle'] == 0:
                print("\n\n== Toggle=1 recognized ==\n\n")

                for compound in mediaComps:

                    cref = compound['compound_ref'].split("/")[-1]

                    for setting in params['container_object']:
                        if cref == setting['option_1']:
                            nameList[cref] = len(setting['option_2'])
                            for value in setting['option_2']:
                                valueList.append(value)

        sampleSize = len(nameList)
        print("\n\n== samplesize adjusted ==\n\n")

        formattedParams = str(strength) + '\n' + str(sampleSize) + '\n'

        for name in nameList:
            formattedParams += str(nameList[name]) + ' 1\n'

        inputfile = open("inputfile.txt", 'w')

        inputfile.write(formattedParams)

        inputfile.close()

        inputfile = open("inputfile.txt", 'r')

        print("\n\n============== Formatted Input Begin ===============\n\n")

        for line in inputfile:
            print(line)

        inputfile.close()

        print("\n\n============== Formatted Input End ===============\n\n")

        os.system('/kb/module/./cover inputfile.txt -F')

        outputfile = open("anneal.out", 'r')
        rawout = " "

        for line in outputfile:
            rawout += line

        outputfile.close()

        outputfile = open("anneal.out", 'r')

        finaloutputText = " "

        for name in nameList:
            finaloutputText += name
            finaloutputText += " "

        finaloutputText += "\n ==================== \n"
        # count by line instead, look for empty line followed by length 1 line to start
        matrixReadFlag = 0
        outPutLead = 0
        for line in outputfile:

            if outPutLead != 0 and matrixReadFlag == 10:
                for c in line.split():
                    if len(line) > 2 and c != str(outPutLead):

                        finaloutputText += str(valueList[int(c)])
                        finaloutputText += ","
                    else:

                        finaloutputText += c
                        finaloutputText += ","

                finaloutputText = finaloutputText[:-1]
                finaloutputText += "\n"

            if matrixReadFlag == 3:
                outPutLead = line
                print(outPutLead)
                print("\n\n" + line + "\n\n")
                finaloutputText += "Sample Size: " + outPutLead + " \n"
                matrixReadFlag = 10

            if(line == "\n" and len(line) == 1):
                matrixReadFlag += 1

        print("\n\n\n FINAL OUTPUT\n" + finaloutputText + "\nFINAL OUTPUT  \n\n\n" + rawout)


# each value is organizated by order, with pairs grouped

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created': [],
                                    'text_message': finaloutputText},
                                    'workspace_name': params['workspace_name']
                                    })
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
            'raw_output': rawout
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
