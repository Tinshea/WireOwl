import tkinter as tk
import trame,paquetip,tcp,httpmodule
import source as src
import sqlite3 as sql

#Dans cette version il faut mettre la liste condition en paramètre et la liste retournée est la liste de résultats filtrés
def database_from_trame(dbft):
    cursor = dbft.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ipdb(num_trame INTEGER, protocol TEXT, ipsrc TEXT, ipaddr TEXT)")
    dbft.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS trame(num_trame INTEGER, ethsrc TEXT, ethaddr TEXT)")
    dbft.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS tcpdb(num_trame INTEGER, tcpsrc TEXT, tcpaddr TEXT)")
    dbft.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS httpdb(num_trame INTEGER, httpversion TEXT)")
    dbft.commit()
    for i in range(src.nbtrames):
        i += 1
        if (((paquetip.Source_Address).get(i) is not None) and ((paquetip.Destination_Address).get(i) is not None)):
            cursor.execute("""
            INSERT INTO ipdb(num_trame, protocol, ipsrc, ipaddr) VALUES (?,?,?,?)""",(i, (paquetip.Protocol).get(i), (paquetip.Source_Address).get(i), (paquetip.Destination_Address).get(i))
            )
        if(((trame.mac_adress_source).get(i) is not None) and ((trame.mac_adress_distination).get(i) is not None)):
            cursor.execute("""
            INSERT INTO trame(num_trame, ethsrc, ethaddr) VALUES (?,?,?)""",(i, (trame.mac_adress_source).get(i), (trame.mac_adress_distination).get(i))
            )
        if(((tcp.Port_Source).get(i) is not None) and ((tcp.Port_destination).get(i) is not None)):
            cursor.execute("""
            INSERT INTO tcpdb(num_trame, tcpsrc, tcpaddr) VALUES (?,?,?)""",(i, (tcp.Port_Source).get(i), (tcp.Port_destination).get(i))
            )
        if(((httpmodule.versiondic).get(i) is not None)):
            cursor.execute("""
            INSERT INTO httpdb(num_trame, httpversion) VALUES (?,?)""",(i, (httpmodule.versiondic).get(i))
            )
        
    return dbft

def filtre(condition):
    try :
        if len(condition)>=3:
            len_con = len(condition)
            temp = condition[0]
            temp = temp.replace('.','')
            temp1 = condition[1]
            temp2 = condition[2]
            requete = 'SELECT * FROM '
            if (temp.lower() == 'ipsrc' or temp.lower() == 'ipaddr'):
                requete = requete + 'ipdb'
                listip = temp2.split('.')
                for eight_bit in listip:
                    try :
                        if ((int(eight_bit) < 0) or (int(eight_bit) >255)):
                            return "echec"
                    except :
                        return "echec"
            try :             
                if (temp.lower() == 'protocol'):
                    requete = requete + 'ipdb'
            except :
                return "echec"
            try :
                if (temp.lower() == 'tcpsrc' or temp.lower() == 'tcpaddr'):
                    requete = requete + 'tcpdb'
                    port = int(temp2)
                    if ((port < 0) or (port > 65535)):
                        return "echec"
            except : 
                return "echec "
            try :
                if (temp.lower() == 'ethsrc' or temp.lower() == 'ethaddr'):
                    requete = requete + 'trame'
            except :
                return "echec"
            try :
                if (temp.lower() == 'httpversion'):
                    requete = requete + 'httpdb'
            except : 
                return "echec"

            try : 
                if (temp.lower() != 'ipsrc' and temp.lower() != 'ipaddr' and temp.lower() != 'protocol' and temp.lower() != 'tcpsrc' and temp.lower() != 'tcpaddr' and temp.lower() != 'ethsrc' and temp.lower() != 'ethaddr' and temp.lower() != 'httpversion'):
                    return "echec"
            except : 
                return "echec"
            requete = requete + ' WHERE '
            if (temp1 == '=='):
                requete = requete + temp + ' = ' + "('"+temp2+"')"
            if (temp1 == '!='):
                requete = requete + temp + ' != ' + "('"+temp2+"')"
            while(len_con > 3):
                if((condition[3].lower() == 'and') or (condition[3] == '&&')):
                    requete = requete + ' AND ('
                if((condition[3].lower() == 'or') or (condition[3] == '||')):
                    requete = requete + ' OR ('
                condition = condition[4:len(condition)]
                temp = condition[0]
                temp = temp.replace('.','')
                temp1 = condition[1]
                temp2 = condition[2]
                if (temp.lower() == 'ipsrc' or temp.lower() == 'ipaddr'):
                    listip = temp2.split('.')
                    for eight_bit in listip:
                        try:
                            if ((int(eight_bit) < 0) or (int(eight_bit) >255)):
                                return "echec"
                        except :
                            return "echec"
                            
                if (temp.lower() == 'tcpsrc' or temp.lower() == 'tcpaddr'):
                    try :
                        port = int(temp2)
                        if ((port < 0) or (port > 65535)):
                            return "echec"
                    except :
                        return "echec"
                        
                requete = requete + temp.lower()
                if (temp1 == '=='):
                    requete = requete + ' = ' + "'"+temp2+"')"
                if (temp1 == '!='):
                    requete = requete + ' != ' + "'"+temp2+"')"
                len_con = len(condition)
            global dbft
            dbft = sql.connect('./trames/ma_base.db') #Crée une base de donnée en mémoire, mettre db.close() quand on en aura plus besoin
            database_from_trame(dbft)
            cursor = dbft.cursor()
            cursor.execute(requete)
            return cursor  
        return "echec"
    except : 
        return "echec"