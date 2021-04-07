# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from biokbase.workspace.client import Workspace
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
    GIT_COMMIT_HASH = "846012f78bfb1d35177b3f8c4b350e055f04614a"

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
        self.workspaceURL = config['workspace-url']
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
                if setting['option_1'] != "":
                    nameList[setting['option_1']] = len(setting['option_2'])
                    for option in setting['option_2']:
                        valueList.append(option)

            # each params["container_object"][x] is a has a list with a name
            # and another list of strings
        else:
            medianame = params['workspace_name']+"/"+str(params['input_media'])

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

            if params['evaluation_options'] == 'append_media':
                print("\n\n== Append Element Mode ==\n\n")
                for compound in mediaComps:
                    
                    cref = compound['compound_ref'].split("/")[-1]
                    nameList[cref] = 2
                    valueList.append(compound['maxFlux'])
                    valueList.append(0)

                for setting in params['container_object']:
                    if setting['option_1'] != "":
                        nameList[setting['option_1']] = len(setting['option_2'])
                        for option in setting['option_2']:
                            valueList.append(option)


                   

            elif params['evaluation_options'] == 'overwrite_media':
                print("\n\n== Overwrite Media Elements Mode ==\n\n")

                for compound in mediaComps:

                    cref = compound['compound_ref'].split("/")[-1]

                    for setting in params['container_object']:
                        if cref == setting['option_1']:
                            nameList[cref] = len(setting['option_2'])
                            for value in setting['option_2']:
                                valueList.append(value)

            elif params['evaluation_options'] == 'isolate_media':
                print("\n\n== Overwrite Media Elements Mode ==\n\n")

                for compound in mediaComps:
                    cref = compound['compound_ref'].split("/")[-1]

                    for setting in params['container_object']:
                        if cref == setting['option_1']:
                            nameList[cref] = 2
                            valueList.append(compound['maxFlux'])
                            valueList.append(0)






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
        trimmedOutFile = ""

        matrixData = {
        "row_ids":[],
        "column_ids":[],
        "row_labels":['combinations'],
        "column_labels":['compounds'],
        "row_groups_ids":['1'],
        "column_groups_ids":['1'],
        "data":[[]]


        }        

        

        for name in nameList:
            finaloutputText += name
            finaloutputText += " "
            matrixData["column_ids"].append(name)


        finaloutputText += "\n ==================== \n"

      

        # count by line instead, look for empty line followed by length 1 line to start
        matrixReadFlag = 0
        outPutLead = 0
        n=1
        for line in outputfile:

            if outPutLead != 0 and matrixReadFlag == 10:
                matrixData["row_ids"].append('row'+str(n))
                n+=1
                for c in line.split():
                    if len(line) > 2 and c != str(outPutLead):

                        finaloutputText += str(valueList[int(c)])
                        finaloutputText += ","
                        trimmedOutFile += str(valueList[int(c)])
                        trimmedOutFile += ","
                    else:

                        finaloutputText += c
                        finaloutputText += ","
                        trimmedOutFile += c
                        trimmedOutFile += ","

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


        matrixData["data"]=[[] for i in range(len(matrixData["row_ids"]))]

        listversion = [n.strip() for n in trimmedOutFile.split(',')]

        for row in range(len(matrixData["row_ids"])):
            for column in range(len(matrixData["column_ids"])):

                matrixData["data"][row].append(listversion[column+(row)*len(matrixData["column_ids"])])
            

        

       


        print("\n\n\n FINAL OUTPUT\n" + finaloutputText + "\nFINAL OUTPUT  \n\n\n" + rawout)


        if params['output_media'] is not None:

            workspaceClient = Workspace(self.workspaceURL,token = ctx['token'])

            matrixObject = workspaceClient.save_objects({'workspace': params['workspace_name'],
                                                    'objects': [{'name':params['output_media'],
                                                    'type':'MAK.StringDataTable',
                                                    'data': matrixData}]
                                                                    })


# each value is organizated by order, with pairs grouped
        #object_report = {'ref':matrixObject[0]['ref'],'description': 'Covering array matrix generated by Build Covering Array'}
     
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report':{
                                    'text_message': finaloutputText},
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

    def gen_html_table(self,matrixData):




    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
