import sqlite3
from sqlite3 import Error
import os

pasta_app = os.path.dirname(__file__)
nome_banco = pasta_app + "\\produtos.db"


def ConexaoBanco():
    con = None
    try:
        con = sqlite3.connect(nome_banco)
    except Error as e:
        print(e)
    return con


vcon = ConexaoBanco()


def dql(query):  # select
    vcon = ConexaoBanco()
    c = vcon.cursor()
    c.execute(query)
    res = c.fetchall()
    vcon.close()
    return res


def dml(query):  # inserir, atualizar, deletar
    try:
        vcon = ConexaoBanco()
        c = vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    except Error as e:
        print(e)


# def criar_tabela(conexao, sql):
#     try:
#         c = conexao.cursor()
#         c.execute(sql)
#         print('Tabela criada')
#     except Error as e:
#         print(e)
#
#
# vsql = """
#     CREATE TABLE tb_produtos(
#         N_IDPRODUTO INTEGER PRIMARY KEY AUTOINCREMENT,
#         T_CODIGOPRODUTO TEXT(10) UNIQUE,
#         T_NOMEPRODUTO VARCHAR(30),
#         F_PRECOPRODUTO FLOAT
#     );
# """

# criar_tabela(vcon, vsql)
