from datetime import datetime, date

from parsers.notab3.helperfuncs import para_numero, para_data, tratar_financeiro

valor_mirae_2014 = {
        "secoes": {
            "dados_iniciais": {
                "marcacao": ("data pregão", 1, 0, 0, -1),
                "tipo": "normal",
                "dados": {
                    int: ["numero_nota"],
                },
                "execute": [
                    ("numero_nota", int)
                ]
            },
            "cliente": {
                "marcacao": ("cliente", 1, "agente de ", 0, -1),
                "tipo": "normal",
                "dados": {
                    "cpf": ["cpf_cliente"],
                },
                "execute": [
                ]
            },
            "negocios": {
                "marcacao": ("tipo mercado", 1, "resumo dos", 0, -1),
                "tipo": "colecao",
                "dados": {
                    str: [
                        "praca",
                        "c/v",
                        "tipo_mercado",
                        "titulo",
                        "titulo",
                        "titulo",
                        "obs",
                        "d/c"],
                    int: ["quantidade"],
                    float: ["preco", "valor"],
                },
                "execute": [
                    ("tipo_mercado", "upper"),
                    ("titulo", "upper"),
                    ("preco", para_numero),
                    ("quantidade", para_numero),
                ]
            },
            "liquido_para": {
                "marcacao": ("líquido para", 0, 0, "líquido para", -1),
                "tipo": "normal",
                "dados": {
                    date: ["data_liquidacao"]
                },
                "execute": [
                    ("data_liquidacao", para_data)
                ]
            },
            "resumo_financeiro": {
                "marcacao": ("resumo financeiro", 1, "(1)", "resumo financeiro", -1),
                "tipo": "chave_valor",
                "dados": {
                },
                "execute": [
                    ("resumo_financeiro", tratar_financeiro)
                ],
            }
        }
    }

mirae_2014 = {
    (datetime(2014, 1, 1).date(), datetime(2021, 1, 1).date(),
     "Mirae Asset"): valor_mirae_2014
}
