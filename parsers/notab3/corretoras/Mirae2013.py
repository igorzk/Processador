from datetime import datetime
import copy
import re

from parsers.notab3.helperfuncs import para_numero
from .Mirae2014 import valor_mirae_2014

valor_mirae_2013 = copy.deepcopy(valor_mirae_2014)

valor_mirae_2013["secoes"].update({
    "cliente": {
        "marcacao": ("cliente", 0, "agente de ", 0, -1),
        "tipo": "normal",
        "dados": {
            int: ["suj", "cpf_cliente"],
        },
        "execute": [
            ("cpf_cliente", lambda x: '.'.join(re.findall('...', x[:-2])) + '-' + x[-2:])
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
                "obs",
            ],
            int: ["quantidade"],
            float: ["preco", "valor"],
        },
        "execute": [
            ("tipo_mercado", "upper"),
            ("titulo", "upper"),
            ("preco", para_numero),
            ("quantidade", para_numero),
        ]
    }
})

mirae_2013 = {
    (datetime(2013, 1, 1).date(), datetime(2013, 12, 31).date(),
     "Mirae Asset"): valor_mirae_2013
}
