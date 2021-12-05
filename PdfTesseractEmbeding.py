# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:50:49 2021

@author: jarl.robert.pedersen

Usage:
PdtTesseractEmbedding.py "<path/to/file>" "<3 letter language code>"

Example:
PdtTesseractEmbedding.py "C:\Scans\Document_inNorwegian.pdf" "nor"
PdtTesseractEmbedding.py "C:\Scans\Document_inEnglish.pdf"

"""

from PIL import Image
import pytesseract
import sys
import os
import shutil
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from tqdm import tqdm




"""
with io.open(path, mode="rb") as f:
    input_pdf = PdfFileReader(f)
    media_box = input_pdf.getPage(0).mediaBox

min_pt = media_box.lowerLeft
max_pt = media_box.upperRight

pdf_width = max_pt[0] - min_pt[0]
pdf_height = max_pt[1] - min_pt[1]
"""



# Cmd line args
file =  sys.argv[1] #r'.\ActivityCoefficientsinHNO3-H2S04-H2OMixtures.pdf' #

lang = 'eng'
if len( sys.argv) > 2:
    lang = sys.argv[2]
# Check for and create img directory
imgDirectory = os.getcwd() + "/images"
try:
    os.stat(imgDirectory)
except:
    os.mkdir(imgDirectory)   

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


F = open(file, "rb")
InputPDF = PdfFileReader(F)
OutputPDF = PdfFileWriter()

for page_i in range(InputPDF.getNumPages()):
    OutputPDF.addPage(pytesseract.image_to_pdf_or_hocr(InputPDF.getPage(page_i).mediabox, lang =lang ))

F.close()
G = open(file.replace('.pdf', '_OCR.pdf'), 'wb')

OutputPDF.write(G)
G.close()


"""
# Convert PDF pages to JPG images
print("Converting PDF pages to PNG images...")
pages = convert_from_path(file, 100, poppler_path = r"C:\Program Files\poppler-21.09.0\Library\bin" )
tqdm1 = tqdm(total=len(pages))
for i, page in enumerate(pages):
    page.save("images/page" + str(i) + ".png", 'PNG')
    tqdm1.update()
tqdm1.clear()
tqdm1.close()
PagesPdf = []
# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


print("tesseract scanning:")
# For each page...
for i in tqdm( range(0, len(pages)) ):
    #print("Scanning page", i+1)

    # Convert JPG to PDF page
    f = open("images/page" + str(i) + ".pdf", mode='wb')
    f.write(pytesseract.image_to_pdf_or_hocr(Image.open("images/page" + str(i) + ".png"), lang =lang ))
    f.close()
    PagesPdf.append(f.name)

merger = PdfFileWriter()
for pdf in PagesPdf:
    merger.addPage(PdfFileReader(pdf, 'rb').getPage(0))

f = open(file.replace('.pdf', '_OCR.pdf'), 'wb')
merger.write(f)
f.close()



# Clean img directory
shutil.rmtree(imgDirectory)
"""
"""
print("Cleaning Images Directory...")
for filename in os.listdir(imgDirectory):
    file_path = os.path.join(imgDirectory, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
"""
print("Finished!")





'''


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
#print(pytesseract.image_to_string(Image.open('.\\test.png')))


f = open('out.pdf', mode='wb', )
f.write(pytesseract.image_to_pdf_or_hocr(Image.open('.\\test.png'), extension='pdf'))
f.close()


'''
