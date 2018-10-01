#from PyPDF2 import PdfFileWriter, PdfFileReader
import zipfile
from fpdf import FPDF
import re
import os
import argparse

parser=argparse.ArgumentParser("Provide the zipped whatsapp file and the name of the two participatnts")
parser.add_argument('--zip',help="zipped whatapp chat archive")
parser.add_argument('-p1',help="first person")
parser.add_argument('-p2',help="second person")
args=parser.parse_args()


print args
fn=args.zip
part1=args.p1
part2=args.p2




### set up the pdf 
pdf=FPDF()
pdf.add_page()
pdf.set_xy(0,0)
pdf.set_font('Times','',10.0)
effective_page_width = pdf.w - 2*pdf.l_margin




zipchat = zipfile.ZipFile(fn, 'r')
#zipchat.printdir()



#chat=zipchat.read("_chat.txt")
chat=zipchat.open("_chat.txt")
#print chat


#exit()
#print chat



#pdf.image("00006181-PHOTO-2018-09-11-05-28-18.jpg",h=20)



n=20
cur_ds=0   ### current datastamp
for line in chat.readlines():
    #print(line)
    #x=raw_input("Press Enter to continue...")
    #continue
    m=re.search("(\[.*?\]) (\S+): (.*)",line)
    if m:
        ts=m.group(1)
        #print ts
        ds=re.search("(\d+\/\d+\/\d+)",ts).group(1)
        #print ds
        #raw_input("Press Enter to continue...")
        
        if ds!=cur_ds:
            #print "new ts is",ts
            if cur_ds != 0:
                
                pdf.add_page()
            
            print ds
            align="C"
            pdf.set_font('Times','B',20.0)
            pdf.set_text_color(0,0,0)
            pdf.cell(h=5,align=align,w=0,txt=ds, border=0)
            pdf.set_font('Times','',10.0)
            pdf.ln(5)
            cur_ds=ds
            
        
        
        id=m.group(2)
        txt=m.group(3)
        
        #print txt

        align="L"
        imagex=1
        if id==part1:
            pdf.set_text_color(244,92,66)
            align="L"
            imagex=1
        if id==part2:
            pdf.set_text_color(66,134,244)
            #align="R"
            #imagex=effective_page_width-40
            align="L"
            imagex=1
        
        #print(id,align)
        if "attached" in line:
            if "jpg" in line:
                #print(line)
                m=re.search("(\S+.jpg)",line)
                jpg=m.group(1)
                img=zipchat.extract(jpg,"temp")
                print("attaching ",img)
                pdf.cell(h=5.0,align=align,w=0,txt=ts, border=0)
                pdf.ln(5)
                pdf.image(img,h=40,x=imagex)
                pdf.ln(5)
                os.remove(img)
        else:
            text=ts + ' ' + txt      
            #pdf.cell(h=5.0,align=align,w=0,txt=ts, border=0)
            pdf.ln(5)
            #pdf.multi_cell(w=effective_page_width,h=5,txt=txt, border=0,align=align)
            pdf.multi_cell(w=effective_page_width,h=5,txt=ts + ":" + txt, border=0,align=align)
            pdf.ln(5)
            #pdf.cell(ln=n,h=5.0,align='L',w=0,txt=text, border=0)
            #pdf.cell(ln=n,h=5.0,align='L',w=0,txt=line, border=0)
            n+=1
            
            
print "printing pdf"
pdf.output('_chat.pdf','F')

