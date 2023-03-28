import paquetip as paquip
import source as sr
#from itertools import cycle


#port_source            #16 bits -> 4 quartets
#port_distination       #16 bits -> 4 quartets     
#num_sequence           #32 bits -> 8 quartets
#num_ack                #32 bits -> 8 quartets
#header_length          #4 bits  -> 1 quartet
#reserved               #6 bitsEn tout 3 quartets (reserved + flags) 
#URG                    #1 bit En tout 3 quartets (reserved + flags) 
#ACK                    #1 bit En tout 3 quartets (reserved + flags) 
#PSH                    #1 bit En tout 3 quartets (reserved + flags) 
#RST                    #1 bit En tout 3 quartets (reserved + flags) 
#SYN                    #1 bit En tout 3 quartets (reserved + flags) 
#FIN                    #1 bit En tout 3 quartets (reserved + flags) 
#window                 #16 bits
#checksum               #16 bits
#urgent_pointer         #16 bits
#options_and_padding    #32 bits
#data
Port_Source = dict()
Port_destination = dict()
flagdic = dict()
Windowdic = dict()
lenght = dict()
secdico = dict()
ackdico = dict()
headerlength = dict()
dicocheksum = dict()
dicoheaderlength = dict()
dicourgentpoint = dict()
list_segment = []

def tcp_flag_id(quartetstring,j):
    # Après des recherches sur internet et du rendu wireshark, on a remarqué qu'il
    #en existait d'autre mais nous avons choisis de nous en tenir à ceux présentés 
    #dans le cours
    #Traduit les quartets en un string de bits
    binstring = bin(int(quartetstring, 16))[2:].zfill(12)
    i = 0
    listflag=[]
    reserved = ''
    for bit in binstring:
        if i < 6:
            reserved = reserved + bit
        elif i == 6:
            if int(bit) == 1:
                urg = 'urg set'
                listflag.append("URG")
            else:
                urg = 'urg not set'
        elif i == 7:
            if int(bit) == 1:
                ack = 'ack set'
                listflag.append("ACK")
            else:
                ack = 'ack not set'
        elif i == 8:
            if int(bit) == 1:
                psh = 'psh set'
                listflag.append("PSH")
            else:
                psh = 'psh not set'
        elif i == 9:
            if int(bit) == 1:
                rst = 'rst set'
                listflag.append("RST")
            else:
                rst = 'rst not set'
        elif i == 10:
            if int(bit) == 1:
                syn = 'syn set'
                listflag.append("SYN")
            else:
                syn = 'syn not set'
        elif i == 11:
            if int(bit) == 1:
                fin = 'fin set'
                listflag.append("SET")
            else:
                fin = 'fin not set'
        i = i + 1
    res = ('Reserved : ' + reserved + '\n' + urg+  '\n' + ack + '\n' + psh + '\n' + rst + '\n' + syn + '\n' + fin + '\n')
    flagdic[j] = listflag
    return res



def tcpaquet(trames):
    list_segment = []
    Port_Source.clear()
    Port_destination.clear()
    flagdic.clear()
    Windowdic.clear()
    lenght.clear()
    secdico.clear()
    ackdico.clear()
    dicocheksum.clear()
    dicoheaderlength.clear()  
    dicourgentpoint.clear()
    for j in range(len(trames)) :
        #initialisation de variable
        trame = trames[j] 
        #si trame invalide on met '' pour tout les if/elif
        if ((trame == '') ):
            list_segment.append('')
        elif ((paquip.Protocol).get(j+1) != 6) :
            list_segment.append('')

        #verification de la taille des paquet et de leurs cohérence
        elif ((len(trame)<40) or ((int(trame[24] , 16) * 8) < 40) or (len(trame) < (int(trame[24] , 16) * 8))):
            list_segment.append('')
            with open("./Trames/Trame"+str(j+1)+".txt",'a') as fichier :
                fichier.write("La trame "+str(j+1)+" à une taille incoherente au niveau Tcp")
                fichier.close()
        #Renvoie un string à print dans le fichier texte

        else :
            with open("./Trames/Trame"+str(j+1)+".txt",'a') as fichier :
                hl = (int(trame[24] , 16) * 8)
                lenght[j+1] = int(hl/2) - 20
                #on prepare la liste des fragment
                list_segment.append(trame[hl:])
                i = 0
                opcpt = 1
                tmp = ''
                trameTCP = 'Port source: '
                src = ''
                dest = ''
                sn = ''
                ack = ''
                resflag = ''
                window_hex_to_dec = ''
                checksum = ''
                urgp = ''
                thl = str(int(trame[24],16))
                liste_op = [] 
                for i in (range(40)):
                    if (i < 4):
                        src = src + trame[i]
                    if (i >= 4) and (i <= 7):
                        dest = dest + trame[i]
                    if (i > 7) and (i <= 15):
                        sn = sn + trame[i]
                    if (i > 15) and (i <= 23):
                        ack = ack + trame[i]
                    if (i > 24) and (i <= 27):
                        resflag = resflag + trame[i]
                    if (i > 27) and (i <= 31):
                        window_hex_to_dec = window_hex_to_dec + trame[i]
                    if (i > 31) and (i <= 35):
                        checksum = checksum + trame[i]
                    if (i > 35) and (i <= 40):
                        urgp = urgp + trame[i]
                
                #Gestion des options
                op = trame[40:]
                for opcpt in range(hl - 39):
                    tmp = tmp + trame[i + opcpt]
                    if (opcpt % 2 == 0):
                        liste_op.append(tmp)
                        tmp = ''
                liste_op = liste_op[1::1]

                cpt = 0
                cpt2 = 0
                eol = 'TCP Option - End Of Options (EOL)\n'
                nop = 'TCP Option - No Operation (NOP)\n'
                mss = ''
                wscale = ''
                ts = ''
                opt_val = '' 
                opt = ''
                for cpt in range(len(liste_op)):
                #while (cpt < len(liste_op)):
                    a = liste_op[cpt]
                    if (a == '00'):
                        opt = opt + eol
                        break
                    if (a == '01'):
                        opt = opt + '\n' + nop
                    if (a == '02'):
                        cpt2 = cpt + 2
                        if ((cpt + 1) == len(liste_op)):
                            break
                        b = liste_op[cpt+1]
                        opt_val = '' 
                        mss = 'TCP Option - Maximum Segment Size (MSS):\nSize: ' + str(int(b,16)) +'\nOption Value: '
                        for cpt2 in range(int(b[1]) + cpt):
                            opt_val = opt_val + liste_op[cpt2]
                        opt_val = opt_val[4::]
                        cpt = cpt2
                        mss = mss + str(int(opt_val,16)) 
                        opt = opt + mss
                        mss = ''
                    if (a == '03'):
                        cpt2 = cpt + 2
                        if ((cpt + 1) == len(liste_op)):
                            break
                        b = liste_op[cpt+1]
                        opt_val = '' 
                        wscale = 'TCP Option - Window Scale (WScale):\nSize: ' + str(int(b,16)) +'\nOption Value: '
                        for cpt2 in range(2 + cpt):
                            opt_val = opt_val + liste_op[cpt2]
                        cpt = cpt2
                        opt_val = opt_val[4::]
                        wscale = wscale + str(int(opt_val,16)) 
                        opt = opt + wscale
                        wscale = ''
                    if (a == '08'):
                        cpt2 = cpt + 2
                        if ((cpt + 1) == len(liste_op)):    
                            break
                        b = liste_op[cpt+1]
                        opt_val = '' 
                        ts = 'TCP Option - TimeStamp (TS):\nSize: ' + str(int(b,16)) +'\nOption Value: '
                        for cpt2 in range(int(b[1],16) + cpt):
                            opt_val = opt_val + liste_op[cpt2]
                        cpt = cpt2
                        opt_val = opt_val[4::]
                        ts = ts + str(int(opt_val,16)) 
                        opt = opt + ts
                        ts = ''
                    if (a not in ['00','01','02','03','08']):
                        continue
                        cpt2 = cpt + 2
                        if ((cpt + 1) == len(liste_op)):
                            break
                        b = liste_op[cpt+1]
                        opt = opt + '\nOption non prise en charge: ' + b
                        for cpt2 in range(len(b[1]) - 2):
                            opt = opt + liste_op[cpt + cpt2]
                        continue
                    #cpt = cpt + 1

                Port_Source[j+1]= str(int(src,16))
                Port_destination[j+1] = str(int(dest,16))
                Windowdic[j+1] = str(int(window_hex_to_dec,16))
                secdico[j+1] = str(int(sn,16))
                ackdico[j+1] =str(int(ack,16))  
                dicocheksum[j+1] = checksum
                dicoheaderlength[j+1] = thl
                dicourgentpoint[j+1]= str(int(urgp,16))
                trameTCP = trameTCP + str(int(src,16)) + '\nPort destination: ' + str(int(dest,16)) + '\nSequence Number: ' + str(int(sn,16)) + '\nAcknowledment Number: ' + str(int(ack,16)) + '\nTransport Header Length: ' + thl + '\n' + tcp_flag_id(resflag,j+1) + '\nWindow: ' + str(int(window_hex_to_dec,16)) + '\nChecksum: ' + checksum + '\nUrgent Pointer: ' + str(int(urgp,16)) + '\n' + opt
                fichier.write(trameTCP)
                fichier.close()
    return list_segment 

           


            




    
