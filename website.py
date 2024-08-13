import streamlit as st
import fitz
import os
import math

def old_parse_file(filename):
    file=fitz.open(filename)
    pages=file.page_count
    final=fitz.open()
    shipping=fitz.open()
    row=0
    otherrow=0
    pagenumber=0
    otherpagenumber=0
    labelsdone=0
    shippinglabelsdone=0
    for i in range(math.ceil((pages/2)/8)):
        final._newPage(width=612,height=792)
    for i in range(round((pages/2))):
        shipping._newPage(width=612,height=792)
    folder=os.path.join(os.path.expanduser('~'), 'Downloads', "TikTokStuff")
    if not os.path.exists(folder):
    # Create the folder if it doesn't exist
        os.makedirs(folder)
    for i in range(pages):
        if i%2==0:
            shippinglabelsdone+=1
            betweenfinal=fitz.open()
            page=file.load_page(i)
            betweenfinal.insert_pdf(file,i,i)
            shippingpage=shipping.load_page(otherpagenumber)
            otherpagenumber+=1
            shippingpage.show_pdf_page(fitz.Rect(0,0,612,792),betweenfinal)
            otherfilepath=os.path.join(folder, "shipping.pdf")
            shipping.save(otherfilepath)
            print(f"Shipping Label {shippinglabelsdone} processed")
        if i%2==1:
            labelsdone+=1
            if labelsdone%2==1:
                row+=1
            
            page=file.load_page(i)
            page.set_cropbox(fitz.Rect(150,180,460,350))
            betweenfinal=fitz.open()
            betweenfinal.insert_pdf(file,i,i)
            width=310*(labelsdone%2)
            height=170*row
            if height>792:
                pagenumber+=1
                height=170
                row=1
            finalpage=final.load_page(pagenumber)
            finalpage.show_pdf_page(fitz.Rect(width,(170*(row-1)),width+310,height),betweenfinal)
            file_path = os.path.join(folder, "labels.pdf")
            # betweenfinal.save("moo.pdf")
            final.save(file_path)
            print(f"Label {labelsdone} processed")
        
def parse_file(filename):
    file=fitz.open(filename)
    pages=file.page_count
    final=fitz.open()
    shipping=fitz.open()
    row=0
    otherrow=0
    pagenumber=0
    otherpagenumber=0
    labelsdone=0
    shippinglabelsdone=0
    for i in range(math.ceil((pages/2))):
        final._newPage(width=612,height=792)
    for i in range(round((pages/2))):
        shipping._newPage(width=612,height=792)
    folder=os.path.join(os.path.expanduser('~'), 'Downloads', "TikTokStuff")
    if not os.path.exists(folder):
    # Create the folder if it doesn't exist
        os.makedirs(folder)
    for i in range(pages):
        if i%2==0:
            shippinglabelsdone+=1
            betweenfinal=fitz.open()
            page=file.load_page(i)
            page.set_cropbox(fitz.Rect(75,30,538,720))
            betweenfinal.insert_pdf(file,i,i)
            shippingpage=shipping.load_page(otherpagenumber)
            otherpagenumber+=1
            shippingpage.show_pdf_page(fitz.Rect(0,0,612,792),betweenfinal)
            otherfilepath=os.path.join(folder, "shipping.pdf")
            # otherfilepath="shipping.pdf"
            shipping.save(otherfilepath)
            print(f"Shipping Label {shippinglabelsdone} processed")
        if i%2==1:
            labelsdone+=1
            if labelsdone%2==1:
                row+=1
            
            page=file.load_page(i)
            page.set_cropbox(fitz.Rect(0,0,575,430))
            betweenfinal=fitz.open()
            betweenfinal.insert_pdf(file,i,i)
            finalpage=final.load_page(pagenumber)
            pagenumber+=1
            finalpage.show_pdf_page(fitz.Rect(0,0,612,792),betweenfinal)
            file_path = os.path.join(folder, "labels.pdf")
            # file_path = "labels.pdf"
            # betweenfinal.save("moo.pdf")
            final.save(file_path)
            print(f"Label {labelsdone} processed")              
    print("Check labels.pdf for the labels and shippinglabels.pdf for the shipping labels")



file=st.file_uploader("Import file",type="pdf")
# f=fitz.open()
# f.write(file.read)
if file is not None:
    parse_file(os.path.join(os.path.expanduser('~'), 'Downloads', file.name))
    st.write("Check your downloads folder for labels.pdf and shipping.pdf")
