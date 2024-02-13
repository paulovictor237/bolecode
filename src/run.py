import base64
import io
import json
from weasyprint import CSS, HTML
from barcode import Code128
from barcode.writer import ImageWriter

def read_file(filename):
    with open(filename, 'r') as file:
        return str(file.read())
    
def barcode_2_decode(barcode_data):
    code128 = Code128(barcode_data, writer=ImageWriter())
    fp = io.BytesIO()
    code128.write(fp,options={ 'module_width': 0.34, 'module_height': 15.0 })
    return base64.b64encode(fp.getvalue()).decode('utf-8')

def html_to_pdf(html, css):
    html = HTML(string=html)
    pdf_bytes = html.write_pdf(stylesheets=[CSS(css)], target='bolecode.pdf')
    # return base64.b64encode(pdf_bytes).decode('utf-8')

folder = 'src/assets/'
json_data = json.loads(read_file( 'src/assets/data.json'))["data"]

data = {
    "chave": json_data["dados_qrcode"]["chave"],
    "nome_cobranca": json_data["beneficiario"]["nome_cobranca"],
    "numero_cadastro_nacional_pessoa_juridica": json_data["beneficiario"]["tipo_pessoa"]["numero_cadastro_nacional_pessoa_juridica"],
    "data_emissao": json_data["dado_boleto"]["data_emissao"],
    "data_vencimento": json_data["dado_boleto"]["dados_individuais_boleto"][0]["data_vencimento"],
    "data_limite_pagamento": json_data["dado_boleto"]["dados_individuais_boleto"][0]["data_limite_pagamento"],
    "valor_titulo": json_data["dado_boleto"]["dados_individuais_boleto"][0]["valor_titulo"],
    "valor_total_titulo": json_data["dado_boleto"]["valor_total_titulo"],
    "codigo_boleto": json_data["dado_boleto"]["dados_individuais_boleto"][0]["codigo_barras"],
    "emv": json_data["dados_qrcode"]["emv"],
    "qr_code_base64": json_data["dados_qrcode"]["base64"],
    "barcode_base64": json_data["dado_boleto"]["dados_individuais_boleto"][0]["codigo_barras"],
}

data['barcode_base64'] = barcode_2_decode(data['barcode_base64'])
html_content = read_file(folder + 'index.html').format(**data)
html_to_pdf(html_content, folder + 'styles.css')
