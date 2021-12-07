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
import io
import shutil
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from tqdm import tqdm

import tempfile



# Cmd line args
file =  sys.argv[1] #r'.\ActivityCoefficientsinHNO3-H2S04-H2OMixtures.pdf' #

lang = 'eng'
if len( sys.argv) > 2:
    lang = sys.argv[2]
# Check for and create img directory


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


tPath  = tempfile.TemporaryDirectory()


Merger = PdfFileWriter()



outputFile = open(file.replace('.pdf', '_OCR.pdf'), 'wb')
# Convert PDF pages to JPG images
print("Progress of " + file)

pdfRead =  PdfFileReader(file)
md = pdfRead.getPage(0).mediaBox

pages = convert_from_path(file, 100, fmt="jpeg", poppler_path = r"C:\Program Files\poppler-21.08.0\Library\bin" )
tqdm1 = tqdm(total=len(pages))
PagesPdf = []

for i, page in enumerate(pages):
    #page.save("images/page" + str(i) + ".png", 'PNG')
    imageObj =  Image.frombytes('RGB', page.size, page.tobytes())
    g = pytesseract.image_to_pdf_or_hocr(imageObj, lang =lang )
    #Merger.addPage(PdfFileReader( io.BytesIO( bytes(g) ) ) )
    #Merger.addPage(PdfFileReader( g ) )
    f = open(tPath.name + str(i) + ".pdf", mode='wb')
    f.write(g)
    f.close()
    PagesPdf.append(f.name)
    tqdm1.update()
tqdm1.clear()
tqdm1.close()

# If you don't have tesseract executable in your PATH, include the following:



merger = PdfFileWriter()
for pdf in PagesPdf:
    merger.addPage(PdfFileReader(pdf, 'rb').getPage(0))

f = open(file.replace('.pdf', '_OCR.pdf'), 'wb')
merger.write(f)
f.close()



# Clean img directory
shutil.rmtree(tPath.name)
print("Finished!")