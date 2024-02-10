def format_data(html_content, json_data):
    boleto_params = extract_boleto_params(json_data["data"])
    pix_params = extract_pix_params(json_data["data"])
    data = parameters(pix_params,boleto_params)
    return html_content.format(**data)

def extract_boleto_params(data):
    return {
        "beneficiario": {
            "nome_cobranca": data["beneficiario"]["nome_cobranca"],
            "tipo_pessoa": data["beneficiario"]["tipo_pessoa"]["codigo_tipo_pessoa"],
            "numero_cadastro_nacional_pessoa_juridica": data["beneficiario"]["tipo_pessoa"]["numero_cadastro_nacional_pessoa_juridica"],
            "endereco": {
                "nome_logradouro": data["beneficiario"]["endereco"]["nome_logradouro"],
                "nome_bairro": data["beneficiario"]["endereco"]["nome_bairro"],
                "nome_cidade": data["beneficiario"]["endereco"]["nome_cidade"],
                "sigla_UF": data["beneficiario"]["endereco"]["sigla_UF"],
                "numero_CEP": data["beneficiario"]["endereco"]["numero_CEP"]
            }
        },
        "dado_boleto": {
            "descricao_instrumento_cobranca": data["dado_boleto"]["descricao_instrumento_cobranca"],
            "tipo_boleto": data["dado_boleto"]["tipo_boleto"],
            "pagador": {
                "nome_pessoa": data["dado_boleto"]["pagador"]["pessoa"]["nome_pessoa"],
                "tipo_pessoa": data["dado_boleto"]["pagador"]["pessoa"]["tipo_pessoa"]["codigo_tipo_pessoa"],
                "numero_cadastro_pessoa_fisica": data["dado_boleto"]["pagador"]["pessoa"]["tipo_pessoa"]["numero_cadastro_pessoa_fisica"],
                "endereco": {
                    "nome_logradouro": data["dado_boleto"]["pagador"]["endereco"]["nome_logradouro"],
                    "nome_bairro": data["dado_boleto"]["pagador"]["endereco"]["nome_bairro"],
                    "nome_cidade": data["dado_boleto"]["pagador"]["endereco"]["nome_cidade"],
                    "sigla_UF": data["dado_boleto"]["pagador"]["endereco"]["sigla_UF"],
                    "numero_CEP": data["dado_boleto"]["pagador"]["endereco"]["numero_CEP"]
                },
                "pagador_eletronico_DDA": data["dado_boleto"]["pagador"]["pagador_eletronico_DDA"],
                "praca_protesto": data["dado_boleto"]["pagador"]["praca_protesto"]
            },
            "codigo_carteira": data["dado_boleto"]["codigo_carteira"],
            "valor_total_titulo": data["dado_boleto"]["valor_total_titulo"],
            "data_emissao": data["dado_boleto"]["data_emissao"],
            "data_vencimento": data["dado_boleto"]["dados_individuais_boleto"][0]["data_vencimento"],
            "valor_titulo": data["dado_boleto"]["dados_individuais_boleto"][0]["valor_titulo"],
            "numero_linha_digitavel": data["dado_boleto"]["dados_individuais_boleto"][0]["numero_linha_digitavel"],
            "data_limite_pagamento": data["dado_boleto"]["dados_individuais_boleto"][0]["data_limite_pagamento"]
        },
        "dados_qrcode": {
            "chave": data["dados_qrcode"]["chave"],
            "txid": data["dados_qrcode"]["txid"],
            "id_location": data["dados_qrcode"]["id_location"],
            "location": data["dados_qrcode"]["location"]
        }
    }

def extract_pix_params(data):
    return {
        "chave": data["dados_qrcode"]["chave"],
        "txid": data["dados_qrcode"]["txid"],
        "id_location": data["dados_qrcode"]["id_location"],
        "location": data["dados_qrcode"]["location"],
        "emv": data["dados_qrcode"]["emv"],
        "base64": data["dados_qrcode"]["base64"]
    }

    
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def parameters(pix_params, boleto_params):
    flattened_pix_params = flatten_dict(pix_params)
    flattened_boleto_params = flatten_dict(boleto_params)
    return {**flattened_pix_params, **flattened_boleto_params}
