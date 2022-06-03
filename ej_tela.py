"""
Name: EJ Cadastros
Version: 4.0
Description: este sistema é para cadastro de produtos no BD sqlite3
Author: Eduardo Brandão <eduardo.ads1814@gmail.com> (https://github.com/EduardoBran)

V2.0 - Adicionado opções de pesquisar por código e deletar por código
     - Mudança da fonte dos subtítulos
     - Alteração da ordem de exibição dos produtos na TreeView (ordenação por código)

V3.0 - Adicionado a opção de excluir todos os produtos da lista
     - Adicionado o botão sobre
     - Alterações no tamanho dos botões e espaçamento entre as labels.

V4.0 - Limpando os campos de digitação de atualizar e pesquisar.
     - Adicionado condição para que o campo 'Nome' não inicie ou tenha somente números
     - Adicionando lógica para substituir caracteres especiais e acentos.
     - A remoção de acentos foi baseada em uma pesquisa no GitHub:
       https://gist.github.com/boniattirodrigo/67429ada53b7337d2e79
     - Adicionado messagebox informando que inserido/atualizado produto
     - Adicionado messagebox perguntando/confirmando a exclusão de um produto
     - Adicionado messagebox informando que deletou um todos os produtos
     - Deixando as primeiras letras de cada string como maiúscula
     - Removendo espaços em branco do código e preço de Inserir e Atualizar produtos
     - Correção Bug ao atualizar campo nome

V5.0 - Correção para impedir que a adição de produtos com mesmos códigos
     - Se o cliente adicionar um código já existente, o mesmo será substituído na lista.
     - Adicionado opção de checkbox para a ordenação
"""

from ej_banco import AppBD
import sqlite3
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import Error
import re
import unicodedata


def verifica_nome(n):
    if n == "":
        return False
    try:
        int(n)
        return True
    except ValueError as e:
        if n[0].isdigit():
            return True
        return False


def removerAcentosECaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub('[^a-zA-Z0-9 \\\]', '', palavra_sem_acento)


def sobre():
    messagebox.showinfo(title='SOBRE', message=f'Desenvolvido por: Eduardo Brandão e Jonata Gomes')
    return


def sair():
    res = messagebox.askyesno('ATENÇÃO', 'Tem certeza de que quer sair de EJ Cadastros ?')
    if res:
        sys.exit()
    return


class JanelaPrincipal:
    def __init__(self, janela):
        self.objBD = AppBD()

        ############ Tela TreeView

        quadro_grid = LabelFrame(app, text='Produtos')
        quadro_grid.configure(font=("Courier", 10, "italic"))
        quadro_grid.pack(fill='both', expand="yes", padx=10, pady=10)

        self.scroll = ttk.Scrollbar(quadro_grid)
        self.scroll.pack(side='right', fill='y')

        self.tv = ttk.Treeview(quadro_grid, columns=('id', 'codigo', 'nome', 'preco'), show='headings',
                               yscrollcommand=self.scroll.set)

        self.tv.column('id', minwidth=0, width=70)
        self.tv.column('codigo', minwidth=0, width=120)
        self.tv.column('nome', minwidth=0, width=340)
        self.tv.column('preco', minwidth=0, width=120)
        self.tv.heading('id', text='ID')
        self.tv.heading('codigo', text='CÓDIGO')
        self.tv.heading('nome', text='NOME')
        self.tv.heading('preco', text='PREÇO')

        self.scroll.config(command=self.tv.yview)

        self.tv.pack()
        self.popular()

        ############ Tela INSERIR

        quadro_inserir = LabelFrame(app, text='Inserir Novos Produtos')
        quadro_inserir.configure(font=("Courier", 10, "italic"))
        quadro_inserir.pack(fill='both', expand='yes', padx=10, pady=10)

        lb_codigo = Label(quadro_inserir, text='Código')
        lb_codigo.pack(side='left', padx=10)
        self.v_codigo = Entry(quadro_inserir, width=7)
        self.v_codigo.pack(side='left', padx=10)
        lb_nome = Label(quadro_inserir, text='Nome', padx=20)
        lb_nome.pack(side='left')
        self.v_nome = Entry(quadro_inserir)
        self.v_nome.pack(side='left', padx=10)
        lb_preco = Label(quadro_inserir, text='Preço', padx=20)
        lb_preco.pack(side='left')
        self.v_preco = Entry(quadro_inserir)
        self.v_preco.pack(side='left', padx=10)

        btn_inserir = Button(quadro_inserir, text='Inserir', command=self.inserir, width=12, height=2)
        btn_inserir.pack(side='right', padx=10)

        ############ Tela ATUALIZAR

        quadro_att = LabelFrame(app, text='Atualizar Produtos')
        quadro_att.configure(font=("Courier", 10, "italic"))
        quadro_att.pack(fill='both', expand='yes', padx=10, pady=10)

        lb_id_att = Label(quadro_att, text='Id')
        lb_id_att.pack(side='left', padx=23)
        self.v_id_att = Entry(quadro_att, width=7)
        self.v_id_att.pack(side='left', padx=10)
        lb_codigo_att = Label(quadro_att, text='Código', padx=17)
        lb_codigo_att.pack(side='left')
        self.v_codigo_att = Entry(quadro_att, width=7)
        self.v_codigo_att.pack(side='left', padx=10)
        lb_nome_att = Label(quadro_att, text='Nome', padx=17)
        lb_nome_att.pack(side='left')
        self.v_nome_att = Entry(quadro_att)
        self.v_nome_att.pack(side='left', padx=10)
        lb_preco_att = Label(quadro_att, text='Preço', padx=17)
        lb_preco_att.pack(side='left')
        self.v_preco_att = Entry(quadro_att, width=9)
        self.v_preco_att.pack(side='left', padx=10)

        btn_att = Button(quadro_att, text='Atualizar', command=self.atualizar, width=12, height=2)
        btn_att.pack(side='right', padx=10)

        ############ Tela PESQUISAR

        quadro_pesquisar = LabelFrame(app, text='Pesquisar Produtos')
        quadro_pesquisar.configure(font=("Courier", 10, "italic"))
        quadro_pesquisar.pack(fill='both', expand='yes', padx=10, pady=10)

        lb_nome_pesquisar = Label(quadro_pesquisar, text='Por nome:', width=8)
        lb_nome_pesquisar.pack(side='left', padx=4)
        self.v_nome_pesquisar = Entry(quadro_pesquisar)
        self.v_nome_pesquisar.pack(side='left')
        btn_pesquisar = Button(quadro_pesquisar, text='Pesquisar', command=lambda: self.pesquisar(1), width=7,
                               height=1)
        btn_pesquisar.pack(side='left', padx=12)

        lb_cod_pesquisar = Label(quadro_pesquisar, text='Por código:')
        lb_cod_pesquisar.pack(side='left')
        self.v_cod_pesquisar = Entry(quadro_pesquisar, width=7)
        self.v_cod_pesquisar.pack(side='left', padx=7)
        btn_pesquisar = Button(quadro_pesquisar, text='Pesquisar', command=lambda: self.pesquisar(2), width=7,
                               height=1)
        btn_pesquisar.pack(side='left', padx=10)

        btn_mostrar_todos = Button(quadro_pesquisar, text='Mostrar todos', command=self.popular_tv, width=12,
                                   height=2)
        btn_mostrar_todos.pack(side='right', padx=10)

        lb_nome_esp = Label(quadro_pesquisar, text='', width=3)
        lb_nome_esp.pack(side='left')

        lb_nome_ordenar = Label(quadro_pesquisar, text='Ordenar por:', width=14)
        lb_nome_ordenar.pack(side='left')
        lista_ordenar = ['Id', 'Código', 'Nome', 'Preço']

        self.cb_lista = ttk.Combobox(quadro_pesquisar, values=lista_ordenar, width=9)
        self.cb_lista.set("Id")  # definindo a primeira opção a vir marcada
        self.cb_lista.pack(side='right', padx=3)

        ############ Tela DELETAR

        quadro_deletar = LabelFrame(app, text='Deletar Produtos')
        quadro_deletar.configure(font=("Courier", 10, "italic"))
        quadro_deletar.pack(fill='both', expand='yes', padx=10, pady=10)

        lb_id_deletar = Label(quadro_deletar, text='Por Id:')
        lb_id_deletar.pack(side='left', padx=10)
        self.v_id_del = Entry(quadro_deletar)
        self.v_id_del.pack(side='left', padx=10)
        btn_deletar_id = Button(quadro_deletar, text='Deletar', command=lambda: self.deletar(1), width=7, height=1)
        btn_deletar_id.pack(side='left', padx=10)

        lb_esp = Label(quadro_deletar, text='')
        lb_esp.pack(side='left', padx=16)

        lb_cod_deletar = Label(quadro_deletar, text='Por código:')
        lb_cod_deletar.pack(side='left')
        self.v_cod_del = Entry(quadro_deletar, width=7)
        self.v_cod_del.pack(side='left', padx=7)
        btn_deletar_cod = Button(quadro_deletar, text='Deletar', command=lambda: self.deletar(2), width=7,
                                 height=1)
        btn_deletar_cod.pack(side='left', padx=10)
        btn_deletar_cod = Button(quadro_deletar, text='Deletar TODOS', command=lambda: self.deletar(3), width=12,
                                 height=2)
        btn_deletar_cod.pack(side='right', padx=10)

        ############ Tela INFO

        quadro_info = LabelFrame(app, text='Info')
        quadro_info.configure(font=("Courier", 10, "italic"))
        quadro_info.pack(fill='both', expand='yes', padx=10, pady=10)

        btn_sobre = Button(quadro_info, text='SOBRE', command=sobre, width=11, height=2)
        btn_sobre.pack(side='left', padx=200)

        btn_sair = Button(quadro_info, text='SAIR', command=sair, width=11, height=2)
        btn_sair.pack(side='left')

    ############ POPULANDO A TREE VIEW

    def popular(self):  # AQUI
        self.tv.delete(*self.tv.get_children())
        v_query = "SELECT * FROM tb_ej_produtos order by I_CODIGOPRODUTO"
        linhas = self.objBD.dql(v_query)

        for i in linhas:
            self.tv.insert("", "end", values=i)

    ############ POPULANDO A TREE VIEW COM CHECK BOX

    def popular_tv(self):  # AQUI
        self.tv.delete(*self.tv.get_children())

        ve = self.cb_lista.get()

        if ve == 'Id':
            v_query = "SELECT * FROM tb_ej_produtos order by N_IDPRODUTO"
            linhas = self.objBD.dql(v_query)
        if ve == 'Código':
            v_query = "SELECT * FROM tb_ej_produtos order by I_CODIGOPRODUTO"
            linhas = self.objBD.dql(v_query)
        if ve == 'Nome':
            v_query = "SELECT * FROM tb_ej_produtos order by T_NOMEPRODUTO"
            linhas = self.objBD.dql(v_query)
        if ve == 'Preço':
            v_query = "SELECT * FROM tb_ej_produtos order by F_PRECOPRODUTO"
            linhas = self.objBD.dql(v_query)

        for i in linhas:
            self.tv.insert("", "end", values=i)

    ############ CRUD INSERIR

    def inserir(self):
        if self.v_codigo.get() == "" or self.v_nome.get() == "" or self.v_preco.get() == "":
            messagebox.showinfo(title='ERRO', message="Digite todos os dados.")
            return

        if verifica_nome(self.v_nome.get()):
            messagebox.showinfo(title='ERRO',
                                message='Nome inválido. \n\nSobre campo "Nome":\n\n- Não pode conter somente números.\n- Não pode iniciar com caracter numérico.\n- Caracteres especiais serão removidos automaticamente.')
            return

        nome = self.v_nome.get()
        nome = removerAcentosECaracteresEspeciais(nome).title()

        if nome == "":
            messagebox.showinfo(title='ERRO',
                                message='Nome inválido. O nome não deve possuir caracteres especiais.')
            return

        codigo = self.v_codigo.get().replace(" ", "")
        preco = self.v_preco.get().replace(" ", "")

        try:
            v_query = f"INSERT or REPLACE INTO tb_ej_produtos " \
                      f"(I_CODIGOPRODUTO, T_NOMEPRODUTO, F_PRECOPRODUTO) " \
                      f"VALUES (?, ?, ?)"
            self.objBD.dml(v_query, codigo, nome, float(preco))

            self.popular()
            messagebox.showinfo(title='CONCLUÍDO', message=f'O produto {nome} foi adicionado com sucesso.')
        except Error as e:
            messagebox.showinfo(title='ERRO', message=f'Erro ao inserir. Erro -> {e}')
            return
        except ValueError as e:
            messagebox.showinfo(title='ERRO',
                                message=f'Os valores de código e/ou preço precisam ser NUMÉRICOS.')
            return

        self.v_codigo.delete(0, END)
        self.v_nome.delete(0, END)
        self.v_preco.delete(0, END)
        self.v_codigo.focus()

    ############ CRUD ATUALIZAR

    def atualizar(self):
        try:
            vid = self.v_id_att.get()
            r = self.objBD.dql(f"SELECT * FROM tb_ej_produtos WHERE N_IDPRODUTO={vid}")
            rcodigo = int(r[0][1])
            rnome = r[0][2]
            rpreco = float(r[0][3])

            vcodigo = self.v_codigo_att.get()
            vnome = self.v_nome_att.get()
            vpreco = self.v_preco_att.get()

        except IndexError as e:
            messagebox.showinfo(title='ERRO', message=f'Id inexistente.')
            return
        except sqlite3.OperationalError as e:
            messagebox.showinfo(title='ERRO', message=f'Id não especificado.')
            return
        except Exception as e:
            messagebox.showinfo(title='ERRO', message=f'Error -> {e}')
            return

        if len(vcodigo) == 0:
            vcodigo = int(rcodigo)
        if len(vnome) == 0:
            vnome = rnome
        if len(vpreco) == 0:
            vpreco = float(rpreco)

        vnome = removerAcentosECaracteresEspeciais(vnome).title()

        if verifica_nome(self.v_nome_att.get()):
            messagebox.showinfo(title='ERRO',
                                message='Nome inválido. \n\nSobre campo "Nome":\n\n- Não pode conter somente números.'
                                        '\n- Não pode iniciar com caracter numérico.'
                                        '\n- Caracteres especiais serão removidos automaticamente.')
            return
        if vnome == "":
            messagebox.showinfo(title='ERRO',
                                message='Nome inválido. O nome não deve possuir caracteres especiais.')
            return

        try:
            v_query = f"UPDATE " \
                      f"tb_ej_produtos SET I_CODIGOPRODUTO=?, T_NOMEPRODUTO=?, F_PRECOPRODUTO=? WHERE N_IDPRODUTO={vid}"
            self.objBD.dml(v_query, int(vcodigo), vnome, float(vpreco))

            self.popular()
            messagebox.showinfo(title='CONCLUÍDO',
                                message=f'O produto de id {self.v_id_att.get()} foi atualizado com sucesso.')
        except ValueError as e:
            messagebox.showinfo(title='ERRO', message=f'Os valores de código e/ou preço precisam ser NUMÉRICOS.')
            return
        except Error as e:
            messagebox.showinfo(title='ERRO', message=f'Error -> {e}')
            return

        self.v_id_att.delete(0, END)
        self.v_codigo_att.delete(0, END)
        self.v_nome_att.delete(0, END)
        self.v_preco_att.delete(0, END)
        self.v_id_att.focus()
        return

    ############ CRUD PESQUISAR

    def pesquisar(self, t):
        self.tv.delete(*self.tv.get_children())

        if t == 1:
            v_query = F"SELECT * FROM tb_ej_produtos WHERE T_NOMEPRODUTO LIKE '%{self.v_nome_pesquisar.get()}%'"
            linhas = self.objBD.dql(v_query)
            for i in linhas:
                self.tv.insert("", "end", values=i)
            self.v_nome_pesquisar.delete(0, END)

        if t == 2:
            v_query = F"SELECT * FROM tb_ej_produtos WHERE I_CODIGOPRODUTO LIKE '%{self.v_cod_pesquisar.get()}%'"
            linhas = self.objBD.dql(v_query, )
            for i in linhas:
                self.tv.insert("", "end", values=i)
            self.v_cod_pesquisar.delete(0, END)
        return

    ############ CRUD DELETAR

    def deletar(self, t):
        if t == 1:
            ve_id = self.v_id_del.get()
            if ve_id == "":
                messagebox.showinfo(title='ERRO', message=f'Por favor especifique o ID a ser deletado.')
                return
            try:
                res = messagebox.askyesno('ATENÇÃO', f'Tem certeza de que deseja deletar o produto de ID {ve_id} ?')
                if res:
                    v_query = f"DELETE FROM tb_ej_produtos WHERE N_IDPRODUTO=? "
                    self.objBD.excluir(v_query, ve_id)

                    self.popular()
            except Error as e:
                messagebox.showinfo(title='ERRO', message=f'Erro ao deletar. Error -> {e}')
            self.v_id_del.delete(0, END)

        if t == 2:
            ve_cod = self.v_cod_del.get()
            if ve_cod == "":
                messagebox.showinfo(title='ERRO', message=f'Por favor especifique o ID a ser deletado.')
                return
            try:
                res = messagebox.askyesno('ATENÇÃO',
                                          f'Tem certeza de que deseja deletar o produto de código {ve_cod} ?')
                if res:
                    v_query = f"DELETE FROM tb_ej_produtos WHERE I_CODIGOPRODUTO=? "
                    self.objBD.excluir(v_query, ve_cod)

                    self.popular()

            except Error as e:
                messagebox.showinfo(title='ERRO', message=f'Erro ao deletar. Error -> {e}')
            self.v_cod_del.delete(0, END)

        if t == 3:
            try:
                res = messagebox.askyesno('ATENÇÃO', 'Tem certeza de que deseja deletar TODOS os produtos ?')
                if res:
                    v_query = f"DELETE FROM tb_ej_produtos"
                    conn = self.objBD.abrir_conexao()
                    cursor = conn.cursor()
                    cursor.execute(v_query)
                    conn.commit()

                    self.popular()
                    messagebox.showinfo(title='CONCLUÍDO', message='TODOS os produtos foram deletados.')
            except Error as e:
                messagebox.showinfo(title='ERRO', message=f'Erro ao deletar todos. Error -> {e}')
                return
        return


if __name__ == '__main__':
    app = Tk()
    janela_principal = JanelaPrincipal(app)
    app.title('EJ Cadastros (v5.0)')
    app.geometry('820x710')
    app.mainloop()

    # ##### CONSULTA
    #
    # def consulta(self, v):
    #     r = self.objBD.dql(f"SELECT * FROM tb_ej_produtos")
    #     r_tam = len(r)
    #     lista_c = []
    #
    #     for i in range(r_tam):
    #         lista_c.append(r[i][1])
    #     v = int(v)
    #     if v in lista_c:
    #         messagebox.showinfo(title='ERRO',
    #                             message=f'Já existe um produto com o código {v} nesta lista.')
    #         return True
    #     return False
