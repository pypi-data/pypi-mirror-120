
import mysql.connector
from mysql.connector import Error
import sys

def getAnbar():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect( host="bookine.ir",
                                        user='doolsaz',
                                        password='22111357',)
        if conn.is_connected():
            print('Connected to MySQL database')
            # conn.escape_string()
            return conn

    except Error as e:
        print(e)



def exec(stmt):
    conn = getAnbar()
    mc = conn.cursor(buffered=True)
    recs=""
    try:
        mc.execute(stmt)
        conn.commit()
        recs=mc.fetchall()
        print(recs)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            #print(agahi)
    mc.close()
    conn.close()
    recs=str(recs)
    return recs



###
#Bama Anbar Tools

# def putBamaGahi(ins):
#     pass
#     rose:{
#  # :'AutoDealer'
#   'بدنه' :'BodyWork',
#  # :
# 'داخل' :'ColorIn',
#  # :
# 'رنگ':'ColorOut',
#  'گیربکس': 'GearBox',
#  # 'Mahaleh'
#  # 'MashinSazi'
#  'كاركرد': 'Milage ',
#  # 'Model '         :
# 'سوخت': 'Sookht'          :
#  # 'Tel'             :
#  'توضیج':'desc'
#      }
#  #    for keys in in:
