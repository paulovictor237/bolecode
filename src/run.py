import json
from PyPDF2 import PdfWriter
import base64
from PIL import Image
import io
import barcode
from barcode.writer import ImageWriter
from weasyprint import HTML, CSS

from data import format_data

class PDFGenerator:
    def write_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    def encode_decode(self, data):
        return base64.b64encode(data).decode('utf-8')
    
    def base64_2_decode(self, data):
        return base64.b64decode(data)

    def decode_2_pdf(self, decode):
        image = Image.open(io.BytesIO(decode))
        pdf_data = io.BytesIO()
        image.save(pdf_data, format="PDF")
        pdf_data.seek(0)
        return pdf_data.getvalue()

    def barcode_2_decode(self, barcode_data):
        EAN = barcode.get_barcode_class('ean13')
        my_ean = EAN(barcode_data, writer=ImageWriter())
        fp = io.BytesIO()
        my_ean.write(fp)
        return fp.getvalue()

    def merge_pdfs(self, *pdfs):
        pdf_writer = PdfWriter()
        for pdf in pdfs:
            pdf_writer.append(io.BytesIO(pdf))

        output_data = io.BytesIO()
        pdf_writer.write(output_data)

        return output_data.getvalue()

    def create_merged_pdf(self, qr_code):
        file_qr_code_pdf = self.decode_2_pdf(self.base64_2_decode(qr_code))
        file_barcode_pdf = self.decode_2_pdf(self.barcode_2_decode('5901234123457'))
        pdfs = [file_qr_code_pdf, file_barcode_pdf]
        result = self.merge_pdfs(*pdfs)
        self.write_file(result, "result.pdf")

pdf = PDFGenerator()

qr_code = "iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6AQAAAACgl2eQAAACy0lEQVR4Xu2XS3LlIBAE4SJw/1v4KHARmMzG9vssHLOw2hthj54l0hHl7qpGU/bP66O8P3lbN3DWDZx1A2f9HzBKqXuu0lfrq/tZ+oyHecDke7S6Ope5WuncVh9mAt6OosDG5uZ21cOkAqNPRBYeRqFa/wMAgX2wU6obUbpcgG/80tzctm37Gc/TAP0539e7q9/3fxlwmRWqhVuiaxjnrCwAnyCpa1Z+3ESngLSAsgCMijrkrU/n6p5piPKAPZqqkNqH/7rt6+th2gRAkTu2SqNI1WrBvP4VVwPqWZEXumWJgLfpyQOWLql2B7HLXvlbx7hZAFmhTJwoXpA3h8l5alYCQEmwKY0C6GeKxgGTCRxd7Di7JCnc9DYRiKHFWcKlWSBEvoY3AdAy7GAagOIBZ2piqKQBhpUC2SuwUyxWKhDBjSvmVXCdNsr9NMBbSzMdI+00jXEaGc4CLEsNrzLDzE/8gtc8gPkZM2uq9mt6OFYSAdyqS7RKjRTHeJdOBNS2fdn1UPHlfyvyKbzXA7xsntPUo5W8EN64/RaZAKArXDJ0jbYxyi8D5HrA7kxPlUqz6FO4GNk1EbA1PF8O8DhdXWA9EVgIcmYso4PkuKo8E6gGltERh/vQOPulWQkAfUKkJSruBNWNbyJgTM1MlIp++R9Df+iJQAgrehWNbvHxOc3SAEQxMjRsCOwRoh6ezQN4GrMLt9Kv1U50n9J9PUBV4lAzPaWa4vh6NCsDwKHGBWlRJmkqVh/JSgCKscEpFoz0tDBOexJ5PYBAm7Q92hkjpkbBT+G9HnAZXvoT5eqENyZZIhCKhlZxjtO4Fu+969u0CYAWoUq4hGcRmKHIlgrYJRJLrZCrVeprs5IA4mta6RAV21G8h2mzAM+TM8y27iE67ucBwfBuE2cKep1hztVEwM4wR1FIv2Jw0LtupvOAn9YNnHUDZ93AWb8A/AN4HAw5z2fBbAAAAABJRU5ErkJggg=="
base64_string = pdf.encode_decode(pdf.barcode_2_decode('5901234123457'))

folder = 'src/assets/'

# Ler o conteúdo do arquivo template.html
with open(folder + 'index.html', 'r') as file:
    html_content = file.read()
    
with open(folder +  "data.json", 'r') as file:
        json_data = json.load(file)

# Substituir as variáveis no conteúdo HTML
html_content = html_content.replace('{{ qr_code_base64 }}', qr_code)
html_content = html_content.replace('{{ barcode_base64 }}', base64_string)

html_content = format_data(html_content,json_data)

# Convertendo o HTML para PDF com WeasyPrint
html = HTML(string=html_content)
html.write_pdf(target='bolecode.pdf', stylesheets=[CSS(folder + 'styles2.css')])
# html.write_pdf(target='bolecode.pdf')
