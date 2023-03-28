from fpdf import FPDF
import glob,datetime,os,platform,time
class PDF(FPDF):
    #header
    def header(self) -> None:
        self.set_fill_color(26, 26, 26)
        self.rect(0,0,pdf.w,pdf.h,"F")
        self.image("./affichage/wireowl_ico.gif",10,8,25)   
        self.set_font("Arial", size=47)
        title_w = self.get_string_width("WireOwl")+6
        doc_w=self.w
        self.set_x((doc_w - title_w)/2)
        self.set_draw_color(255,255,255)
        self.set_fill_color(26, 26, 26)
        self.set_text_color(255,255,255)
        self.set_line_width(1)
        self.cell(title_w,20,"WireOwl",border=True,ln=1,align='C',fill=1)
        self.ln(10)

    #footer
    def footer(self) :
       self.set_y(-15) 
       self.set_font("Arial", size=11) 
       self.set_text_color(169,169,169)
       self.cell(0,10,f'Page {self.page_no()}',align='C')

    def chapter_title(self,ch_num,link):
        self.set_link(link)
        self.set_draw_color(255, 255, 255)
        self.set_fill_color(26, 26, 26)
        self.set_text_color(255,255,255)
        self.set_font("Arial", size=24) 
        if ch_num == -1:
            chapter_title = "Sommaire"
        elif ch_num == 0:
             chapter_title = "Flow Graph"
        else : chapter_title = f"Trame : {ch_num} "
        self.cell(self.w/5,10,chapter_title,ln=1,fill=1)
        self.ln()

    def chapter_body(self,name):
        with open(os.path.join(os.getcwd(), name), 'rb') as fh : 
           txt = fh.read().decode('latin-1')
        self.set_font('Times','',9)
        self.set_text_color(255,255,255) 
        pdf.multi_cell(w=0,h=5,txt =txt,border=True)
        self.ln()
        #end

    def chapter_resume(self,name):
        pdf.add_page()     
        with open(name,'r') as filin:
            lignes = filin.readlines()
            for ligne in lignes :
                self.set_draw_color(26, 26, 26)
                self.set_fill_color(26, 26, 26)
                self.set_text_color(255,255,255)
                self.set_font("Arial", size=9) 
                pdf.cell(w=0,h=5,txt=ligne.replace("    "," "),border=True,ln=1,fill=1)
        


    def print_chapter(self,ch_num,name,link):
        self.add_page()
        self.chapter_title(ch_num,link)
        self.chapter_body(name)
        

def lauchpdf(nbtrame):
    my_os = platform.system()
    global pdf
    pdf = PDF('L')
    pdf.set_auto_page_break(auto=True,margin = 15)
    pdf.add_page()
    pdf.chapter_title(-1,link=pdf.add_link)
    Listlink=[]
    Listlink.append(pdf.add_link())
    pdf.set_font('Times','',11)
    pdf.cell(w=0,h=10,txt="--------  Flow Graph  ---------",ln=1,fill=1,link=Listlink[0],align="C")
    for i in range(1,nbtrame+1) :
        Listlink.append(pdf.add_link())
        pdf.set_font('Times','',11)
        pdf.cell(w=0,h=4,txt="-------- Trame : "+str(i)+" ---------",ln=1,fill=1,link=Listlink[i],align="C")   
    i=0
    for filename in glob.glob("./Trames/*.txt"):
        i=i+1   
        if (filename != "./Trames/Trame0.txt") : 
            pdf.print_chapter(i-1,filename,Listlink[i-1])  
        else : 
            pdf.print_chapter(0,filename,Listlink[0])
    tmp="./PDF/Analyse"+str(datetime.datetime.now()).replace(":","-").replace(" ","_") + ".pdf"
    pdf.output(tmp) 

    try : 
        if (my_os == "Darwin") :
            os.open(tmp)
        elif(my_os == "Windows"):   
            os.startfile(tmp)
        elif(my_os == "Linux"):
            os.system("xdg-open "+tmp)
    except FileNotFoundError :
      pass
            

            
    

    