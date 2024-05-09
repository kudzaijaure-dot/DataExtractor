from flask import jsonify
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import PIL.Image
import pikepdf
import io
import base64

app = Flask(__name__)

# def image_to_base64(image):
#     # Convert an image (PIL Image object) to base64
#     buffered = io.BytesIO()
#     image.save(buffered, format="PNG")  # You can choose other formats if needed
#     return base64.b64encode(buffered.getvalue()).decode("utf-8")
#
# @app.route('/post-images-pdf', methods=['POST'])
# def upload_document():
#     # Check if the post request has the file part
#     if 'document' not in request.files:
#         return 'No file part', 400
#
#     file = request.files['document']
#
#     # If the user does not select a file, the browser submits an
#     # empty file without a filename.
#     if file.filename == '':
#         return 'No selected file', 400
#
#     start_page = request.form.get('start_page', type=int)
#     end_page = request.form.get('end_page', type=int)
#
#     if start_page is None or end_page is None:
#         return 'Please provide both start_page and end_page parameters', 400
#
#     pdf_data = file.read()
#
#     # Create a PDF document from the in-memory data
#     pdf_document = pikepdf.Pdf.open(io.BytesIO(pdf_data))
#
#     if pdf_document:
#
#         counter = 1
#         container = []
#         # #
#         for i in range(start_page - 1, min(end_page, len(pdf_document.pages))):
#             page = pdf_document.pages[i]
#             #
#             for img_ref in page.images.keys():
#                 img_stream = page.images[img_ref]
#                 img = pikepdf.PdfImage(img_stream)
#                 img_base64 = image_to_base64(img.as_pil_image())  # Convert to base64
#                 container.append(img_base64)
#                 counter += 1
#         # #
#         # # json.dumps(img)
#         # #
#         # #
#         return jsonify(container)
#
#     return 'Something went wrong with image upload', 500
#
# #
# @app.route('/post-text-pdf', methods=['POST'])
# def upload_text():
#     # Check if the post request has the file part
#     if 'document' not in request.files:
#         return 'No file part', 400
#
#     file = request.files['document']
#
#     # If the user does not select a file, the browser submits an
#     # empty file without a filename.
#     if file.filename == '':
#         return 'No selected file', 400
#
#     pdf_data = file.read()
#
#     from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#     from pdfminer.converter import TextConverter
#     from pdfminer.layout import LAParams
#     from pdfminer.pdfpage import PDFPage
#     from io import BytesIO
#
#     def create_in_memory_pdf(pdf_data):
#         # Initialize PDFMiner components
#         rsrcmgr = PDFResourceManager()
#         retstr = BytesIO()
#         codec = 'utf-8'
#         laparams = LAParams()
#         device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#
#         # Create a PDF document from the in-memory data
#         fp = BytesIO(pdf_data)
#         interpreter = PDFPageInterpreter(rsrcmgr, device)
#         password = ""  # Set the password if needed
#         maxpages = 0
#         caching = True
#         pagenos = set()
#
#         # Process each page
#         for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
#                                       check_extractable=True):
#             interpreter.process_page(page)
#
#         # Get the extracted text
#         text = retstr.getvalue()
#
#         # Clean up
#         device.close()
#         retstr.close()
#
#         return text
#  # Assuming you already read the PDF data from the uploaded file
#     in_memory_text = create_in_memory_pdf(pdf_data)
#     decoded_text = in_memory_text.decode('utf-8')
#
#     if(decoded_text):
#         return jsonify(decoded_text)
#     else:
#         return 'Failed to extract text', 500

#
@app.route('/post-tables-pdf', methods=['POST'])
def upload_tables():
    # Check if the post request has the file part
    if 'document' not in request.files:
        return 'No file part', 400

    file = request.files['document']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file', 400

    pdf_data = file.read()


    # Create a PDF document from the in-memory data
    pdf_document = pikepdf.Pdf.open(io.BytesIO(pdf_data))

    #
    if pdf_document:
        import tempfile

    #
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Define the file path for saving the PDF
        pdf_file_path = os.path.join(temp_dir, "temporary.pdf")
    #
    #
        pdf_document.save(pdf_file_path)


        from tabula import read_pdf

        tables = read_pdf(pdf_file_path, output_format="json", multiple_tables=True, pages=all)

        if(tables):
            return 'success', 200


        # return "success"
    return  "Error with table extraction", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=22)

