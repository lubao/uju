from threading import Thread
import os
import sys
import array
import Queue
import threading
import time
import logging
import logging.config
import Defines
from SQLEng import SQLEng
from ComAlg import codec
from SchemaReader import AppReader
from SchemaReader import FormReader
from GammuSender import PduSender

class MessageHandler(Thread):
    '''
    This class will handle incomeing message
    '''
    def __init__(self,phone_number,mesg):
        # the new PKG will put into QUEUE
        # self.income_pkg = Queue.Queue(0)
        # self.income_pkg.put(mesg)
        self.phone_number = phone_number
        self.package = self.get_pkg_byte_array(mesg)
        # invoke constructor of parent class
        Thread.__init__(self)
        # Record each SESSIONs' info and current state
        # 0(INIT) -> 1(COLLECTING_REQUEST) -> 2(DONE) and 4 (PENDING)
        # session_info[Session ID]  =  Session Info [Session State , PKG]
        # Put new session in session_info if a session receive a new SESSION ID
        # New session will not be processed utill the current session is DONE
        # self.session_info = {}
        # A flag indicate is there a new session
        #self.hasMoreSession = True
        # record current session ID
        self.current_session_id = -1
        # record TID
        self.tidList = []
        # This LOGGER file copy from PYTHON
        # It will record everything in file
        # and only show ERROR and CRITICAL mesg on console
        self.logger  =  logging.getLogger(phone_number)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh  =  logging.FileHandler("service.log")
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch  =  logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter  =  logging.Formatter("%(asctime)s - 
            %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # add the handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        
    def run(self):
        self.set_session_info()
        self.process_package()
      
    def get_pkg_byte_ary(self, message):
        # Text is a string that present a byte stream in OCT
        pkg = array.array('B')# UNSIGNED CHARACTER  = > 1 BYTE
        self.logger.debug("message  =  %s", message)
        pos = 0
        while pos < len(message):
            pkg.append(int(message[pos:pos+2], 16))
            pos += 2
        return pkg

    def set_session_info(self):
        self.session_status = Defines.SESSION_INIT
        self.current_session_id = self.package[1]
        
    def create_return_package(self,retArray):
        self.logger.debug("Enter Create Pkg")
        package_size = Defines.SMS_SIZE-4
        number_packagess  =  len(retArray) / package_size
        ret_list = []
        if number_packagess % package_size != 0: 
            number_packagess += 1
        if not number_packagess : 
            number_packagess += 1
        for i in range(number_packagess):
            retArray.insert(0,i)
            retArray.insert(0,number_packagess)
            retArray.insert(0,self.current_session_id)
            retArray.insert(0,Defines.RESPONSE_PACKET)
            if i  ==  number_packagess-1: 
                sendArray = retArray[0:len(retArray)]
                for i in range(len(retArray)): retArray.pop(0)
            else: 
                sendArray = retArray[0:package_size]
                for i in range(package_size): retArray.pop(0)
            ret_list.append(sendArray)
        return ret_list
            
    def setACK(self,retArray):
        self.tidList = sorted(self.tidList)
        # Start TID || End TID || ACK LIST ||RESPONSE
        curBitPos = 0
        totalLen = self.tidList[len(self.tidList)-1] - self.tidList[0] + 1
        ackspace  =  (totalLen)/8
        if (totalLen)%8 !=  0: 
            ackspace += 1
        while ackspace>0:
            retArray.insert(0,0)
            ackspace-= 1
        # build ACK vector
        ackList = []
        for i in range (totalLen):
            ackList.append(0)
        start = self.tidList[0]
        for t in self.tidList:
            ackList[t-start] = 1
        #// we have ackvec ready here. stick it into the newresult.    
        for v in ackList:
            startBitPos = curBitPos%8
            curBytePos = curBitPos/8
            mask = 0x1
            #// adjust the mask.
            mask <<=  (7 - startBitPos)
            if v  ==  1:
                #// set the bit at byteNum/offset
                retArray[curBytePos] |=  mask
            else:
                #// clear the bit at byteNum/offset
                retArray[curBytePos] &=  (~mask)
            #// increment the location pointer
            curBitPos += 1
        retArray.insert(0,self.tidList[len(self.tidList)-1])
        retArray.insert(0,self.tidList[0])
        # clear TID List and put it into retArray
        while not len(self.tidList):
            self.tidList.pop()
        return retArray
    
    def process_package(self):
        sender  =  PduSender()
        if self.session_status  ==  Defines.SESSION_INIT :
            self.logger.debug("%s State  =  INIT",self.current_session_id)
            # only TWO type from client to server
            # SESSION_PACKET  =  1
            # ACK_PACKET  =  2;
            # -----------------------------------------------------------
            # |TYPE of PKG || Session ID || 
            #  Num of PKG || PKG Num ||
            # |infoList[1][0] || infoList[1][1] || 
            #  infoList[1][2] || infoList[1][3] ||
            # -----------------------------------------------------------
            if self.package[0]  ==  Defines.ACK_PACKET :
                self.logger.debug(
                    "%s: This is a  ACK_PACKET session",self.current_session_id
                )
                #TODO: 
                # The reliable layer is missing for this release version.
                # client is requesting the lost packets in the current session.
                # check if there are packets for the session id specified
                # by the client then send the SMSes back to the client.
                # else do nothing
                self.session_status = Defines.SESSION_FINISH
            else :
                self.logger.debug(
                    "%s: This is a NEW session",self.current_session_id
                )  
                # if the session has more than 1 pkgs, 
                # go to COLLECT state, otherwise go to DONE state
                # to process pkg
                #TODO:
                # There is a constrains on number of message could be sent in
                # this release version. The number is one.
                if self.package[2] == 1 : 
                    self.session_status = Defines.SESSION_DONE
                else : 
                    self.logger.debug(
                        "%s: Except more PKG",self.current_session_id) 
                    self.session_status = Defines.SESSION_COLLECT
                
        if self.session_status == Defines.SESSION_COLLECT:
            #TODO: 
            #   The reliable layer is missing for this release version.
            #   Client will always send only one message.
            self.session_status = Defines.SESSION_DROP
        
        if self.session_status == Defines.SESSION_DONE:
            # in DONE state
            ret = self.process_transation()
            if ret !=  None:
                ret_list = self.create_return_package(ret)
                for sendAry in ret_list:
                    sender.send(self.phone_number, sendAry)
            self.session_status = Defines.SESSION_FINISH
        
        if self.session_status == Defines.SESSION_DROP:
            self.logger.debug("%s: State  =  DROP",self.current_session_id)
            self.session_info.pop(self.current_session_id)
        

    def process_transation(self):
        self.logger.debug( "Enter process_transation")
        # When we arrive here, it means we have collect all PKG
        # First ignore RELIABLE HEADER  = > 4 byte for each PKG
        #self.package = self.package[i]
        point = Defines.RELIABLE_HEADER_OFFSET
        tId = self.package[point]
        point += 1
        number_query = self.package[point]
        self.logger.debug(
            "%s: There are %s query in this Transaction. TID = %s",
            self.current_session_id,number_query,+tId
        )
        point += 1
        # Second, extract the QUERY from TRANSACTION then executing it
        # Transaction HEADER
        # -------------------------------------------------------------------
        # | TID   || # of Q || Len of Q1 || Q1|| Len of Q2 || Q2||.....
        # --------------------------------------------------------------------
        #                        ^---point is here now.
        #   It is an INT. Make sure We can read it properly
        
        for j in range(number_query):
            len_of_query = self.package[point]
            self.logger.debug(
                "%s: The length of this QUERY is %s",
                    self.current_session_id,len_of_query
            )
            point += 1
            # ByteArray [x:y] 
            # will return an array array('b', ByteArray[x], 
            #                                 ByteArray[x+1],ByteArray[x+2]
            #                            ......,ByteArray[y-1])
            # so In our case, 
            # just point to point+len_of_query will be the Query
            # [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]
            #-------------------------------------------------
            #          ^   ^               ^   ^
            #     len = 5  |-    Query    -|   |->point +len  = > l
            #              ^---current point position
            ret = self.process_query(self.package[point:point+len_of_query])
            point += len_of_query
            # Transaction HEADER
            # ----------------------------------------------------------------
            # ....|| Len of Qn || Qn********* || Len of Qn+1 || Qn+1*********|
            # ----------------------------------------------------------------
            #                                        ^---point is here now.
            
        if ret !=  None:
            # Here means there is a FETCH/FETCH AGG/SEARCH 
            # operation in this QUERY
            self.logger.debug(
                "%s: Building ACK Vector",self.current_session_id
            )
            if len(self.tidList) == 0:
                ret.insert(0,0)
                ret.insert(0,0)
            else:   
                ret = self.setACK(ret)
        return ret
    
    def process_query(self,query):
        mySQLEng = SQLEng()
        # for debug under older configuration
        #query.pop(0)
        aid = query[0]
        fid = query[1]
        self.logger.debug(
            "%s: Start to Execute QUERY  = > App ID = %s",
            self.current_session_id,aid
        )
        self.logger.debug(
            "%s: Start to Execute QUERY  = > Form ID = %s",
            self.current_session_id,fid
        )
        self.logger.debug(
            "%s : Check privacy (Have not really implemented)",
            self.current_session_id
        )
        # Parsing Form description according to fid
        appDict = AppReader().parse_file(aid)
        formDict = FormReader().parse_file(aid,fid)
        myComAlg = codec()
        #TODO : We need to check the privacy before start to process query
        if int(formDict['operation'])  ==  Defines.OP_CREATE_ID or 
           int(formDict['operation'])  ==  Defines.OP_UPDATE_ID:
            self.logger.debug(
                "%s : This is a CREATE/UPDATE OPERATION QUERY",
                self.current_session_id
            )
            self.logger.debug("%s : Decode the QUERY",self.current_session_id)
            appendDict = myComAlg.decode(appDict, formDict, query)
            SQL = mySQLEng.getInsertSQL(appendDict)
            self.logger.debug("%s : SQL =  %s",self.current_session_id,SQL)
            mySQLEng.exeSQL(SQL)
            return None
        
        if int(formDict['operation'])  ==  Defines.OP_SEARCH_ID:
            self.logger.debug(
                "%s : This is a SEARCH OPERATION QUERY",
                self.current_session_id
            )
            self.logger.debug(
                "%s : Decode the QUERY",self.current_session_id
            )
            searchDict = myComAlg.decode(appDict, formDict, query)
            self.logger.debug(
                "%s : Get the fetch field list",self.current_session_id)
            for sid in formDict['schemas']:
                fetchList = self.getFetchList(
                    formDict['schemas'][sid]['fetch'],appDict['schemas'][sid]
                )
            SQL = mySQLEng.getSearchSQL(searchDict,fetchList)
            
        if int(formDict['operation'])  ==  Defines.OP_DESTROY_ID:
            self.logger.debug(
                "%s : This is a DESTORY OPERATION QUERY",
                self.current_session_id
            )
            self.logger.debug("%s : Decode the QUERY",self.current_session_id)
            destroyDict = myComAlg.decode(appDict, formDict, query)
            SQL = mySQLEng.getDestroySQL(destroyDict)
            self.logger.debug("%s : SQL =  %s",self.current_session_id,SQL)
            mySQLEng.exeSQL(SQL)
            return None
        
        if int(formDict['operation'])  ==  Defines.OP_ADV_SEARCH_ID:
            self.logger.debug(
                "%s : This is a ADVANCE SEARCH OPERATION QUERY",
                self.current_session_id
            )
            self.logger.debug("%s : Decode the QUERY",self.current_session_id)
        
        result = mySQLEng.exeSQL(SQL)
        
        if result :
            self.logger.debug("%s : FETCH DATA DONE",self.current_session_id)
            self.logger.debug(
                "%s : Encode FETCH Result",self.current_session_id
            )
            ret = myComAlg.encodeFetchResult(
                result, AppReader().parse_file(aid), 
                FormReader().parse_file(aid,fid)
            )
            self.logger.debug(
                "%s : ADD Header for FETCH Result",
                self.current_session_id)
            ret.insert(0,Defines.RESULT_RESPONSE)
            return ret
        else:
            self.logger.debug("%s : OPERATION FAIL",self.current_session_id)
            self.logger.debug("%s : MySQL reply  =  %s",
                        self.current_session_id,result
            )
            # Build a JustMessage reponse here
            ret = array.array('B')
            res = "Record does not exist"
            ret = array.array('B',res)
            ret.insert(0,len(ret))
            ret.insert(0,Defines.JUST_MESSAGE_RESPONSE)
            return ret
        return
    
    def getFetchList(self,commonField,fieldList):
        fetchList = []
        for id in commonField:
            fetchList.append(fieldList[id]['name'])
        return fetchList
