import streamlit as st
import fitz
import os
import math
import tempfile



def parse_file(filename):
    file=fitz.open(filename)
    pages=file.page_count
    final=fitz.open()
    shipping=fitz.open()
    pagenumber=0
    otherpagenumber=0
    labelsdone=0
    shippinglabelsdone=0
    for i in range(math.ceil((pages/2))):
        final._newPage(width=612,height=792)
    for i in range(round((pages/2))):
        shipping._newPage(width=612,height=792)
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
            otherfilepath="shipping.pdf"
            # otherfilepath="shipping.pdf"
            shipping.save(otherfilepath)

            print(f"Shipping Label {shippinglabelsdone} processed")
        if i%2==1:
            labelsdone+=1
            finalpage=final.load_page(pagenumber)
            pagenumber+=1
            finalpage.show_pdf_page(fitz.Rect(0,0,612,792),betweenfinal)
            file_path = "labels.pdf"
            # file_path = "labels.pdf"
            # betweenfinal.save("moo.pdf")
            final.save(file_path)
            print(f"Label {labelsdone} processed")              

    print("Check labels.pdf for the labels and shippinglabels.pdf for the shipping labels")

uploaded_file = st.file_uploader("File upload", type="pdf",accept_multiple_files=True)
paths={}
master_file=fitz.open()
if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        for file in range(len(uploaded_file)):
            paths.update({f"{file}":{"path":os.path.join(temp_dir, uploaded_file[file].name)}})
            paths[f"{file}"].update({"file":uploaded_file[file]})
        # print(paths)
        # for file in uploaded_file:
        for path in paths:
            print(path)
            with open(paths[str(path)]["path"], "wb") as f:
                print(f)
                f.write(paths[str(path)]["file"].getvalue())
        for path in paths:
            with fitz.open(paths[str(path)]["path"]) as f:
                master_file.insert_pdf(f) 
                master_file.save("master.pdf")
        # # path = os.path.join(temp_dir, uploaded_file.name)
        # # with open(path, "wb") as f:
        # #         f.write(uploaded_file.getvalue())
        parse_file("master.pdf")
        with open ("labels.pdf","rb") as label:
            st.download_button(
                label="Download labels",
                data=label,
                file_name="labels.pdf"
            )
        with open("shipping.pdf","rb") as shippingdata:
            st.download_button(
                label="Download shipping info",
                data=shippingdata,
                file_name="shipping.pdf"
            )
        