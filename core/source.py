import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog,messagebox,scrolledtext,ttk
import trame,paquetip,tcp,os,httpmodule,pdf,filtrage
import tkmacosx


#creation de fenetre Principale et peronnalisation de la fenetre
window = tk.Tk()
window.resizable(False, False)
window.title("Wire Owl")
window.geometry("1280x720")
img = tk.Image("photo", file="./affichage/wireowl_ico.gif")#pour la compatibilite des different os en prendra en gif  
window.iconphoto(True, img) 
window.config(background="#FFFFFF")
window.minsize(1280,720)
window.update()
width = window.winfo_width()     
height = window.winfo_height()
global path 
path =""

indicelistbox = 0

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def traitement(fichier):
    files=os.listdir("./Trames")
    for i in range(len(files)):
        os.remove("./Trames"+'/'+files[i])
        #ligne additionnelle si on veut supprimer le repertoire
    message :str =""
    try :
        #ouverture du fichier texte
        with open(fichier, 'r') as filin:
            lignes = filin.readlines()
            tab_result=[] #on stock ici les differentes trames du fichier 
            global nbtrames
            nbtrames = 0
            for ligne in lignes :

                if ligne[0:7] =='0000   ': #on detecte une nouvelle trame 
                    nbtrames+=1
                
                    if (message !='' and is_hex(message.replace("\n",""))): # verification de la trame (securiter)
                        tab_result.append(message.replace("\n",""))  #on rajoute le message dans le tableau (on en profite pour suprimer les \n)
                        message='' #on reniallise le message
                    elif nbtrames == 1 and message =='' :
                        pass
                    else :
                        tab_result.append('')  #on rajoute le message dans le tableau (on en profite pour suprimer les \n)
                        message='' #on reniallise le message
                tmp = ligne[7::].split("  ")
                message += tmp[0].replace(" ","")

            if (message !='' and is_hex(message.replace("\n",""))):
                tab_result.append(message.replace("\n","").lower())#on rajoute le dernier message
            if '' in tab_result :
                messagebox.showinfo("Attention","Il semblerai que certaine trame soit corrumpu ou incorrect")

    except ImportError: #gestion des erreurs
        messagebox.showerror("FileUnfound","Aucun fichier de ce nom existe")
        filin.close()
        exit()
    # gerer le cas ou liste vide a faire
    finally :
        filin.close()
                
    return tab_result
 

def exitcustom():
    if(messagebox.askyesno("Exit","Voulez-vous stopper le programme ?")):
        try :
            filtrage.dbft.close()
        except :
            pass
        window.destroy()
        try : 
            Flow_sharkw.destroy()
        except : 
            pass

def exitcustomflow():
    if(messagebox.askyesno("Exit","Voulez-vous sortir de Flow Graph ?")):
        try : 
            Flow_sharkw.destroy()
        except :
            pass

def pdfsave(): 
    if(messagebox.askyesno("sauvegarde","Voulez-vous un pdf ?")):
        pdf.lauchpdf(nbtrames)

def search():
    global path
    path = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.realpath(__file__)),title="Select A File",filetypes=(("txt files", "*.txt"),))

def launch():
    try :
        trames = traitement(path)
 
        global lentrames
        lentrames = []
        for i in range (len(trames)):
            lentrames.append(len(trames[i]))

        for widget in window.winfo_children():
            widget.pack_forget() # Si vous utilisez .pack()
        httpmodule.req_or_rep(tcp.tcpaquet(paquetip.paquetipv4(trame.tramecalcul(trames))))
        affichage()

    except UnboundLocalError: #gestion des erreurs
        messagebox.showerror("Wrong Path","Mauvais chemin veuillez donner un chemin valide")

def filtrefolistbox(event):
    listbox.delete(0,tk.END)
    if entry.get() == "" :
        entry.config(bg="#2f3542")
        for i in range(nbtrames) :
            i+=1
            ipsource =""
            ipdest = ""
            iproto = ""
            portsource = ""
            portdest = ""
            flag = ""
            windowtcp = ""
            lenght = ""
            sec = ""
            ack= ""
            #and 
            if (i in paquetip.Source_Address) :
                ipsource = paquetip.Source_Address.get(i)
                
            else :
                ipsource = "Unknown"
            
            if (i in paquetip.Destination_Address) :
                ipdest = (paquetip.Destination_Address).get(i)
                
            else :
                ipsource = "Unknown"
            
            if (i in paquetip.Protocol) :
                iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(i))
                
            else :
                iproto = "Unknown"

            if (i in tcp.Port_Source) :
                portsource = tcp.Port_Source.get(i)
            else :
                portsource = "Unknown"

            if (i in tcp.Port_destination) :
                portdest = tcp.Port_destination.get(i)
            else : 
                portdest = "Unknow"

            if (i in tcp.flagdic) :
                flag = tcp.flagdic.get(i)
            else : 
                flag = "Unknow"

            if (i in tcp.secdico) :
                sec = tcp.secdico.get(i)
            else : 
                sec = "Unknow"

            if (i in tcp.ackdico) :
                ack = tcp.ackdico.get(i)
            else : 
                sec = "Unknonw"   

            if (i in tcp.Windowdic) :
                windowtcp = tcp.Windowdic.get(i)
            else : 
                windowtcp  = "Unknow"

            if (i in tcp.lenght) :
                lenght = tcp.lenght.get(i)
            else : 
                lenght  = "Unknow"
            if (i in trame.dicoipver):
                iptype = trame.dicoipver.get(i)
            if iptype == "IPV4" :
                if(iproto == "TCP"):
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<15s}"+(40-len(ipsource))*"-" +"> {:<15s}"+(40-2*len(ipdest))*" " +" [ {:<6s}"+(7-len(portsource))*"-"+"> {:<6s}"+(10-len(portdest))*" "+"{}  Seq={}  Ack={}  Win={} Len={} ]").format(i,ipsource,ipdest,portsource,portdest,str(flag),sec,ack,windowtcp,lenght)
                    listbox.insert(tk.END,tmp)
                    if (i in httpmodule.httpsample) :
                         listbox.itemconfig(tk.END,bg="#6F1E51")           
                    else :
                         listbox.itemconfig(tk.END,bg="#006266")  
                else :
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iproto))*" "+"n'est pas pris en charge par le programme").format(i,iproto)
                    listbox.insert(tk.END,tmp)
                    listbox.itemconfig(tk.END,bg="#ee5253")  
            else :
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iptype))*" "+"n'est pas pris en charge par le programme").format(i,iptype)
                    listbox.insert(tk.END,tmp) 
                    listbox.itemconfig(tk.END,bg="#ee5253")
    else :
        condition = (entry.get()).split()
        row = filtrage.filtre(condition)
        if row == "echec":
            entry.config(bg="#ee5253")
        else : 
            if (row != "") : 
                entry.config(bg="#006266")
                for j in row:
                    (i,a,b,c)=j
                    ipsource = paquetip.Source_Address.get(i)
                    ipdest = (paquetip.Destination_Address).get(i)
                    iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(i))
                    portsource = tcp.Port_Source.get(i)
                    portdest = tcp.Port_destination.get(i)    
                    flag = tcp.flagdic.get(i)        
                    sec = tcp.secdico.get(i)
                    ack = tcp.ackdico.get(i)
                    windowtcp = tcp.Windowdic.get(i)
                    lenght = tcp.lenght.get(i)
                
                    if trame.dicoipver.get(i) == "IPV4" :
                            if(iproto == "TCP"):
                                tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<15s}"+(40-len(ipsource))*"-" +"> {:<15s}"+(40-2*len(ipdest))*" " +" [ {:<6s}"+(7-len(portsource))*"-"+"> {:<6s}"+(10-len(portdest))*" "+"{}  Seq={}  Ack={}  Win={} Len={} ]").format(i,ipsource,ipdest,portsource,portdest,str(flag),sec,ack,windowtcp,lenght)
                                listbox.insert(tk.END,tmp)
                                if (i in httpmodule.httpsample) :
                                    listbox.itemconfig(tk.END,bg="#6F1E51")           
                                else :
                                    listbox.itemconfig(tk.END,bg="#006266")  
                            else :
                                tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iproto))*" "+"n'est pas pris en charge par le programme").format(i,iproto)
                                listbox.insert(tk.END,tmp)
                                listbox.itemconfig(tk.END,bg="#ee5253")  
                    else :
                            tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iptype))*" "+"n'est pas pris en charge par le programme").format(i,iptype)
                            listbox.insert(tk.END,tmp) 
            try :
                filtrage.dbft.close()
            except :
                    pass  


def filtretree(event):
    for i in tree.get_children():
        tree.delete(i)
    if entry2.get() == "" :
        entry2.config(bg="#2f3542")
        for j in range(nbtrames):
            indarr = 0
            indidep =0
            tree.insert('', 'end', text= str(j+1),iid=str(j+1),tags=str(j+1))
            if paquetip.Source_Address.get(j+1) in listipflow  :
                fleche =(listipflow.index(paquetip.Source_Address.get(j+1))+1) < (listipflow.index(paquetip.Destination_Address.get(j+1))+1)

                if (j+1) in tcp.Port_destination :
                    portsource =""
                    if not(fleche):
                        portsource = tcp.Port_Source.get(j+1)
                    else :
                        portsource = tcp.Port_Source.get(j+1)+(size-len(tcp.Port_Source.get(j+1)))*"\u2015"
                else :
                    portsource ="Unknown"
            
                tree.set(str(j+1),column=listipflow.index(paquetip.Source_Address.get(j+1))+1,value= portsource)
                    
                indidep = listipflow.index(paquetip.Source_Address.get(j+1))+1

            if paquetip.Destination_Address.get(j+1) in listipflow  :

                if (j+1) in tcp.Port_destination :
                    portdest =""
                    if not(fleche) :
                        portdest = tcp.Port_destination.get(j+1)+"\u2190"+(size-len(tcp.Port_destination.get(j+1))-1)*"\u2015"
                    else :
                        portdest = "\u2192"+str(tcp.Port_destination.get(j+1))
                        tree.tag_configure(str(j+1), background='green')
                else :
                    portdest = "Unknown"
                
                tree.set(str(j+1),column=listipflow.index(paquetip.Destination_Address.get(j+1))+1,value= portdest) 

                if portdest == ("Unknown" or portsource =="Unknown") :
                    tree.tag_configure(str(j+1), background='#ee5253')
                else :
                    tree.tag_configure(str(j+1), background='#006266')
                    indarr = listipflow.index(paquetip.Destination_Address.get(j+1))+1
                    if indidep+1 < indarr:
                        for k in range (indidep+1,indarr) : 
                            tree.set(str(j+1),column=k,value="\u2015"*size) 
                    else : 
                        for k in range (indarr+1,indidep) : 
                            tree.set(str(j+1),column=k,value="\u2015"*size)
            else :
                if j+1 in trame.dicoipver :
                    tree.set(str(j+1),column=1,value= trame.dicoipver.get(j+1)) 
                    tree.tag_configure(str(j+1), background='#ee5253') 
                else : 
                    tree.set(str(j+1),column=1,value= "Unknown") 
                    tree.tag_configure(str(j+1), background='#ee5253')
    else :
        condition = (entry2.get()).split()
        row = filtrage.filtre(condition)
        if row == "echec":
            entry2.config(bg="#ee5253")
        else : 
            entry2.config(bg="#006266")
            for k in row:
                    (j,a,b,c)=k
                    indarr = 0
                    indidep =0
                    tree.insert('', 'end', text= str(j),iid=str(j),tags=str(j))
                    if paquetip.Source_Address.get(j+1) in listipflow  :
                        fleche =(listipflow.index(paquetip.Source_Address.get(j))+1) < (listipflow.index(paquetip.Destination_Address.get(j+1))+1)

                        if (j) in tcp.Port_destination :
                            portsource =""
                            if not(fleche):
                                portsource = tcp.Port_Source.get(j)
                            else :
                                portsource = tcp.Port_Source.get(j)+(size-len(tcp.Port_Source.get(j)))*"\u2015"
                        else :
                            portsource ="Unknown"
                    
                        tree.set(str(j),column=listipflow.index(paquetip.Source_Address.get(j))+1,value= portsource)
                            
                        indidep = listipflow.index(paquetip.Source_Address.get(j))+1

                    if paquetip.Destination_Address.get(j+1) in listipflow  :

                        if (j) in tcp.Port_destination :
                            portdest =""
                            if not(fleche) :
                                portdest = tcp.Port_destination.get(j+1)+"\u2190"+(size-len(tcp.Port_destination.get(j))-1)*"\u2015"
                            else :
                                portdest = "\u2192"+str(tcp.Port_destination.get(j))
                                tree.tag_configure(str(j+1), background='green')
                        else :
                            portdest = "Unknown"
                        
                        tree.set(str(j),column=listipflow.index(paquetip.Destination_Address.get(j))+1,value= portdest) 

                        if portdest == ("Unknown" or portsource =="Unknown") :
                            tree.tag_configure(str(j), background='#ee5253')
                        else :
                            tree.tag_configure(str(j), background='#006266')
                            indarr = listipflow.index(paquetip.Destination_Address.get(j))+1
                            if indidep+1 < indarr:
                                for k in range (indidep+1,indarr) : 
                                    tree.set(str(j),column=k,value="\u2015"*size) 
                            else : 
                                for k in range (indarr+1,indidep) : 
                                    tree.set(str(j),column=k,value="\u2015"*size)
                    else :
                        if j+1 in trame.dicoipver :
                            tree.set(str(j),column=1,value= trame.dicoipver.get(j)) 
                            tree.tag_configure(str(j), background='#ee5253') 
                        else : 
                            tree.set(str(j),column=1,value= "Unknown") 
                            tree.tag_configure(str(j), background='#ee5253')
            try :
                filtrage.dbft.close()
            except :
                pass

def lauchflow():
    global Flow_sharkw
    Flow_sharkw = tk.Tk()
    Flow_sharkw.title("Wire Owl - Flow Graph")
    Flow_sharkw.geometry("1280x720")  
    Flow_sharkw.config(background="#FFFFFF")
    Flow_sharkw.minsize(1280,720)
    Flow_sharkw.update()
    widthflow = Flow_sharkw.winfo_width()     
    heightflow = Flow_sharkw.winfo_height()

    frameflow =tk.Frame(Flow_sharkw,width=widthflow,bg = "#1a1a1a",height=(15*heightflow)/20)
    frameflow.pack_propagate(False)
    frameflow.pack(fill="both",side="top")
    global tree
    tree = ttk.Treeview(frameflow)
    # Création d'un widget de type Scrollbar
    scrollbar = tk.Scrollbar(frameflow, orient="horizontal")
    scrollbar2 = tk.Scrollbar(frameflow)
  
    scrollbar.configure(command=tree.xview)
    scrollbar2.configure(command=tree.yview)

    tree.configure(xscrollcommand=scrollbar.set)
    tree.configure(yscrollcommand=scrollbar.set)

    # Génération dynamique des noms de colonnes-
    global listipflow
    listipflow = list(set(paquetip.my_global_listip))
    listipflow.sort()
    nbcolonne = len(listipflow)
    global size
    size = int((widthflow)/10)
    colonnes = [str(i) for i in range(1,nbcolonne+1)]
    tree.column("#0", width=int(size/2), minwidth=int(size/2), stretch=tk.NO)
    tree.heading("#0", text="Trame", anchor=tk.W)
    # Définition des colonnes dans l'objet treeview
    tree["columns"] = colonnes
    name =""

    for i in range(0,nbcolonne) :
        name = listipflow[i]
        tree.column(str(i+1), width=size, minwidth=size, stretch=tk.NO)
        tree.heading(str(i+1), text=name, anchor=tk.W)
    scrollbar.pack(side="bottom", fill="x")
    scrollbar2.pack(side="right", fill="y")
    tree.pack(fill = tk.BOTH, expand=True)
   
    for j in range(nbtrames):
        indarr = 0
        indidep =0
        tree.insert('', 'end', text= str(j+1),iid=str(j+1),tags=str(j+1))
        if paquetip.Source_Address.get(j+1) in listipflow  :
            fleche =(listipflow.index(paquetip.Source_Address.get(j+1))+1) < (listipflow.index(paquetip.Destination_Address.get(j+1))+1)

            if (j+1) in tcp.Port_destination :
                portsource =""
                if not(fleche):
                    portsource = tcp.Port_Source.get(j+1)
                else :
                    portsource = tcp.Port_Source.get(j+1)+(size-len(tcp.Port_Source.get(j+1)))*"\u2015"
            else :
                portsource ="Unknown"
        
            tree.set(str(j+1),column=listipflow.index(paquetip.Source_Address.get(j+1))+1,value= portsource)
                
            indidep = listipflow.index(paquetip.Source_Address.get(j+1))+1

        if paquetip.Destination_Address.get(j+1) in listipflow  :

            if (j+1) in tcp.Port_destination :
                portdest =""
                if not(fleche) :
                    portdest = tcp.Port_destination.get(j+1)+"\u2190"+(size-len(tcp.Port_destination.get(j+1))-1)*"\u2015"
                else :
                    portdest = "\u2192"+str(tcp.Port_destination.get(j+1))
                    tree.tag_configure(str(j+1), background='green')
            else :
                portdest = "Unknown"
               
            tree.set(str(j+1),column=listipflow.index(paquetip.Destination_Address.get(j+1))+1,value= portdest) 

            if portdest == ("Unknown" or portsource =="Unknown") :
                 tree.tag_configure(str(j+1), background='#ee5253')
            else :
                tree.tag_configure(str(j+1), background='#006266')
                indarr = listipflow.index(paquetip.Destination_Address.get(j+1))+1
                if indidep+1 < indarr:
                    for k in range (indidep+1,indarr) : 
                        tree.set(str(j+1),column=k,value="\u2015"*size) 
                else : 
                    for k in range (indarr+1,indidep) : 
                        tree.set(str(j+1),column=k,value="\u2015"*size)
        else :
            if j+1 in trame.dicoipver :
                tree.set(str(j+1),column=1,value= trame.dicoipver.get(j+1)) 
                tree.tag_configure(str(j+1), background='#ee5253') 
            else : 
                tree.set(str(j+1),column=1,value= "Unknown") 
                tree.tag_configure(str(j+1), background='#ee5253') 

    framebot = tk.Frame(Flow_sharkw,width=widthflow,height=(5*heightflow)/20)
    buttonexit = tkmacosx.Button(framebot,text = "Exit",command=exitcustomflow,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a",fg = "white")
    text = tk.Text(framebot,bg ="#1a1a1a",fg="#FFFFFF",width=widthflow,font=tkFont.Font(family='Myanmar Text', size=12),yscrollcommand=scrollbar1)
    buttonexit.pack(side="right")
    
    
    global entry2 
    entry2 = tk.Entry(framebot, textvariable=tk.StringVar(),justify=tk.LEFT,bg="#2f3542",cursor="xterm",fg="#dfe6e9",width=20,font=tkFont.Font(family='Myanmar Text', size=9,slant="italic"))
    entry2.insert(0," Appliquer un filtre")
    entry2.pack(side="top",fill="both")
    entry2.bind('<Return>', filtretree)
    entry2.bind("<Double-Button-1>",lambda event: entry2.delete(0, tk.END))
    text.pack(side="top" )
    entry2.pack(side = "bottom",fill="both")
    framebot.pack(side="bottom",fill="both")
    def itemselecttree (event) :
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['tags']
            # show a message
            text.delete('1.0', tk.END)
        #and 
        i = record[0]
        if i != 0 :    
            if (i in paquetip.Protocol) :
                iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(i))    
            else :
                iproto = "Unknown"

            if (i in tcp.Port_Source) :
                portsource = tcp.Port_Source.get(i)
            else :
                portsource = "Unknown"

            if (i  in tcp.Port_destination) :
                portdest = tcp.Port_destination.get(i)
            else : 
                portdest = "Unknown"

            if (i  in tcp.flagdic) :
                flag = tcp.flagdic.get(i)
            else : 
                flag = "Unknown"
            if(i in tcp.dicoheaderlength):
                hl = tcp.dicoheaderlength.get(i)
            else : 
                hl = "Unknown"
            if (i  in tcp.secdico) :
                sec = tcp.secdico.get(i)
            else : 
                sec = "Unknown"

            if (i  in tcp.ackdico) :
                ack = tcp.ackdico.get(i)
            else : 
                ack = "Unknown"   

            if (i  in tcp.Windowdic) :
                windowtcp = tcp.Windowdic.get(i)
            else : 
                windowtcp  = "Unknown"

            if (i  in tcp.lenght) :
                tcplenght = tcp.lenght.get(i)
            else : 
                tcplenght  = "Unknown"
                
            if (i in tcp.dicocheksum):
                check = tcp.dicocheksum.get(i)
            else :
                check = "Unknown"
            if(i in tcp.dicourgentpoint):
                urgentpoint =  tcp.dicourgentpoint.get(i)
            else : 
                urgentpoint = "Unknown"

            if(iproto == "TCP"):
                tmp = ("Port Source :{:<6s} Port Destination :{:<6s}\n Tcp Segment Option: {} \n Next Sequence Number: {}  Acknowledgment number: {}\n Header Length: {} \nFlag: {}\n Window: {}\nChecksum: {} \nUrgent Point: {}").format(portsource,portdest,tcplenght,sec,ack,hl,str(flag),windowtcp,check,urgentpoint)        
                text.insert(tk.END,tmp)
        

    tree.bind('<<TreeviewSelect>>',itemselecttree) 
        

    # Modifiez la valeur d'une cellule
   

    Flow_sharkw.mainloop()        
        
def Restart() : 
    if(messagebox.askyesno("Restart","Voulez-vous relancer le programme ?")):
        for widget in window.winfo_children():
            widget.pack_forget() # Si vous utilisez .pack()
            
        global path
        path =""
        global listbox
        listbox.delete(0,tk.END)
        menu_principal()

def menu_principal():
    
    # Add image file
    bg = tk.PhotoImage(file = "./affichage/bg-menu.png")
    
    # Create Canvas
    Background = tk.Canvas( window, width = 400,height = 400)
    Background.pack(fill = "both", expand = True)
    
    # Display image
    Background.create_image( 0, 0, image = bg, anchor = "nw")

	#ajout Bouton start et association
    start = tk.Frame(Background,bg="#FFFFFF",height =54,width=280)
    button = tk.PhotoImage(file = "./affichage/button.png")
    launch_button = tkmacosx.Button(start,command=launch,image=button,relief=tk.RIDGE,borderwidth=1)
    Background.create_window( width/2 ,height -height/7,window = start)
    launch_button.pack(fill = "both")
    
    #ajout Bouton Folder et association
    folder = tk.Frame(Background,bg="#FFFFFF",height =54,width=54)
    searchico = tk.PhotoImage(file = "./affichage/icone-de-dossier-symbole-png-noi.png")
    launch_search = tkmacosx.Button(folder,command=search,image=searchico,relief=tk.RIDGE,borderwidth=1,bg="White",activebackground="#1a1a1a")
    Background.create_window( width-width/3 ,height -height/7,window = folder)
    launch_search.pack(fill = "both")

    #Info pratique
    label_copyright=tk.Label(Background,text="2022-2023, Sorbonne Universite. Designed by Malek Bouzarkouna, Sevag Baboyan",bg="#1a1a1a",fg="#ffffff")
    label_copyright.pack(side="bottom")

    window.mainloop()



def affichage():
    #peronnalisation de la fenetre
   
    # Add image file
    bg = tk.PhotoImage(file = "./affichage/bg.png")
    
    # Create Canvas
    Background = tk.Canvas( window, width = 400,height = 400)
    Background.pack(fill = "both", expand = True)
    
    # Display image
    Background.create_image( 0, 0, image = bg, anchor = "nw")
  
    frame_text =tk.Frame(Background,height = height/2,width=(29*width)/30,bg ="#1a1a1a") 
    frame_text.grid(column=0,row=2,columnspan=3,pady=50,padx=25,sticky="nswe")
    frame_text.pack_propagate(False)
    frame_separation=tk.Frame(Background,height = height/3,width=(19*width)/20,bg="White")   
    frame_separation.pack_propagate(False)
    frame_separation.grid(row=1,column=0,padx=10,columnspan=2,sticky="n")

  

    #Different titre 
    global entry 
    global listbox
    entry = tk.Entry(Background, textvariable=tk.StringVar(),justify=tk.LEFT,bg="#2f3542",cursor="xterm",fg="#dfe6e9",width=50,font=tkFont.Font(family='Myanmar Text', size=9,slant="italic"))
    entry.insert(0," Appliquer un filtre")
    entry.grid(row=0,column=0,columnspan=2,sticky="nsew",padx=10,pady=5) 
    entry.bind('<Return>', filtrefolistbox)
    entry.bind("<Double-Button-1>",lambda event: entry.delete(0, tk.END))

    #creation de de la listbox pour contenir nos information
    i=0
    fixedlen =40

    listbox =tk.Listbox(frame_separation,height = 40,
                        width=170,
                        bg = "#1a1a1a",
                        activestyle = 'dotbox',
                        font = tkFont.Font(family='Myanmar Text', size=9),
                        fg = "black")

    fichier = open(".\Trames\Trame0.txt", "w")
    for i in range(nbtrames) :
            i+=1
            ipsource =""
            ipdest = ""
            iproto = ""
            portsource = ""
            portdest = ""
            flag = ""
            windowtcp = ""
            lenght = ""
            sec = ""
            ack= ""
            #and 
            if (i in paquetip.Source_Address) :
                ipsource = paquetip.Source_Address.get(i)
                
            else :
                ipsource = "Unknown"
            
            if (i in paquetip.Destination_Address) :
                ipdest = (paquetip.Destination_Address).get(i)
                
            else :
                ipsource = "Unknown"
            
            if (i in paquetip.Protocol) :
                iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(i))
                
            else :
                iproto = "Unknown"

            if (i in tcp.Port_Source) :
                portsource = tcp.Port_Source.get(i)
            else :
                portsource = "Unknown"

            if (i in tcp.Port_destination) :
                portdest = tcp.Port_destination.get(i)
            else : 
                portdest = "Unknow"

            if (i in tcp.flagdic) :
                flag = tcp.flagdic.get(i)
            else : 
                flag = "Unknow"

            if (i in tcp.secdico) :
                sec = tcp.secdico.get(i)
            else : 
                sec = "Unknow"

            if (i in tcp.ackdico) :
                ack = tcp.ackdico.get(i)
            else : 
                sec = "Unknonw"   

            if (i in tcp.Windowdic) :
                windowtcp = tcp.Windowdic.get(i)
            else : 
                windowtcp  = "Unknow"

            if (i in tcp.lenght) :
                lenght = tcp.lenght.get(i)
            else : 
                lenght  = "Unknow"
            if (i in trame.dicoipver):
                iptype = trame.dicoipver.get(i)
            if iptype == "IPV4" :
                if(iproto == "TCP"):
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<15s}"+(fixedlen-len(ipsource))*"-" +"> {:<15s}"+(fixedlen-2*len(ipdest))*" " +" [ {:<6s}"+(7-len(portsource))*"-"+"> {:<6s}"+(10-len(portdest))*" "+"{}  Seq={}  Ack={}  Win={} Len={} ]").format(i,ipsource,ipdest,portsource,portdest,str(flag),sec,ack,windowtcp,lenght)
                    fichier.write(tmp+"\n")
                    listbox.insert(tk.END,tmp)
                    if (i in httpmodule.httpsample) :
                         listbox.itemconfig(tk.END,bg="#6F1E51")           
                    else :
                         listbox.itemconfig(tk.END,bg="#006266")  
                else :
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iproto))*" "+"n'est pas pris en charge par le programme").format(i,iproto)
                    fichier.write(tmp+"\n")
                    listbox.insert(tk.END,tmp)
                    listbox.itemconfig(tk.END,bg="#ee5253")  
            else :
                    tmp = ("{:<4d}"+(8-len(str(i)))*" " +"{:<10s}"+(8-len(iptype))*" "+"n'est pas pris en charge par le programme").format(i,iptype)
                    fichier.write(tmp+"\n")
                    listbox.insert(tk.END,tmp)
                    listbox.itemconfig(tk.END,bg="#ee5253")  
    fichier.close()


    #creation de la scroolbar qu'on fixe sur le cote 
    scrollbar = tk.Scrollbar(frame_separation)

    #lien entre la scrool bar et la list box 
    scrollbar.config(command = listbox.yview)
    policesize = 11
    listbox.config(yscrollcommand = scrollbar.set,font=tkFont.Font(family='Myanmar Text', size=policesize),fg="#ffffff")

    
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y,pady=5)
    listbox.pack(fill="both",padx=5,pady=5)
            
    #Detail
    frame_info = tk.Frame(frame_text,bg ="White")
    frame_info_button_m = tk.Frame(frame_info,bg ="white",width=width/20,height=height/2)
    #fonction utile 
    def all() :
        if indicelistbox != 0 :
            label_print.delete('1.0', tk.END)
            fichier = open("./Trames/Trame"+str(indicelistbox)+".txt", "r")
            label_print.insert(tk.END,fichier.read())
            fichier.close()

    def Ethernet():
        info =""
        ipver =""
        label_print.delete('1.0', tk.END)
        if indicelistbox != 0 :
            if indicelistbox in trame.mac_adress_source : 
                mac_adresse = trame.mac_adress_source.get(indicelistbox)
            if indicelistbox in trame.mac_adress_distination :
                mac_source = trame.mac_adress_distination.get(indicelistbox)
            if indicelistbox in trame.dicoipver:
                ipver = trame.dicoipver.get(indicelistbox)
                for cle, valeur in trame.typethernet.items():
                    if valeur == ipver :
                        info = cle 

            text = "Ethernet : \n Mac Source: {} \n Mac destination: {} \n Type: {} (0x{}) ".format(mac_adresse,mac_source,ipver,info )
            label_print.insert(tk.END,text)

    def Ipv4():
        label_print.delete('1.0', tk.END)
        if indicelistbox != 0 :
            if (indicelistbox in paquetip.Source_Address) :
                ipsource = paquetip.Source_Address.get(indicelistbox)
                    
            else :
                ipsource = "Unknown"
                
            if (indicelistbox in paquetip.Destination_Address) :
                ipdest = (paquetip.Destination_Address).get(indicelistbox)
                    
            else :
                ipsource = "Unknown"
                
            if (indicelistbox in paquetip.Protocol) :
                iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(indicelistbox))
                    
            else :
                iproto = "Unknown"

            if  (indicelistbox in paquetip.header_length) :
                hdl = paquetip.header_length.get(indicelistbox) 
            else :
                hdl = "Unknown"
            if (indicelistbox in paquetip.tos) : 
                tos = paquetip.tos.get(indicelistbox)
            else : 
                tos = "Unknown"
            if (indicelistbox in paquetip.total_length): 
                tl = paquetip.total_length.get(indicelistbox)
            else : 
                tl = "Unknown"
            if (indicelistbox in paquetip.Identification) :
                ident = paquetip.Identification.get(indicelistbox)
            else : 
                ident = "Unknown"
            if (indicelistbox in paquetip.Fragment_offsetdic):
                frag = paquetip.Fragment_offsetdic.get(indicelistbox)
            else :
                frag = "Unknown"
            if (indicelistbox in paquetip.Time_to_live) :
                ttl = paquetip.Time_to_live.get(indicelistbox)
            else :
                ttl = "Unknown"
            if (indicelistbox in paquetip.Reserved) :
                res = paquetip.Reserved.get(indicelistbox)
            else : 
                res = "Unknown"
            if (indicelistbox in paquetip.DF):
                df = paquetip.DF.get(indicelistbox)
            else:
                df = "Unknown"
            if (indicelistbox in paquetip.MF) :
                mf = paquetip.MF.get(indicelistbox)
            else :
                mf = "Unknown"
            if (indicelistbox in paquetip.Header_checksum) :
                hc = paquetip.Header_checksum.get(indicelistbox)

            else : 
                hc = "Unknown"
            label_print.delete('1.0', tk.END)
            text = "IP : \nSource : {} --> Destination {}\nType : {}\nHeader Length: {}    Tos: {}   Total length : {}   \nIdentification : 0x{} \nFlag :\nReserved : {} DF : {} MF : {} \nTTL {} \nProtocol : {} \nHeader_checksum : {} \n Fragment offset {}".format(ipsource,ipdest,"4",hdl,tos,tl,ident,res,df,mf,ttl,iproto,hc,frag)
            label_print.insert(tk.END,text)

    def TCPf() : 
        label_print.delete('1.0', tk.END)
        #and 
        if indicelistbox != 0 :    
            if (indicelistbox in paquetip.Protocol) :
                iproto = paquetip.dico_protocol.get((paquetip.Protocol).get(indicelistbox))    
            else :
                iproto = "Unknown"

            if (indicelistbox in tcp.Port_Source) :
                portsource = tcp.Port_Source.get(indicelistbox)
            else :
                portsource = "Unknown"

            if (indicelistbox  in tcp.Port_destination) :
                portdest = tcp.Port_destination.get(indicelistbox)
            else : 
                portdest = "Unknown"

            if (indicelistbox  in tcp.flagdic) :
                flag = tcp.flagdic.get(indicelistbox)
            else : 
                flag = "Unknown"
            if(indicelistbox in tcp.dicoheaderlength):
                hl = tcp.dicoheaderlength.get(indicelistbox)
                print(hl)
            else : 
                hl = "Unknown"
            if (indicelistbox  in tcp.secdico) :
                sec = tcp.secdico.get(indicelistbox)
            else : 
                sec = "Unknown"

            if (indicelistbox  in tcp.ackdico) :
                ack = tcp.ackdico.get(indicelistbox)
            else : 
                ack = "Unknown"   

            if (indicelistbox  in tcp.Windowdic) :
                windowtcp = tcp.Windowdic.get(indicelistbox)
            else : 
                windowtcp  = "Unknown"

            if (indicelistbox  in tcp.lenght) :
                tcplenght = tcp.lenght.get(indicelistbox)
            else : 
                tcplenght  = "Unknown"
                
            if (indicelistbox in tcp.dicocheksum):
                check = tcp.dicocheksum.get(indicelistbox)
            else :
                check = "Unknown"
            if(indicelistbox in tcp.dicourgentpoint):
                urgentpoint =  tcp.dicourgentpoint.get(indicelistbox)
            else : 
                urgentpoint = "Unknown"

            if(iproto == "TCP"):
                tmp = ("Port Source: "+portsource+" Port Destination: "+ portdest+"\nTcp Segment option: "+str(tcplenght)+"\n Next Sequence Number: "+sec+"Acknowledgment number: "+ack+" \nFlag: "+str(flag)+"\n Window: "+windowtcp+"\nChecksum: "+check+"\nUrgent Point:"+ urgentpoint)     
                label_print.insert(tk.END,tmp)

    def Http():
        label_print.delete('1.0', tk.END)
        if indicelistbox != 0 :
            if indicelistbox in httpmodule.httpsample and (tcp.Port_Source.get(indicelistbox) == "80" or tcp.Port_destination.get(indicelistbox) == "80"):
                text = httpmodule.httpsample.get(indicelistbox)
                
            else :
                text = "Il n'a pas de HTTP"
            label_print.insert(tk.END,text)

        
        
    frame_info_button=tk.Canvas(frame_info_button_m, width = width/10,height = height/2,bg="#1a1a1a")

   


    #Buttton select
    all_frame = tk.Frame(frame_info_button,bg="#1a1a1a")
    allico = tk.PhotoImage(file = "./affichage/all.png")
    frame_button_All =tkmacosx.Button(all_frame,command=all,image=allico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    all_frame.pack(pady=10,padx=10)
    frame_button_All.pack_propagate(False)
    frame_button_All.pack(fill="both")
    
    Ethernet_frame = tk.Frame(frame_info_button,bg="#1a1a1a")
    Ethernetico = tk.PhotoImage(file = "./affichage/Ethernet.png")
    frame_button_Ethernet=tkmacosx.Button(Ethernet_frame,command = Ethernet,image=Ethernetico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    Ethernet_frame.pack(pady=10,padx=10)
    frame_button_Ethernet.pack_propagate(False)
    frame_button_Ethernet.pack()
   
    ipv4frame  = tk.Frame(frame_info_button,bg="#1a1a1a")
    ipv4ico = tk.PhotoImage(file = "./affichage/IPV4.png")
    frame_button_IPV4=tkmacosx.Button(ipv4frame,command = Ipv4,image= ipv4ico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    ipv4frame.pack(pady=10,padx=10)
    frame_button_IPV4.pack_propagate(False)
    frame_button_IPV4.pack()
    
    TCPframe  = tk.Frame(frame_info_button,bg="#1a1a1a")
    TCPico = tk.PhotoImage(file = "./affichage/tcp.png")
    frame_button_TCP=tkmacosx.Button(TCPframe,command = TCPf,image= TCPico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    TCPframe.pack(pady=10,padx=10)
    frame_button_TCP.pack_propagate(False)
    frame_button_TCP.pack()
    
    httpframe  = tk.Frame(frame_info_button,bg="#1a1a1a")
    httpico = tk.PhotoImage(file = "./affichage/http.png")
    frame_button_HTTP=tkmacosx.Button(httpframe,command = Http,image= httpico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    httpframe.pack(pady=10,padx=10)
    frame_button_HTTP.pack_propagate(False)
    frame_button_HTTP.pack()


    frame_info_button.pack(fill=tk.X)
    frame_info_button_m.pack_propagate(False)
    frame_info_button_m.pack(side=tk.LEFT,fill=tk.X,pady=10)
    global scrollbar1
    scrollbar1 = tk.Scrollbar(frame_info)
    label_print=tk.Text(frame_info,bg ="#1a1a1a",fg="#FFFFFF",font=tkFont.Font(family='Myanmar Text', size=12),yscrollcommand=scrollbar1)
    scrollbar1.pack(side=tk.RIGHT,fill=tk.Y,pady=5)
    label_print.pack(side=tk.RIGHT,fill="both",pady=5)
    frame_info.pack(side=tk.LEFT,fill=tk.X,padx=5,pady=5)
   

    
    def items_selected(event):
        selected_indices= listbox.curselection()
        if(selected_indices != ()) :
            tmp :str = listbox.selection_get()
            label_print.delete('1.0', tk.END)
            global indicelistbox
            tmp=tmp[:8]
            tmp = tmp.replace(" ","")
            indicelistbox = int(tmp)
            fichier = open("./Trames/Trame"+tmp+".txt", "r")
            label_print.insert(tk.END,fichier.read())
            fichier.close()

    listbox.bind('<<ListboxSelect>>', items_selected) 

  
    #Buttton option menu
    frame_button = tk.Frame(frame_text,borderwidth=0)
    frame_button.pack(side=tk.RIGHT,fill=tk.X,anchor="se")
    framerestart=tk.Canvas(frame_button, width = width/10,height = height/3,bg="#1a1a1a")

    flow = tk.Frame(framerestart,bg="#1a1a1a")
    flowico = tk.PhotoImage(file = "./affichage/flow_graph.png")
    buttonflow = tkmacosx.Button(flow ,command=lauchflow,image=flowico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    framerestart.create_window( 1 ,0,window =flow)
    flow.pack(pady=10,padx=10)
    buttonflow.pack(fill="both")

    pdf = tk.Frame(framerestart,bg="#1a1a1a")
    pdfico = tk.PhotoImage(file = "./affichage/idcopdf.png")
    buttonpdf = tkmacosx.Button(pdf,command=pdfsave,image= pdfico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    framerestart.create_window( 1 ,0,window =pdf)
    pdf.pack(pady=10,padx=10)
    buttonpdf.pack(fill="both",pady=5,padx=5)

    
    restart = tk.Frame(framerestart,bg="#1a1a1a")
    restartico = tk.PhotoImage(file = "./affichage/reset.png")
    buttonrestart = tkmacosx.Button(restart,command=Restart,image= restartico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    framerestart.create_window( 100,0,window = restart)
    restart.pack(pady=10,padx=10)
    buttonrestart.pack(fill="both")

    
    exit = tk.Frame(framerestart,bg="#1a1a1a")
    exitico = tk.PhotoImage(file = "./affichage/exit.png")
    buttonexit = tkmacosx.Button(exit,command=exitcustom,image= exitico,relief=tk.RIDGE,borderwidth=0,bg="#1a1a1a",activebackground="#1a1a1a")
    framerestart.create_window( 0,0,window =exit)
    exit.pack(pady=10,padx=10)
    buttonexit.pack(fill="both")
    framerestart.pack()

    
    window.mainloop()






