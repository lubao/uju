# possible packet types. from client to Server
# 1. session packet
# 2. ACK packet
SESSION_PACKET  =  1
ACK_PACKET  =  2
# types --- server to the client
RESPONSE_PACKET  =  3
NACK_PACKET  =  4
SMS_SIZE  =  130 
# If Size is made 140 then 
# it sends 2 SMS. Why? So we figured out that
# the limit is actually 133. Lets keep it 130 then
FIELD_STR_SIZE  =  128
FIELD_DATE_SIZE  =  2
MS_PER_DAY  =  1000 * 60 * 60 * 24

STR_FIELD_RANGE  =  0
DATE_FIELD_RANGE =  -1
MC_FIELD_RANGE =  -2
SC_FIELD_RANGE =  -3

FIELD_TYPE_INT  =  0
FIELD_TYPE_STR  =  1
FIELD_TYPE_DATE  =  2
FIELD_TYPE_MULTIPLECHOICE  =  3
FIELD_TYPE_SINGLECHOICE  =  4

OP_CREATE_ID  =  0
OP_UPDATE_ID  =  1
OP_DESTROY_ID  =  2
OP_SEARCH_ID  =  3
OP_ADV_SEARCH_ID  =  4

JUST_MESSAGE_RESPONSE  =  0
RESULT_RESPONSE  =  1

FETCH_ALL  =  0
FETCH_COMMON  =  1
FETCH_CUSTOME = 2

LASTSESSION = 9999

SESSION_INIT = 0
SESSION_COLLECT = 1
SESSION_DONE = 2
SESSION_FINISH = 3
SESSION_DROP = 4

BEFORE = 0
AFTER = 1
RELIABLE_HEADER_OFFSET = 4
# in seconds
SESSION_SLEEP_TIME = 9999999999

# Prefix of the path configuration file
PATHPREFIX = 'Apps'
