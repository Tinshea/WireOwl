import source as src
httpsample = dict()
versiondic = dict()
def is_meth(str_quartets):
    
    return (str_quartets in ['GET','HEAD','POST','PUT','DELETE','CONNECT','OPTIONS','TRACE','PATCH'])


def req_or_rep(trames):
    trame = ""
    httpsample.clear()
    for j in range(src.nbtrames):
        try :
            final :str  = ""
            trame = trames[j]
            if trame == '' :
                pass
            else :
                with open("./Trames/Trame"+str(j+1)+".txt",'a') as fichier :
                    if trame == "":
                        final = "http corrumpu ou absent"
                        fichier.write(final)
                        httpsample[j+1] = final
                    else : 
                        method_or_version = []
                        count = 0
                        tmpc = 0
                        tmp = trame[0] + trame[1]
                        method_or_version.append(tmp)
                        tmp = ''
                        while count < len(trame):
                            tmp = tmp + trame[count]
                            if (tmp == '20'):
                                count = count + 1
                                break
                            tmpc = tmpc + 1
                            if (tmpc == 2):#Si apres 2 caracteres parcourus, la chaine n est pas '20' alors ce n est pas la fin de ce champ
                                method_or_version.append(tmp)
                                tmp = ''
                                tmpc = 0
                            count = count + 1
                        #Tests pour savoir si c'est une requête HTTP OU une réponse HTTP
                        method_or_version = method_or_version[1::1]
                        test_meth = ''
                        for e in method_or_version:
                            test_meth = test_meth + e
                        try :
                            test_meth = bytes.fromhex(test_meth).decode()
                        except UnicodeDecodeError : 
                            final = "http corrumpu ou absent"
                            fichier.write(final)
                            httpsample[j+1] = final
                            break
                        #On verifie si c'est une requete ou une reponse
                        a = is_meth(test_meth)
                        
                        #lecture de l'url ou du code status
                        tmp = ''
                        url = ''
                        code_status = ''
                        tmpc = 0
                        while (count < len(trame)):
                            tmp = tmp + trame[count]
                            if (tmp == '20'):
                                count = count + 1
                                break
                            tmpc = tmpc + 1
                            if (tmpc == 2):#Si apres 2 caracteres parcourus, la chaine n est pas '20' alors ce n est pas la fin de ce champ
                                url = url +tmp
                                tmp = ''
                                tmpc = 0
                            count = count + 1

                        #lecture de la Request Version ou du message
                        tmp = ''
                        message = ''
                        version = ''
                        tmpc = 0
                        while (count < len(trame)):
                            tmp = tmp + trame[count]
                            if (tmp == '0d0a'):
                                count = count + 1
                                break
                            tmpc = tmpc + 1
                            if (tmpc == 4):#Si apres 4 caracteres parcourus, la chaine n est pas '0d0a' alors ce n est pas la fin de ce champ
                                version = version + tmp
                                tmp = ''
                                tmpc = 0
                            count = count + 1
                        
                        #Conversion d hexadecimal en ascii pour comprendre
                        if(a):
                            final +='Analyse de la requete : \n'
                            final +='Methode: ' + test_meth + "\n"
                            url = 'URL: ' + bytes.fromhex(url).decode()+"\n"
                            versiondic[j+1] = version
                            final +=url
                            version = 'Request Version: ' + bytes.fromhex(version).decode()
                            final +=version
                        else:
                            final +='Analyse de la reponse \n'
                            final +='Version: ' + test_meth+"\n"
                            versiondic[j+1] = test_meth
                            code_status = bytes.fromhex(url).decode()
                            if(int(code_status)<100 or int(code_status)>599):
                                final +="Erreur, code statut incorrect"
                                return
                            final +='Code Status: ' + code_status +"\n"
                            message = 'Message: ' + bytes.fromhex(version).decode() + '\n'
                            final +=message
                    
                        #Reste: Nom des champ d entetes et leur valeurs
                        header_and_value_list = []
                        tmp = ''
                        tmpc = 0
                        champ_n:str = ''
                        
                        while(True):
                            while (count < len(trame)):
                                tmp = tmp + trame[count]
                                champ_n = champ_n + trame[count]
                                tmpc += 1
                                if((tmp == '0d0a')):
                                    if((count + 1) >= len(trame)):
                                        break
                                    else:
                                        champ_n.replace('0d0a','')
                                        header_and_value_list.append(bytes.fromhex(champ_n).decode())
                                        champ_n = ''
                                if (tmpc == 4):
                                    tmp = tmp[1::1]
                                    tmpc = tmpc - 1
                                count += 1
                            break
                        fichier.write(final)
                        httpsample[j+1] = final
                    fichier.close()
        except:
            continue
            