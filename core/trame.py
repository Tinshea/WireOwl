import source as src
taille_trame = 28  #14 octets donc 28 quartets
mac_adress_source = dict()
mac_adress_distination = dict()
dicoipver = dict()
typethernet ={"0800":"IPV4","0805":"X.25 niveau 3","0806":"ARP","8035":"RARP","8098":"Appletalk","86dd":"IPV6"}
def tramecalcul(trames):
    dicoipver.clear()
    mac_adress_distination.clear()
    mac_adress_source.clear()
    list_paquet = []
    try :
        i = 0
        for i in range(src.nbtrames):
            with open("./Trames/Trame"+str(i+1)+".txt",'w') as fichier : 

                message = trames[i]
                if message == '' :
                    list_paquet.append('')
                    
                else :
                    trame = ""
                    trame = message[0:taille_trame]
                    fichier.write("Mac_adress_destination : " + trame[0:12] + '\n') #6 premiers octets pour l'adresse mac destination
                    mac_adress_distination[i+1] = trame[0:12]
                    fichier.write("Mac_adress_source : " + trame[12:24] + '\n')  #6 octets suivant pour l'adresse mac source
                    mac_adress_source[i+1] = trame[12:24]
                    ipversion = trame[24:taille_trame] #2octets    
                    
                    if ipversion in typethernet : 
                        if ( ipversion == "0800" ) :
                            fichier.write("Type : IPV4\n")
                            list_paquet.append(message[taille_trame:])
                            dicoipver[i+1] = "IPV4"
                        else : 
                            fichier.write("Erreur : désoler votre trame ne respecte pas les types que notre programme peut suporter :"+typethernet.get(ipversion)) 
                            list_paquet.append('')
                            dicoipver[i+1] = typethernet.get(ipversion) 
                            fichier.close()
                        
                    fichier.close() 
    except ImportError: #gestion des erreurs
        dicoipver[i+1] = "Unknown"
        list_paquet.append('')
    return list_paquet





       


        

        


       
    