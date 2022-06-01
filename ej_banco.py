import sqlite3
from sqlite3 import Error
import os

pasta_app = os.path.dirname(__file__)
nome_banco = pasta_app + "\\bd_ej.db"


class AppBD:
    def __init__(self):
        self.conn = None

    def abrir_conexao(self):
        try:
            self.conn = sqlite3.connect(nome_banco)
        except Error as e:
            print(e)
        return self.conn

    def dql(self, query):  # select
        vcon = self.abrir_conexao()
        c = vcon.cursor()
        c.execute(query)
        res = c.fetchall()
        vcon.close()
        return res

    def dml(self, query, d1, d2, d3):  # inserir, atualizar, deletar
        try:
            vcon = self.abrir_conexao()
            c = vcon.cursor()
            c.execute(query, (d1, d2, d3))
            vcon.commit()
            vcon.close()
        except Error as e:
            print(e)

    def excluir(self, query, d):
        try:
            vcon = self.abrir_conexao()
            c = vcon.cursor()
            c.execute(query, (d,))
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
#
# # criar_tabela(vcon, vsql)
#
# conexao = AppBD()
#
# criar_tabela(conexao.abrir_conexao(), vsql)
