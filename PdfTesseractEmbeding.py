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
from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from tqdm import tqdm




"""
creds: https://gist.github.com/gstorer/f6a9f1dfe41e8e64dcf58d07afa9ab2a
"""

"""
import struct
from collections import namedtuple
import io

PdfImage = namedtuple('PdfImage', ['data', 'format','image_name'])

def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
    # http://www.fileformat.info/format/tiff/corion.htm
    fields = 8
    tiff_header_struct = '<' + '2s' + 'H' + 'L' + 'H' + 'HHLL' * fields + 'L'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little indian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       fields,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       # StripOffsets, LONG, 1, len of header
                       273, 4, 1, struct.calcsize(tiff_header_struct),
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, length
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )


def extract_images_from_pdf_page(xObject):
    image_list = []

    xObject = xObject['/Resources']['/XObject'].getObject()

    for obj in xObject:
        o = xObject[obj]
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            # getData() does not work for CCITTFaxDecode or DCTDecode
            # as of 1 Aug 2018. Not sure about JPXDecode.
            data = xObject[obj]._data
            
            color_space = xObject[obj]['/ColorSpace']
            if '/FlateDecode' in xObject[obj]['/Filter']:
                if isinstance(color_space, pdf.generic.ArrayObject) and color_space[0] == '/Indexed':
                    color_space, base, hival, lookup = [v.getObject() for v in color_space] # pg 262
                mode = img_modes[color_space]

                data = xObject[obj].getData() # need to use getData() here
                img = Image.frombytes(mode, size, data)
                if color_space == '/Indexed':
                    img.putpalette(lookup.getData())
                    img = img.convert('RGB')
                imgByteArr = io.BytesIO()
                img.save(imgByteArr,format='PNG')
                image_list.append(PdfImage(data=imgByteArr,
                                   format='PNG',
                                   image_name=obj[1:]))
                    
            elif '/DCTDecode' in xObject[obj]['/Filter']:
                image_list.append(PdfImage(data=io.BytesIO(data),
                                   format='JPG',
                                   image_name=obj[1:]))
            elif '/JPXDecode' in xObject[obj]['/Filter']:
                image_list.append(PdfImage(data=io.BytesIO(data),
                                   format='JP2',
                                   image_name=obj[1:]))
            elif '/CCITTFaxDecode' in xObject[obj]['/Filter']:
                if xObject[obj]['/DecodeParms']['/K'] == -1:
                    CCITT_group = 4
                else:
                    CCITT_group = 3
                data = xObject[obj]._data 
                img_size = len(data)
                tiff_header = tiff_header_for_CCITT(
                    size[0], size[1], img_size, CCITT_group)
                im = Image.open(io.BytesIO(tiff_header + data))

                if xObject[obj].get('/BitsPerComponent') == 1:
                    # experimental condition
                    # http://users.fred.net/tds/leftdna/sciencetiff.html
                    im = ImageOps.flip(im)

                imgByteArr = io.BytesIO()
                img.save(imgByteArr,format='PNG')
                image_list.append(PdfImage(data=imgByteArr,
                                   format='PNG',
                                   image_name=obj[1:]))
            else:
                print ('Unhandled image type: {}'.format(xObject[obj]['/Filter']))
        else:
            image_list += extract_images_from_pdf_page(xObject[obj])
    
    return image_list


"""




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
file =  r'.\TEST.pdf'  # sys.argv[1] #r'.\ActivityCoefficientsinHNO3-H2S04-H2OMixtures.pdf' #

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


"""

F = open(file, "rb")
InputPDF = PdfFileReader(F)
OutputPDF = PdfFileWriter()

for page_i in range(InputPDF.getNumPages()):
    if (InputPDF.getPage(page_i).extractText() != None):
        listImages = extract_images_from_pdf_page(InputPDF.getPage(page_i))
        OutputPDF.addPage(pytesseract.image_to_pdf_or_hocr(InputPDF.getPage(page_i).mediaBox, lang =lang ))
    else:
        OutputPDF.addPage(InputPDF.getPage(page_i))

F.close()
G = open(file.replace('.pdf', '_OCR.pdf'), 'wb')

OutputPDF.write(G)
G.close()
"""
import io
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


Merger = PdfFileWriter()



outputFile = open(file.replace('.pdf', '_OCR.pdf'), 'wb')
# Convert PDF pages to JPG images
print("Progress of " + file)
pages = convert_from_path(file, 100, poppler_path = r"C:\Program Files\poppler-21.08.0\Library\bin" )
tqdm1 = tqdm(total=len(pages))
for i, page in enumerate(pages):
    #page.save("images/page" + str(i) + ".png", 'PNG')
    imageObj =  Image.frombytes('RGB', page.size, page.tobytes())
    g = pytesseract.image_to_pdf_or_hocr(imageObj, lang =lang )
    Merger.addPage(PdfFileReader( io.BytesIO( bytes(g) ) ) )
    tqdm1.update()
tqdm1.clear()
tqdm1.close()
PagesPdf = []
# If you don't have tesseract executable in your PATH, include the following:




outputFile

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
