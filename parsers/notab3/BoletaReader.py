from pprint import pprint

from .helperfuncs import remove_brancos_consecutivos, testa_data, para_data, extrai_tipo, update, tratar_negocios, \
    sanity_check
from .corretoras import readers


class BoletaReader:
    def __init__(self, txt: str):
        txt = txt.replace('\xad', "-")
        txt = '\n'.join(list(filter(lambda x: not x.strip() == '', txt.split('\n'))))
        txt = txt.lower()
        self.__txt = txt.split('\n')
        self.__readers = readers
        self.__props = {
            "corretora": BoletaReader.extrair_corretora(txt).title(),
            "data_operacao": BoletaReader.extrair_data(self.__txt)}
        self.__reader = self.extrair_reader(
            self.__props["data_operacao"], self.__props["corretora"]
        )

    def read(self):
        secoes = self.__reader["secoes"]
        for nome_secao, secao in secoes.items():
            segmento_secao = self.__extrair_secao(secao)
            dados = BoletaReader.extrair_dados(
                segmento_secao, secao["tipo"], secao["dados"], nome_secao
            )
            for key, func in secao["execute"]:
                if len(dados) == 1 and isinstance(list(dados.values())[0], list):
                    for item in dados[list(dados.keys())[0]]:
                        update(item, key, func)
                else:
                    update(dados, key, func)
            self.__props.update(dados)
        if "suj" in self.__props:
            del self.__props["suj"]
        self.__props["negocios"] = tratar_negocios(self.__props["negocios"])
        sanity_check(self.__props)
        return self.__props

    def __extrair_secao(self, secao):
        marcador, linha_ini, marca_fim, col_marca_ini, col_marca_fim = \
            secao["marcacao"]
        for i, linha in enumerate(self.__txt):
            if marcador in linha:
                li = i + linha_ini
                ci = None
                cf = None
                if isinstance(marca_fim, int):
                    lf = li + marca_fim + 1
                else:
                    lf = i
                    while marca_fim not in self.__txt[lf]:
                        lf += 1
                if isinstance(col_marca_ini, int):
                    if not col_marca_ini == 0:
                        ci = col_marca_ini
                else:
                    j = i
                    while col_marca_ini not in self.__txt[j]:
                        j += 1
                    ci = self.__txt[j].index(col_marca_ini)
                if isinstance(col_marca_fim, int):
                    if not col_marca_fim == -1:
                        cf = col_marca_fim
                else:
                    j = i
                    while col_marca_fim not in self.__txt[j]:
                        j += 1
                    cf = self.__txt[j].index(col_marca_fim) + len(col_marca_fim)
                return [self.__txt[i][ci:cf] for i in range(li, lf)]

    @staticmethod
    def extrair_dados(segmento, tipo, dados_esperados, nome_secao):
        dados_tipados = {}
        dados = {}
        if tipo == "normal":
            items = remove_brancos_consecutivos('  '.join(segmento)).split('  ')
            for item in items:
                tipo = extrai_tipo(item)
                if tipo in dados_tipados:
                    dados_tipados[tipo].append(item)
                else:
                    dados_tipados[tipo] = [item]
            return BoletaReader.extrair_dados_tipados(dados_tipados, dados_esperados)
        elif tipo == "colecao":
            colecao = []
            for linha in segmento:
                dados_tipados = {}
                items = remove_brancos_consecutivos(linha).split('  ')
                for item in items:
                    tipo = extrai_tipo(item)
                    if tipo in dados_tipados:
                        dados_tipados[tipo].append(item)
                    else:
                        dados_tipados[tipo] = [item]
                colecao.append(BoletaReader.extrair_dados_tipados(dados_tipados, dados_esperados))
            dados = {nome_secao: colecao}
        elif tipo == "chave_valor":
            colecao = {}
            for linha in segmento:
                items = remove_brancos_consecutivos(linha).strip()
                items = items.split('  ')
                if items[-2:] != [items[0]]:
                    if len(items) == 2:
                        colecao.update({items[0]: items[1]})
                    else:
                        colecao.update({items[0]: items[-2:]})
            dados[nome_secao] = colecao
            return dados
        return dados

    @staticmethod
    def extrair_dados_tipados(dados_tipados, dados_esperados):
        dados = {}
        for tipo_dado in dados_tipados:
            if tipo_dado in dados_esperados:
                for i, chave in enumerate(dados_esperados[tipo_dado]):
                    if chave in dados and isinstance(dados[chave], str):
                        dados[chave] += ' ' + str(dados_tipados[tipo_dado][i])
                    else:
                        dados[chave] = dados_tipados[tipo_dado][i]
        return dados

    def extrair_reader(self, data, corretora):
        for data1, data2, corretora_reader in self.__readers:
            if data1 <= data <= data2 and corretora == corretora_reader:
                return readers[data1, data2, corretora_reader]

    @staticmethod
    def extrair_corretora(txt: str):
        corretoras = ["socopa", "mirae asset", "clear sa", "caixa"]
        for corretora in corretoras:
            if corretora in txt:
                return corretora

    @staticmethod
    def extrair_data(txt):
        marcador_data = ["data pregão", ]
        for i, linha in enumerate(txt):
            for marcador in marcador_data:
                if marcador in linha:
                    linha_com_data = \
                        remove_brancos_consecutivos(txt[i + 1]).split(' ')
                    for item in linha_com_data:
                        if testa_data(item):
                            return para_data(item)
