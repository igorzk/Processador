import re
from datetime import datetime, date


def para_numero(item: str) -> float:
    num = item.replace(".", "").replace(",", ".")
    return float(num)


def testa_cpf(item: str) -> bool:
    return bool(re.match('[0-9]{3}.[0-9]{3}.[0-9]{3}.[0-9]{2}', item))


def testa_num_ver(item: str) -> bool:
    return re.match('[^"]*[0-9]-[0-9][^"]*', item) and item.replace("-", "").isnumeric()


def testa_data(item: str) -> bool:
    return bool(re.match('[0-9]{2}/[0-9]{2}/[0-9]{4}', item))


def para_data(item: str) -> date:
    return datetime.strptime(item, '%d/%m/%Y').date()


def remove_brancos_consecutivos(texto: str) -> str:
    return re.sub('  +', '  ', texto.replace("\t", " "))


def update(x, key, func):
    if isinstance(func, str):
        x.update({key: getattr(x[key], func)()})
    else:
        x.update({key: func(x[key])})


def extrai_tipo(item: str) -> any:
    if testa_data(item):
        return date
    if testa_cpf(item):
        return "cpf"
    if testa_num_ver(item):
        return "num_ver"
    if item.isnumeric():
        return int
    try:
        float(item)
        return float
    except ValueError:
        try:
            para_numero(item)
            return float
        except ValueError:
            if item.replace(' ', 'a').translate(
                    str.maketrans({"-": '', "/": '', "&": '', ".": ''})).isalnum():
                return str


def tratar_negocios(negocios):
    novo_negocios = {}
    for negocio in negocios:
        negocio.pop("obs", None)
        negocio.pop("praca", None)
        negocio.pop("d/c", None)
        negocio.pop("valor", None)
        mult = 1
        cv = negocio["c/v"]
        if cv == "v":
            mult = -1
        negocio["quantidade"] = mult * negocio["quantidade"]
        del negocio["c/v"]
        chave_op = cv + negocio["titulo"] + negocio["tipo_mercado"]
        if chave_op in novo_negocios:
            novo_negocios[chave_op]["quantidade"] += negocio["quantidade"]
        else:
            novo_negocios[chave_op] = negocio
    return list(novo_negocios.values())


def tratar_financeiro(dados):
    novos_dados = {}
    for key, value in dados.items():
        if isinstance(value, str):
            if extrai_tipo(value) in (int, float):
                numero = para_numero(value)
            else:
                continue
        else:
            num, op = value
            if '$' in num:
                numero = para_numero(op)
            else:
                if op == 'd':
                    mult = -1
                else:
                    mult = 1
                numero = mult * para_numero(num)
        new_key = key
        if re.match(r"total[^']+", new_key) or "numnota" in new_key:
            continue
        if "i.r.r.f" in new_key:
            new_key = "irrf"
            if numero > 0:
                numero = -numero
        elif "líquido para" in new_key or re.match(r"ara\s+[0-9]{2}/[0-9]{2}/[0-9]{3}", new_key):
            new_key = "valor_total"
        elif "iss" in new_key:
            new_key = "iss"
        elif "ana" in new_key.replace(".", ""):
            new_key = "taxa_ana"
        elif "líquido das operações" in new_key:
            new_key = "liquido_operacoes"
        new_key = new_key.replace(" de ", "_").replace("ç", "c").\
            replace("ã", "a").replace("/", "_").replace("õ", "o")
        novos_dados[new_key] = numero
    if "irrf" not in novos_dados:
        novos_dados["irrf"] = 0
    return novos_dados


def sanity_check(dados):
    if not testa_cpf(dados["cpf_cliente"]):
        raise ValueError
    if not isinstance(dados["data_liquidacao"], date):
        raise ValueError
    if "numero_nota" not in dados or "valor_total" not in dados["resumo_financeiro"]:
        raise ValueError
    total_operacoes = 0.0
    for negocio in dados["negocios"]:
        total_operacoes += negocio["quantidade"] * negocio["preco"]
    if not abs(total_operacoes + dados["resumo_financeiro"]["liquido_operacoes"]) < 0.01:
        raise ValueError
    chaves_permitidas = (
        "corretagem",
        "emolumentos",
        "iss",
        "liquido_operacoes",
        "outras",
        "taxa_ana",
        "taxa_liquidacao",
        "taxa_registro",
        "taxa_termo_opcoes",
        "valor_total",
        "irrf"
    )
    for item in dados["resumo_financeiro"].keys():
        if item not in chaves_permitidas:
            raise ValueError
