import MySQLdb
import DBconf
class SQLEng():
    
    def exeSQL(self,SQL):
        try:
            conn=MySQLdb.connect(host = DBconf.DB_HOST,
                                 user = DBconf.DB_USER,
                                 passwd = DBconf.DB_PASSWORD,
                                 )
            cursor=conn.cursor()
            cursor.execute(SQL)
            ret=cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
            return ret
        except MySQLdb.Error ,e:
            #ret="Error %d: %s".format(e.args[0],e.args[1])
            return False
    
    def getMsg(self,id):
        SQL="""
            SELECT `Text` , `SenderNumber` , `UDH`
            FROM `smsd`.`inbox`
            WHERE ID ={0}
            """.format(id)
        return self.exeSQL(SQL)
            
    def getAppPath(self,id):
        SQL="""
            SELECT `path`
            FROM `AppInfo`.`Info`
            WHERE `id` ={0}
            """.format(id)
        return self.exeSQL(SQL)
            
    def getFormPath(self,aid,fid):
        SQL="""
            SELECT `path`
            FROM `FormInfo`.`Info`
            WHERE `aid` ={0} and `fid`={1}
            """.format(aid,fid)
        return self.exeSQL(SQL)
        
    def getInsertSQL(self,d):
        schema=d.pop('schemaName')
        db=d.pop('dbName')
        sqlCol,sqlVal,update="","",""
        for col in d.iterkeys():
            sqlCol +="`{0}`,".format(col)
            val=str(d.get(col))
            if val.isdigit():
                sqlVal +="{0},".format(val)
            else:
                sqlVal +="'{0}',".format(val)
                val="'{0}'".format(val)
            if col!="Patient ID": # It is the Primary Key
                update += "{0}={1},".format("`{0}`".format(col),val)
        sqlCol=sqlCol.rstrip(',')
        sqlVal=sqlVal.rstrip(',')
        update=update.rstrip(',')
        sql="INSERT INTO `{4}`.`{0}` ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE {3} ".format(schema,sqlCol,sqlVal,update,db)
        return sql
    
    def getSearchSQL(self,d,fetchList):
        order='''ORDER BY `Time` DESC LIMIT 0 , 10'''
        schema=d.pop('schemaName')
        db=d.pop('dbName')
        fetch=""
        for field in fetchList:
            fetch += "`{0}`,".format(field)
        fetch=fetch.rstrip(',')    
        for (k,v) in d.iteritems():
            constrain="`{0}`={1}".format(k,v)
        sql="SELECT {3} FROM `{2}`.`{0}` WHERE {1} {4}".format(schema,constrain,db,fetch,order)
        return sql
    
    def getDestroySQL(self,d):
        schema=d.pop('schemaName')
        db=d.pop('dbName')
        for (k,v) in d.iteritems():
            constrain="`{0}`={1}".format(k,v)
        sql="DELETE FROM `{2}`.`{0}` WHERE {1}".format(schema,constrain,db)
        return sql
    
    def getInsetSentBox(self,to,mesg):
        return '''
            INSERT INTO `smsd`.`outbox` (
            `UpdatedInDB` ,
            `InsertIntoDB` ,
            `SendingDateTime` ,
            `Text` ,
            `DestinationNumber` ,
            `Coding` ,
            `UDH` ,
            `Class` ,
            `TextDecoded` ,
            `ID` ,
            `MultiPart` ,
            `RelativeValidity` ,
            `SenderID` ,
            `SendingTimeOut` ,
            `DeliveryReport` ,
            `CreatorID`
            )
            VALUES (
            CURRENT_TIMESTAMP , 
            '0000-00-00 00:00:00', 
            '0000-00-00 00:00:00', 
            '{0}', '{1}', '8bit', '060504DF8B0000', 
            '-1', '', NULL , 'false', '-1', NULL , 
            '0000-00-00 00:00:00', 'default', ''
            )'''.format(mesg,to)
