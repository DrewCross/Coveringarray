# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import copy
import traceback
import json
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
    VERSION = "0.1.6"
    GIT_URL = "git@github.com:DrewCross/Coveringarray.git"
    GIT_COMMIT_HASH = "e1e9bfe0f34eaca3a31f027792f47b0f4e594e5d"

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
        #try catch for lack in media object failure

        for key,value in params.items():
            print ("{},{}".format(key,value))
        
        if params['whole_media'] == "" or params['whole_media'] is None:  # flake8 change
            try:

                for setting in params['container_object']:
                    if setting['option_1'] != "":
                        nameList[setting['option_1']] = len(setting['option_2'])
                        for option in setting['option_2']:
                            valueList.append(option)
            except:
                print("Failed to read in non-media input")

            # each params["container_object"][x] is a has a list with a name
            # and another list of strings

        else:
            #try catch for media object retreival failure
            mediainput = params['input_media']

            try: 
                if mediainput == "Full": 
                    mediainput = params['whole_media']
                    medianame = params['workspace_name']+"/"+str(mediainput)
                    media = self.dfu.get_objects({'object_refs': [medianame]})['data'][0]['data']
                    print(media['id'])
## if input is full, input it replaced with media name, and proceed as normal
                    mediaComps = media.get("mediacompounds")

                    
                else:
                    wholeinput = params['whole_media']
                    wholename = params['workspace_name']+"/"+str(wholeinput)
                    whole = self.dfu.get_objects({'object_refs': [wholename]})['data'][0]['data']
                    print(whole['id'])
## if input is full, input it replaced with media name, and proceed as normal
                    wholeComps = whole.get("mediacompounds")
                    mediaComps = []


                    
                    print("BEFORE NEW CODE TEST!!!!!!!!!!!")
                    for mList in mediainput:
                        
                        for comp in wholeComps:
                            
                            cref = comp['compound_ref']
                            print("CREF: {}, mLIST: {} !!!!".format(cref,mList))

                            if cref == mList and comp not in mediaComps:
                                print("THIS IS A MATCH!!!{}".format(cref))
                                mediaComps.append(comp)

                    for comp in mediaComps:
                        print("TEST LOOK HERE!!!{}".format(comp))

                    print("END TEST SECTION ENDER")


#set mediacomps to list of dicts as "/" + name                 

                

                

                # print('\n\n ======' + str(media.items()) + '=======\n\n')
                # for modnames in params['container_object']
                #     if modnames['option_0'] == compound['name']
                #         compo
                

                # print('\n\n ======' + str(mediaComps.items()) + '=======\n\n')
                crefMatch = 0
                print("\n\n==cref match init"+"==\n\n")
            except:
                print("Media read in failure")


            try:
                if params['evaluation_options'] == 'append_media':
                    print("\n\n== Append Element Mode ==\n\n")
                    for compound in mediaComps:
                        
                        cref = compound['compound_ref'].split("/")[-1]
                        nameList[cref] = 2
                        valueList.append(compound['maxFlux'])
                        valueList.append(-100)

                    for setting in params['container_object']:
                        if setting['option_1'] != "":
                            nameList[setting['option_1']] = len(setting['option_2'])
                            for option in setting['option_2']:
                                valueList.append(option)
            except:
                print("Append media option failure")


                   
            try:
                if params['evaluation_options'] == 'overwrite_media':
                    ow = 0
                    print("\n\n== Overwrite Media Elements Mode ==\n\n")

                    for compound in mediaComps:
                        ow = 0

                        cref = compound['compound_ref'].split("/")[-1]

                        for setting in params['container_object']:
                            if cref == setting['option_1']:
                                ow = 1
                                nameList[cref] = len(setting['option_2'])
                                for value in setting['option_2']:
                                    valueList.append(value)
                        if ow == 0:
                            nameList[cref] = 2
                            valueList.append(compound['maxFlux'])
                            valueList.append(-100)
            except:
                print("Overwrite media option failure")



            try:
                if params['evaluation_options'] == 'isolate_media':
                    print("\n\n== Isolate Media Elements Mode ==\n\n")

                    for compound in mediaComps:
                        cref = compound['compound_ref'].split("/")[-1]

                        for setting in params['container_object']:
                            if cref == setting['option_1']:
                                nameList[cref] = 2
                                valueList.append(compound['maxFlux'])
                                valueList.append(-100)
            except:
                print("Isolate media option failure")








        sampleSize = len(nameList)
        print("\n\n== samplesize adjusted to " + str(sampleSize) + " ==\n\n")

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

        try:
            os.system('/kb/module/./cover inputfile.txt -F')
            
            outputfile = open("anneal.out", 'r')
            rawout = " "

            for line in outputfile:
                rawout += line

            outputfile.close()

            outputfile = open("anneal.out", 'r')
        except:
            print("Wrapped cover tool failure")

        finaloutputText = " "
        trimmedOutFile = ""


        #if json out do this elif media out do that else
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


        if params['evaluation_options'] == 'isolate_media':
            unchangedmedialist = []

            for compound in mediaComps:
                    cref = compound['compound_ref'].split("/")[-1]

                    if cref not in matrixData['column_ids']:
                        unchangedmedialist.append([cref,compound['maxFlux']])
                        

            for item in unchangedmedialist:
                matrixData['column_ids'].append(item[0])
                for row in matrixData["data"]:
                    row.append(item[1])


            

        

       
        #replace finaloutput text script with sourcing from matrixdata

        print("\n\n\n FINAL OUTPUT\n" + finaloutputText + "\nFINAL OUTPUT  \n\n\n" + rawout)


        if params['output_media'] is not None or params['output_json_check'] == 1:

            workspaceClient = Workspace(self.workspaceURL,token = ctx['token'])
            #try catch for json object creation 
            try:
                matrixObject = workspaceClient.save_objects({'workspace': params['workspace_name'],
                                                        'objects': [{'name':params['output_media'],
                                                        'type':'MAK.StringDataTable',
                                                        'data': matrixData}]
                                                                        })
            except:
                print("JSON out object creation")


        test_media = {
            'mediacompounds':[{'compound_ref':'testref1','concentration':100,'minFlux':0,'maxFlux':0},{'compound_ref':'testref2','concentration':100,'minFlux':100,'maxFlux':100}],
            'isMinimal':0,
            'isDefined':0,
            'type':'Undefined',
            'name':'testname',
            'id':'testid'
        }
          #  def __copy__(self):
           #     return MediaCompound(self.compound_ref,self.concentration,self.minFlux,self.maxFlux)
            #def __deepcopy__(self,memo):
             #   return MediaCompound(copy.deepcopy(self.compound_ref,self.concentration,self.minFlux,self.maxFlux,memo))

##IDEAS 10/28/21: give a default value for compound_reference.
##remove deepcopys and pass reference to preserve original object
#call workspace save on each piece before assembling
        def make_compound(compound_ref,concentration,minFlux,maxFlux):
            mediaCompound = { 
            'compound_ref': "489/6/8/"+"compounds/"+"id/"+compound_ref, ##KBaseBiochem.Biochemistry.compounds.*.id
            'concentration':concentration, #first SECTION IS WORKSPACE NAME KBASEBIOCHEM -> WORKSPACE NAME I think it uses workspaceclient getobjects2 in order to fetch, check getobjects2 api!
            'minFlux':minFlux,
            'maxFlux':maxFlux
            } #potential reason: reference cpdxxx unrecognized error: media obect meta data shows "null" for extracted ids field and with no data bout the compounds
            return mediaCompound #CAUSES: refernce data/ointers lost in the media creation process: solution, more deepcopies

        if params['output_media'] is not None and params['output_media_check'] == 1:
            media_compounds_data = []
            media_data = {}
            media_data_list = []

            for index1, case in enumerate(matrixData['data']):
                media_compounds_data = []##BELOW ISSUE: On CDG TESTS, sizes go from 20 -> 9 on 3 compound isolations, why are ~50% of reactions changing to sub 0?
                for index2, compound in enumerate(case): ###BELOW: Maybe? Is object creation tied to the test suite? I Dont remember...
                    if float(compound) > 0: ##Compound filtering for trimmed makeups will conflict with test suite expected outcome of Coveing Array Tool
                        media_compound = make_compound(matrixData['column_ids'][index2],.001,-100,float(compound))
                        media_compounds_data.append(copy.deepcopy(media_compound))
                media_data = {
                'mediacompounds':copy.deepcopy(media_compounds_data),
                'isMinimal':0,
                'isDefined':0,
                'type':'Undefined',
                'name':params['output_media']+str(index1),
                'id':params['output_media']+str(index1),
                'sourceid':params['output_media']+str(index1)
                } 
                media_data_list.append(copy.deepcopy(media_data))
            for index,media in enumerate(media_data_list):
                try:
                    workspaceClient.save_objects({'workspace': params['workspace_name'],
                                                        'objects': [{'name':media['name'],
                                                        'type':'KBaseBiochem.Media',
                                                        'data': media}]
                                                                        })
                except:
                    print("\n\n ERROR TRACE: \n\n" + traceback.format_exc()+'\n\n')
                    print("KbaseBioChem.Media object out object creation failure")
                    print("Media " + str(media['name']) + "Keys:\n" + str(media.keys())+'\n')

                    print("Media " + str(media['name']) +  "Values:\n" +'\n')

                    for x,value in enumerate(media['mediacompounds']):
                        print("Media compound "+ str(x) + ": "+ str(media['mediacompounds'][x]) +"\n")

                    print("Other media properties"+str(media['isMinimal'])+ ' '+ str(media['isDefined'])+' ' + str(media['type'])+' ' + media['name']+' ' + media['media_id'])
                    

#            matrixData = {
  #      "row_ids":[],
  #      "column_ids":[],
  #      "row_labels":['combinations'],
  #      "column_labels":['compounds'],
  #      "row_groups_ids":['1'],
  #      "column_groups_ids":['1'],
 #       "data":[[]]
#
#
 #       }    

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
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
