
import source as src
header_length = dict()
tos = dict()
total_length = dict()
Identification = dict()
Reserved = dict()
DF = dict()
MF = dict()
Fragment_offsetdic = dict()
Time_to_live = dict()
Protocol = dict()
Header_checksum = dict()
Source_Address = dict()
Destination_Address = dict()
dico_protocol = {1:"ICMP",2:"IGMP",6:"TCP",8:"EGP",9:"IGP",17:"UDP",36:"XTP",46:"RSVP"}
my_global_listip = []


def paquetipv4(paquets):
    Protocol.clear()
    header_length.clear()
    tos.clear() 
    total_length.clear() 
    Identification.clear() 
    Reserved.clear() 
    DF.clear()
    MF.clear() 
    Fragment_offsetdic.clear() 
    Time_to_live.clear() 
    Header_checksum.clear() 
    Source_Address.clear() 
    Destination_Address.clear() 
    my_global_listip.clear() 
    list_segment = []
    for i in range(len(paquets)) :
        #initialisation de variable
        paquet = ""
        paquet=paquets[i] 
        #si trame invalide on met '' pour tout les if/elif
        if paquet == '':
            list_segment.append('')

        #verification de la taille des paquet et de leurs cohérence
        elif ((len(paquet)<40) or ((int(paquet[1] ,16) * 4) * 2 <40)):
            list_segment.append('')
            with open("./Trames/Trame"+str(i+1)+".txt",'a') as fichier :
                fichier.write("La trame "+str(i+1)+" à une taille incoherente")
                fichier.close()

        #on reverifie le type ip
        elif (paquet[0] != '4'):
            with open("./Trames/Trame"+str(i+1)+".txt",'a') as fichier :
                fichier.write("Erreur : désoler mauvais type d'IP")
                fichier.close()
            list_segment.append('')

        else: 
            #calcul de la taille du paquet pour les vérifications : 
            taille_paquet = (int(paquet[1] ,16) * 4) * 2 #pour avoir la taille en quartet(20 octets pour en tete + option = taille_paquet-20)
            with open("./Trames/Trame"+str(i+1)+".txt",'a') as fichier :
                
                #initialisation de donnée utile au programme
                paquetip = ''
                paquetip = paquet[0:taille_paquet]

                #ecriture en fichier et mise dans le dico de la taille
                hl = int(taille_paquet / 2)
                fichier.write("Header_Length:" + str(hl) + " octets " + "(" + paquet[1]+")\n")
                header_length[i+1] = hl

                #on prepare la liste des fragment
                list_segment.append(paquet[taille_paquet:])

                #Type of service
                Tos = paquetip[2:4]
                fichier.write("Tos:"+ str(Tos)+"\n")
                tos[i+1] = Tos

                #Total length
                Tl = int(paquetip[4:8],16)
                fichier.write("Total length_:" + str(Tl)+"\n")
                total_length[i+1] = Tl
                    
                #Identifiant
                id = paquetip[8:12]
                fichier.write("Identification_:" + id + " (" + str(int(id,16)) + ")\n")
                Identification[i+1] = id 

                #FLAGS
                flag = fc_flag(paquetip)

                #Reserved
                fichier.write("Reserved_:"+str(flag[0])+"\n")
                Reserved[i+1] = str(flag[0])
                #Dont Fragment  
                fichier.write("DF_:"+str(flag[1])+"\n")
                DF[i+1] = str(flag[1])
                #More Fragment 
                fichier.write("MF_:"+str(flag[2])+"\n")
                MF[i+1] = str(flag[2])
                
                #Fragment offset
                fragmentoffset =fc_fragmentoffset(paquetip)
                fichier.write("Fragment_offset_: "+str(int(fragmentoffset,2))+' = 0b'+fragmentoffset+' \n')
                Fragment_offsetdic[i+1] = str(int(fragmentoffset,2))+' = 0b'+fragmentoffset+' \n'
                #TTL
                fichier.write("Time_to_live_: "+str(int(paquetip[16:18],16))+"\n")
                Time_to_live[i+1] = str(int(paquetip[16:18],16))
                #Protocol

                Proto = int(paquetip[18:20],16)
                fichier.write("Protocol_:" + str(Proto)+"\n")
                Protocol[i+1] = Proto

                #Header checksum
                hc = paquetip[20:24]
                Header_checksum [i+1] = hc
                fichier.write("Header_checksum_:0x" + str(hc)+"\n")
                
                #Source Adress
                ipsource = ip_address(paquetip[24:32])
                
                fichier.write("Source_Address_: " + ipsource+"\n")
                my_global_listip.append(ipsource)
                Source_Address[i+1] = ipsource
                

                #Destination Adress
                ipdes = ip_address(paquetip[32:40])
                fichier.write("Destination_Address_: " + ipdes +"\n")
                Destination_Address[i+1] = ipdes
                my_global_listip.append(ipdes)

                
                #Fermeture du fichier
                fichier.close()
    return list_segment


def fc_flag(tab):
    #convertion en binaire 
    flag = bin(int(tab[12],16)) [2::]
    #on complete les bits de poids fort a 0 pour avoir 4 bits
    flag=flag.zfill(4)
    flag = flag[:-1]
    return flag 


def fc_fragmentoffset(tab):
    #convertion en binaire 
    fragmentoffset=bin(int(tab[12:16],16)) [2::]
    fragmentoffset=fragmentoffset.zfill(16)
    fragmentoffset=fragmentoffset[3::]
    return fragmentoffset


def ip_address(package) :
    ip_address =""
    i=0
    #met un .  et on prend chauque octet convertit en decimal sur 4 octets
    while i < 8 :
       ip_address+="."+str(int(package[i:i+2],16))
       i+=2
    #on supprime le premier point
    return ip_address[1:]
        

        