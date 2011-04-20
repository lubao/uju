'''
Created on Nov 25, 2009

@author: paul
'''
import Defines
import array
import math

class codec(object):
    '''
    classdocs
    This class will take an input, byte array, and de-compress it
    according to form description
    The outpout is according to the operation
    either a Dict or List
    '''
    def __init__(self):
        '''
        Constructor
        '''
    #===========================================================================
    # def decord(self,appDict,formDict,queryByteArray):
    #    data={}
    #    queryByteArray.pop(0)# Form id
    #    curBitPos=0
    #    #=======================================================================
    #    # for (k,v) in ((myHandler.appDict['schemas'])['0']).iteritems():
    #    #    print (k,v)
    #    #    ('name', u'HIV Medical Historoy')
    #    #    (u'1', {'range': u'17', 'type': u'int', 'name': u'Employee ID'})
    #    #    (u'0', {'range': u'17', 'type': u'int', 'name': u'Patient ID'})
    #    #    (u'3', {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']})
    #    #    (u'2', {'range': u'-1', 'type': u'int', 'name': u'Date'})
    #    #    (u'5', {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']})
    #    #    (u'4', {'range': u'0', 'type': u'text', 'name': u'ELISA'})
    #    #    (u'7', {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'})
    #    #    (u'6', {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'})
    #    #    (u'8', {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'})
    #    #=======================================================================
    #    #=======================================================================
    #    # for (k,v) in myHandler.formDict.iteritems():
    #    #    print (k,v)
    #    #    (u'application', u'0')
    #    #    (u'operation', u'0')
    #    #    (u'id', u'0')
    #    #    (u'name', u'Hiv Patient Intake Form')
    #    #    ('schemas', {u'0': [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']})
    #    #=======================================================================
    #    
    #    formTableDict=formDict['schemas']
    #    for sid in formTableDict.iterkeys():
    #        appSchemaDict=appDict['schemas'][sid]
    #        tableList=formTableDict[sid]
    #        #===================================================================
    #        # print "{0}{1}".format("sid=",sid)
    #        # print appSchemaDict
    #        # print tableList
    #        # sid=0
    #        # {'name': u'HIV Medical Historoy', 
    #        #   u'1': {'range': u'17', 'type': u'int', 'name': u'Employee ID'}, 
    #        #   u'0': {'range': u'17', 'type': u'int', 'name': u'Patient ID'}, 
    #        #   u'3': {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']}, 
    #        #   u'2': {'range': u'-1', 'type': u'int', 'name': u'Date'}, 
    #        #   u'5': {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']}, 
    #        #   u'4': {'range': u'0', 'type': u'text', 'name': u'ELISA'}, 
    #        #   u'7': {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'}, 
    #        #   u'6': {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'}, 
    #        #   u'8': {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'}}
    #        # [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']
    #        #===================================================================
    #        for fieldID in tableList:
    #            range=int(appSchemaDict[fieldID]['range'])
    #            if range==Defines.DATE_FIELD_RANGE : 
    #                range=16 # date
    #                data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
    #                curBitPos += range
    #            elif range==Defines.STR_FIELD_RANGE: # str
    #                strLen=self.getInt(queryByteArray, curBitPos,8)
    #                curBitPos+=8
    #                strArray=array.array('B')
    #                while strLen !=0:
    #                    strLen-=1
    #                    strArray.append(self.getInt(queryByteArray, curBitPos, 8))
    #                    curBitPos+=8
    #                data[appSchemaDict[fieldID]['name']]=strArray.tostring()
    #            elif range==Defines.MC_FIELD_RANGE:
    #                range=1
    #                chList=appSchemaDict[fieldID]['choice']
    #                for ch in chList:
    #                    data[ch]=self.getInt(queryByteArray, curBitPos, range)
    #                    curBitPos += range
    #            elif range==Defines.SC_FIELD_RANGE:
    #                range=math.ceil(math.log(len(appSchemaDict[fieldID]['choice']),2))
    #                select=self.getInt(queryByteArray, curBitPos, range)
    #                data[appSchemaDict[fieldID]['choice'][select]]=1
    #                curBitPos += range
    #            else:
    #                data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
    #                curBitPos += range
    #            data['schemaName']=appDict['schemas'][sid]['name']
    #    return data
    #===========================================================================
    
    def decode(self,appDict,formDict,queryByteArray):
        data={}
        data['dbName']=appDict['name']
        queryByteArray.pop(0)#aid
        queryByteArray.pop(0)#fid
        curBitPos=0
        #=======================================================================
        # for (k,v) in ((myHandler.appDict['schemas'])['0']).iteritems():
        #    print (k,v)
        #    ('name', u'HIV Medical Historoy')
        #    (u'1', {'range': u'17', 'type': u'int', 'name': u'Employee ID'})
        #    (u'0', {'range': u'17', 'type': u'int', 'name': u'Patient ID'})
        #    (u'3', {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']})
        #    (u'2', {'range': u'-1', 'type': u'int', 'name': u'Date'})
        #    (u'5', {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']})
        #    (u'4', {'range': u'0', 'type': u'text', 'name': u'ELISA'})
        #    (u'7', {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'})
        #    (u'6', {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'})
        #    (u'8', {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'})
        #=======================================================================
        #=======================================================================
        # for (k,v) in myHandler.formDict.iteritems():
        #    print (k,v)
        #    (u'application', u'0')
        #    (u'operation', u'0')
        #    (u'id', u'0')
        #    (u'name', u'Hiv Patient Intake Form')
        #    ('schemas', {u'0': [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']})
        #=======================================================================
        
        formTableDict=formDict['schemas']
        for sid in formTableDict.iterkeys():
            appSchemaDict=appDict['schemas'][sid]
            tableList=formTableDict[sid]['fields']
            #===================================================================
            # print "{0}{1}".format("sid=",sid)
            # print appSchemaDict
            # print tableList
            # sid=0
            # {'name': u'HIV Medical Historoy', 
            #   u'1': {'range': u'17', 'type': u'int', 'name': u'Employee ID'}, 
            #   u'0': {'range': u'17', 'type': u'int', 'name': u'Patient ID'}, 
            #   u'3': {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']}, 
            #   u'2': {'range': u'-1', 'type': u'int', 'name': u'Date'}, 
            #   u'5': {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']}, 
            #   u'4': {'range': u'0', 'type': u'text', 'name': u'ELISA'}, 
            #   u'7': {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'}, 
            #   u'6': {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'}, 
            #   u'8': {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'}}
            # [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']
            #===================================================================
            for fieldID in tableList:
                #print fieldID
                range=int(appSchemaDict[fieldID]['range'])
                #print range
                if range==Defines.DATE_FIELD_RANGE : 
                    range=16 # date
                    data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
                    curBitPos += range
                elif range==Defines.STR_FIELD_RANGE: # str
                    strLen=self.getInt(queryByteArray, curBitPos,8)
                    curBitPos+=8
                    strArray=array.array('B')
                    while strLen !=0:
                        strLen-=1
                        strArray.append(self.getInt(queryByteArray, curBitPos, 8))
                        curBitPos+=8
                    data[appSchemaDict[fieldID]['name']]=strArray.tostring()
                elif range==Defines.MC_FIELD_RANGE:
                    range=len(appSchemaDict[fieldID]['choice'])
                    select=self.getInt(queryByteArray, curBitPos, range)
                    data[appSchemaDict[fieldID]['name']]=select
                    curBitPos += range
                elif range==Defines.SC_FIELD_RANGE:
                    range=int(math.ceil(math.log(len(appSchemaDict[fieldID]['choice']),2)))
                    select=self.getInt(queryByteArray, curBitPos, range)
                    data[appSchemaDict[fieldID]['name']]=select
                    curBitPos += range
                else:
                    data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
                    curBitPos += range
                data['schemaName']=appDict['schemas'][sid]['name']
        print data
        return data
    
    #===========================================================================
    # def decordSearch(self,appDict,formDict,queryByteArray):
    #    data={}
    #    queryByteArray.pop(0)# Form id
    #    curBitPos=0
    #    #=======================================================================
    #    # for (k,v) in ((myHandler.appDict['schemas'])['0']).iteritems():
    #    #    print (k,v)
    #    #    ('name', u'HIV Medical Historoy')
    #    #    (u'1', {'range': u'17', 'type': u'int', 'name': u'Employee ID'})
    #    #    (u'0', {'range': u'17', 'type': u'int', 'name': u'Patient ID'})
    #    #    (u'3', {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']})
    #    #    (u'2', {'range': u'-1', 'type': u'int', 'name': u'Date'})
    #    #    (u'5', {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']})
    #    #    (u'4', {'range': u'0', 'type': u'text', 'name': u'ELISA'})
    #    #    (u'7', {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'})
    #    #    (u'6', {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'})
    #    #    (u'8', {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'})
    #    #=======================================================================
    #    #=======================================================================
    #    # for (k,v) in myHandler.formDict.iteritems():
    #    #    print (k,v)
    #    #    (u'application', u'0')
    #    #    (u'operation', u'0')
    #    #    (u'id', u'0')
    #    #    (u'name', u'Hiv Patient Intake Form')
    #    #    ('schemas', {u'0': [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']})
    #    #=======================================================================
    #    
    #    formTableDict=formDict['schemas']
    #    for sid in formTableDict.iterkeys():
    #        appSchemaDict=appDict['schemas'][sid]
    #        tableList=formTableDict[sid]
    #        #===================================================================
    #        # print "{0}{1}".format("sid=",sid)
    #        # print appSchemaDict
    #        # print tableList
    #        # sid=0
    #        # {'name': u'HIV Medical Historoy', 
    #        #   u'1': {'range': u'17', 'type': u'int', 'name': u'Employee ID'}, 
    #        #   u'0': {'range': u'17', 'type': u'int', 'name': u'Patient ID'}, 
    #        #   u'3': {'range': u'3', 'type': u'choices', 'name': u'Symptoms', 'choice': [u'Fever', u'Weight loss', u'Nausea']}, 
    #        #   u'2': {'range': u'-1', 'type': u'int', 'name': u'Date'}, 
    #        #   u'5': {'range': u'1', 'type': u'choices', 'name': u'Rapid Antibody', 'choice': [u'Positive', u'Negative']}, 
    #        #   u'4': {'range': u'0', 'type': u'text', 'name': u'ELISA'}, 
    #        #   u'7': {'range': u'7', 'type': u'int', 'name': u'Percentage CD4'}, 
    #        #   u'6': {'range': u'16', 'type': u'int', 'name': u'Absolute CD4'}, 
    #        #   u'8': {'range': u'15', 'type': u'int', 'name': u'Viral Load(Copies/ml)'}}
    #        # [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8']
    #        #===================================================================
    #        for fieldID in tableList:
    #            range=int(appSchemaDict[fieldID]['range'])
    #            if range==Defines.DATE_FIELD_RANGE : 
    #                range=16 # date
    #                data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
    #                curBitPos += range
    #            elif range==Defines.STR_FIELD_RANGE: # str
    #                strLen=self.getInt(queryByteArray, curBitPos,8)
    #                curBitPos+=8
    #                strArray=array.array('B')
    #                while strLen !=0:
    #                    strLen-=1
    #                    strArray.append(self.getInt(queryByteArray, curBitPos, 8))
    #                    curBitPos+=8
    #                data[appSchemaDict[fieldID]['name']]=strArray.tostring()
    #            elif range==Defines.MC_FIELD_RANGE:
    #                range=1
    #                chList=appSchemaDict[fieldID]['choice']
    #                for ch in chList:
    #                    data[ch]=self.getInt(queryByteArray, curBitPos, range)
    #                    curBitPos += range
    #            elif range==Defines.SC_FIELD_RANGE:
    #                range=int(math.ceil(math.log(len(appSchemaDict[fieldID]['choice']),2)))
    #                select=self.getInt(queryByteArray, curBitPos, range)
    #                data[appSchemaDict[fieldID]['choice'][select]]=1
    #                curBitPos += range
    #            else:
    #                data[appSchemaDict[fieldID]['name']]=self.getInt(queryByteArray, curBitPos, range)
    #                curBitPos += range
    #            data['schemaName']=appDict['schemas'][sid]['name']
    #    return data
    #===========================================================================
    
    def encodeFetchResult(self,resultList,appDict,formDict):
        num=0
        formTableDict=formDict['schemas']
        print formTableDict
        finalArray=array.array('B')
        for result in resultList:
            rId,size=0,0
            print result
            for sid in formTableDict.iterkeys():
                appSchemaDict=appDict['schemas'][sid]
                tableList=formTableDict[sid]['fetch']
                newList=[]
                print tableList
                for fieldID in tableList:
                    print fieldID
                    print result[rId]
                    ranges=int(appSchemaDict[fieldID]['range'])
                    if ranges==Defines.DATE_FIELD_RANGE : 
                        ranges=16 # date
                        size += ranges
                        newList.append([ranges,result[rId]])
                        rId+=1
                    elif ranges==Defines.STR_FIELD_RANGE: # str
                        size+=8+8*len(result[rId])
                        newList.append([ranges,result[rId]])
                        rId+=1
                    elif ranges==Defines.MC_FIELD_RANGE:
                        ranges=len(appSchemaDict[fieldID]['choice'])
                        size+=ranges
                        newList.append([ranges,result[rId]])
                        rId+=1
                    elif ranges==Defines.SC_FIELD_RANGE:
                        ranges=int(math.ceil(math.log(len(appSchemaDict[fieldID]['choice']),2)))
                        size += ranges
                        newList.append([ranges,result[rId]])
                        rId+=1
                    else:
                        size += ranges
                        newList.append([ranges,result[rId]])
                        rId+=1
                    print newList        
            byteList=[]
            if size%8:
                s=(size/8)+1
                for i in range(s):
                    byteList.append(0)
            else:
                s=size/8
                for i in range(s):
                    byteList.append(0)
            size=0
            retArray=array.array('B',byteList)
            for wList in newList:
                num+=1
                if (wList[0]==Defines.STR_FIELD_RANGE):
                    retArray=self.setBits(retArray, size, 8,len(wList[1]))
                    size+=8
                    strAry=array.array('B',wList[1])
                    for ch in strAry:
                        retArray=self.setBits(retArray, size, 8, ch)
                        size+=8
                else:
                    retArray=self.setBits(retArray, size,wList[0],wList[1])
                    size+=wList[0]
            #print retArray
            finalArray.extend(retArray)
            #print len(finalArray)
        print finalArray
        print num
        mask=0x000000FF
        finalArray.insert(0,num & mask)
        finalArray.insert(0,(num>>8) & mask)
        finalArray.insert(0,(num>>16) & mask)
        finalArray.insert(0,(num>>24) & mask)
        return finalArray
            
    #===========================================================================
    # def encodeFetchCommonResult(self,resultList,appDict,formDict):
    #    size=0
    #    rId=0
    #    num=0
    #    formTableDict=formDict['schemas']
    #    #print formTableDict
    #    #{u'0': {'fields': [u'0'], 'common': [u'3', u'4', u'5', u'6', u'7', u'8']}}
    #    finalArray=array.array('B')
    #    for result in resultList:
    #        for sid in formTableDict.iterkeys():
    #            appSchemaDict=appDict['schemas'][sid]
    #            tableList=formTableDict[sid]['common']
    #            newList=[]
    #            #===============================================================
    #            # print tableList
    #            # [u'3', u'4', u'5', u'6', u'7', u'8']
    #            #===============================================================
    #            for fieldID in tableList:
    #                print fieldID
    #                print result[rId]
    #                ranges=int(appSchemaDict[fieldID]['range'])
    #                if ranges==Defines.DATE_FIELD_RANGE : 
    #                    ranges=16 # date
    #                    size += ranges
    #                    newList.append([ranges,result[rId]])
    #                    rId+=1
    #                elif ranges==Defines.STR_FIELD_RANGE: # str
    #                    size+=8+8*len(result[rId])
    #                    newList.append([ranges,result[rId]])
    #                    rId+=1
    #                elif ranges==Defines.MC_FIELD_RANGE:
    #                    ranges=len(appSchemaDict[fieldID]['choice'])
    #                    size+=ranges
    #                    for i in range(ranges):
    #                        newList.append([1,result[rId]])
    #                        rId+=1
    #                elif ranges==Defines.SC_FIELD_RANGE:
    #                    ranges=len(appSchemaDict[fieldID]['choice'])
    #                    size += ranges
    #                    for i in range(ranges):
    #                        newList.append([1,result[rId]])
    #                        rId+=1
    #                else:
    #                    size += ranges
    #                    newList.append([ranges,result[rId]])
    #                    rId+=1
    #                #===========================================================
    #                # print newList
    #                # [[1, 1L], [1, 0L], [1, 0L], [0, 'J'], [1, 1L], [1, 0L], [16, 10L], [7, 10L], [15, 10L]]        
    #                #===========================================================
    #        byteList=[]
    #        if size%8:
    #            s=(size/8)+1
    #            for i in range(s):
    #                byteList.append(0)
    #        else:
    #            s=size/8
    #            for i in range(s):
    #                byteList.append(0)
    #        size=0
    #        retArray=array.array('B',byteList)
    #        for wList in newList:
    #            num+=1
    #            if (wList[0]==Defines.STR_FIELD_RANGE):
    #                retArray=self.setBits(retArray, size, 8,len(wList[1]))
    #                size+=8
    #                strAry=array.array('B',wList[1])
    #                for ch in strAry:
    #                    retArray=self.setBits(retArray, size, 8, ch)
    #                    size+=8
    #            else:
    #                retArray=self.setBits(retArray, size,wList[0],wList[1])
    #                size+=wList[0]
    #        #print retArray
    #        finalArray.extend(retArray)
    #        #print len(finalArray)
    #        print finalArray
    #        print num
    #        mask=0x000000FF
    #        finalArray.insert(0,num & mask)
    #        finalArray.insert(0,(num>>8) & mask)
    #        finalArray.insert(0,(num>>16) & mask)
    #        finalArray.insert(0,(num>>24) & mask)
    #    return finalArray
    #===========================================================================

    def getInt(self,queryByteArray,curBitPos,lenBits):
        # Length of PID is 17 bits
        # means the first two bytes plus the first bits of third byte
        startBitPos=curBitPos%8
        curBytePos=curBitPos/8
        if curBitPos == 0: curBytePos =0 
        pid,lenOfWorkingBytes,curWorkingBits=0,0,0
        lenOfWorkingBytes=(startBitPos+lenBits)/8+1
        # Get require bytes
        workingByteArray=queryByteArray[curBytePos:curBytePos+lenOfWorkingBytes]
        #print workingByteArray
        for curByteAry in workingByteArray :
            mask=0x80
            while curWorkingBits < lenBits:
                if startBitPos !=0:
                    startBitPos -= 1
                elif curByteAry & mask: 
                    pid+=1
                    pid<<=1
                    curWorkingBits+=1
                else :
                    curWorkingBits+=1
                    pid<<=1
                mask >>= 1
                if mask==0 : break
                #print pid
        return pid>>1    

    def setBits(self,retArray,curBitPos,lenBits,val):
        valList=self.getValList(val,lenBits)
        #print valList
        for v in valList:
            #if v : print v
            startBitPos=curBitPos%8
            curBytePos=curBitPos/8
            mask=0x1
            #// adjust the mask.
            mask <<= (7 - startBitPos)
            if v == '1':
                #// set the bit at byteNum/offset
                retArray[curBytePos]=retArray[curBytePos] | mask
                #print retArray
            else:
                #// clear the bit at byteNum/offset
                retArray[curBytePos]=retArray[curBytePos] & (~mask)
            #// increment the location pointer
            curBitPos +=1
        #print retArray
        return retArray

    def getTotalSizeBit(self,newList):
        size=0
        return size

    def getValList(self,val,lenBits):
        retList=[]
        tmp=bin(val)
        tmp=tmp.lstrip('0b')
        kk=array.array('c',tmp)
        for i in range(len(kk)):
            retList.append(kk[i])
        #print retList
        while len(retList) != lenBits:retList.insert(0, '0')
        #print retList
        return retList
