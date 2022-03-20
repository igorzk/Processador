from datetime import datetime
import copy

from parsers.notab3.helperfuncs import para_data
from .Mirae2014 import valor_mirae_2014

valor_socopa_2013 = copy.deepcopy(valor_mirae_2014)

valor_socopa_2013["secoes"]["negocios"].update({"dados": {
    str: [
        "praca",
        "c/v",
        "tipo_mercado",
        "titulo",
        "titulo",
        "d/c"],
    int: ["quantidade"],
    float: ["preco", "valor"],
}})

valor_socopa_2013["secoes"]["liquido_para"].update(
    {"dados":
        {
            str: ["data_liquidacao"]
        },
        "execute":
            [
                ("data_liquidacao", lambda x: x.split()[-1]),
                ("data_liquidacao", para_data)
            ]
    })

socopa_2013 = {
    (datetime(2013, 1, 1).date(), datetime(2014, 12, 31).date(),
     "Socopa"): valor_socopa_2013
}
