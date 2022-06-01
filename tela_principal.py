"""
Name: EJ Cadastros
Version: 1.0
Description: este sistema é para cadastro de produtos no BD sqlite3
Author: Eduardo Brandão <eduardo.ads1814@gmail.com> (https://github.com/EduardoBran)

V2.0 - Adicionado opções de pesquisar por código e deletar por código
     - Mudança da fonte dos subtítulos
     - Alteração da ordem de exibição dos produtos na TreeView (ordenação por código)

V3.0 - Adicionado a opção de excluir todos os produtos da lista
     - Adicionado o botão sobre
     - Alterações no tamanho dos botões e espaçamento entre as labels.
<<<<<<< HEAD

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

     AVISAR QUE PRODUTO NÃO FOI DELETADO,
     TRATAR PARA NAO REPETIR CAMPO CÓDIGOS

     ALTERAR ORDEM DE PESQUISAR PRODUTOS:
     Por Id [    ]    Por Código [    ]   Por nome [      ]

     CRIAR SUBTITULO ORDENAÇÃO
     [ORDERNAR POR ID] [ORDERNADOR POR CODIGO] [ORDERNAR POR NOME] [MOSTRAR TODOS]
=======
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
"""

import sqlite3
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import Error
from banco import dql, dml


def popular():
    tv.delete(*tv.get_children())
    v_query = "SELECT * FROM tb_produtos order by N_IDPRODUTO"
    linhas = dql(v_query)

    for i in linhas:
        tv.insert("", "end", values=i)


<<<<<<< HEAD
def verifica_nome(t):
    if t == 1:
        try:
            int(v_nome.get())
            return True
        except ValueError as e:
            if v_nome.get()[0].isdigit():
                return True
            return False

    if t == 2:
        if v_nome_att.get() == "":
            return False
        try:
            int(v_nome_att.get())
            return True
        except ValueError as e:
            if v_nome_att.get()[0].isdigit():
                return True
            return False


def removerAcentosECaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub('[^a-zA-Z0-9 \\\]', '', palavra_sem_acento)


=======
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
def inserir():
    if v_codigo.get() == "" or v_nome.get() == "" or v_preco.get() == "":
        messagebox.showinfo(title='ERRO', message="Digite todos os dados")
        return

    try:
        v_query = f"INSERT INTO tb_produtos (T_CODIGOPRODUTO, T_NOMEPRODUTO, F_PRECOPRODUTO) VALUES ('{int(v_codigo.get())}','{v_nome.get()}', '{float(v_preco.get())}')"
        dml(v_query)
<<<<<<< HEAD
        messagebox.showinfo(title='CONCLUÍDO', message=f'O produto {nome} foi adicionado com sucesso.')
    except sqlite3.IntegrityError as e:
        print('erro inter')
=======
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
    except Error as e:
        messagebox.showinfo(title='ERRO', message=f'Erro ao inserir. Erro -> {e}')
        return
    except ValueError as e:
<<<<<<< HEAD
        messagebox.showinfo(title='ERRO',
                            message=f'Os valores de código e/ou preço precisam ser NUMÉRICOS e sem espaço.')
=======
        messagebox.showinfo(title='ERRO', message=f'Os valores de código e/ou preço precisam ser NUMÉRICOS')
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
        return

    popular()
    v_codigo.delete(0, END)
    v_nome.delete(0, END)
    v_preco.delete(0, END)
    v_codigo.focus()


def atualizar():
    try:
        vid = v_id_att.get()
        r = dql(f"SELECT * FROM tb_produtos WHERE N_IDPRODUTO={vid}")
        rcodigo = int(r[0][1])
        rnome = r[0][2]
        rpreco = float(r[0][3])

        vcodigo = v_codigo_att.get()
        vnome = v_nome_att.get()
        vpreco = v_preco_att.get()

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

<<<<<<< HEAD
    vnome = removerAcentosECaracteresEspeciais(vnome).title()

    if verifica_nome(2):
        messagebox.showinfo(title='ERRO',
                            message='Nome inválido. \n\nSobre campo "Nome":\n\n- Não pode conter somente números.\n- Não pode iniciar com caracter numérico.\n- Caracteres especiais serão removidos automaticamente.')
        return

=======
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
    try:
        v_query = f"UPDATE tb_produtos SET T_CODIGOPRODUTO='{int(vcodigo)}', T_NOMEPRODUTO='{vnome}', F_PRECOPRODUTO='{float(vpreco)}' WHERE N_IDPRODUTO={vid}"
    except ValueError as e:
        messagebox.showinfo(title='ERRO', message=f'Os valores de código e/ou preço precisam ser NUMÉRICOS')
        return
    except Error as e:
        messagebox.showinfo(title='ERRO', message=f'Error -> {e}')
        return

<<<<<<< HEAD
    v_id_att.delete(0, END)
    v_codigo_att.delete(0, END)
    v_nome_att.delete(0, END)
    v_preco_att.delete(0, END)
    v_id_att.focus()
    popular()
    return
=======
    dml(v_query)
    popular()
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)


def pesquisar(t):
    tv.delete(*tv.get_children())

    if t == 1:
        v_query = F"SELECT * FROM tb_produtos WHERE T_NOMEPRODUTO LIKE '%{v_nome_pesquisar.get()}%'"
        linhas = dql(v_query)
        for i in linhas:
            tv.insert("", "end", values=i)
        return

    if t == 2:
        v_query = F"SELECT * FROM tb_produtos WHERE T_CODIGOPRODUTO LIKE '%{v_cod_pesquisar.get()}%'"
        linhas = dql(v_query)
        for i in linhas:
            tv.insert("", "end", values=i)
        return


def deletar(t):
    if t == 1:
        ve_id = v_id_del.get()
        if ve_id == "":
            messagebox.showinfo(title='ERRO', message=f'Por favor especifique o ID a ser deletado.')
            return
        try:
            v_query = f"DELETE FROM tb_produtos WHERE N_IDPRODUTO={ve_id} "
            dml(v_query)
        except Error as e:
            messagebox.showinfo(title='ERRO', message=f'Erro ao deletar. Error -> {e}')
        popular()
        v_id_del.delete(0, END)

    if t == 2:
        ve_cod = v_cod_del.get()
        if ve_cod == "":
            messagebox.showinfo(title='ERRO', message=f'Por favor especifique o ID a ser deletado.')
            return
        try:
            v_query = f"DELETE FROM tb_produtos WHERE T_CODIGOPRODUTO={ve_cod} "
            dml(v_query)
        except Error as e:
            messagebox.showinfo(title='ERRO', message=f'Erro ao deletar. Error -> {e}')
        popular()
        v_cod_del.delete(0, END)

    if t == 3:
        try:
            res = messagebox.askyesno('ATENÇÃO', 'Tem certeza de que quer deletar TODOS os produtos ?')
            if res == True:
                v_query = f"DELETE FROM tb_produtos"
                dml(v_query)
<<<<<<< HEAD
                messagebox.showinfo(title='CONCLUÍDO', message='TODOS os produtos foram deletados.')
=======
            else:
                return
>>>>>>> parent of e0e28bb (Add novas condicoes para inserir ou att dados, add novas message box)
        except Error as e:
            messagebox.showinfo(title='ERRO', message=f'Erro ao deletar todos. Error -> {e}')
            return
        popular()
    return

def sobre():
    messagebox.showinfo(title='SOBRE', message=f'Desenvolvido por: Eduardo Brandão e Jonata Gomes')
    return


def sair():
    res = messagebox.askyesno('ATENÇÃO', 'Tem certeza de que quer sair de EJ Cadastros ?')
    if res == True:
        sys.exit()
    return


######################################################### JANELA

app = Tk()
app.title('EJ Cadastros (v3.0)')
app.geometry('820x720')

######################################################### TreeView

quadro_grid = LabelFrame(app, text='Produtos')
quadro_grid.configure(font=("Courier", 10, "italic"))
quadro_grid.pack(fill='both', expand="yes", padx=10, pady=10)

scroll = ttk.Scrollbar(quadro_grid)
scroll.pack(side='right', fill='y')

tv = ttk.Treeview(quadro_grid, columns=('id', 'codigo', 'nome', 'preco'), show='headings', yscrollcommand=scroll.set)

tv.column('id', minwidth=0, width=70)
tv.column('codigo', minwidth=0, width=120)
tv.column('nome', minwidth=0, width=340)
tv.column('preco', minwidth=0, width=120)
tv.heading('id', text='ID')
tv.heading('codigo', text='CÓDIGO')
tv.heading('nome', text='NOME')
tv.heading('preco', text='PREÇO')

scroll.config(command=tv.yview)

tv.pack()
popular()

######################################################### INSERIR

quadro_inserir = LabelFrame(app, text='Inserir Novos Produtos')
quadro_inserir.configure(font=("Courier", 10, "italic"))
quadro_inserir.pack(fill='both', expand='yes', padx=10, pady=10)

lb_codigo = Label(quadro_inserir, text='Código')
lb_codigo.pack(side='left', padx=10)
v_codigo = Entry(quadro_inserir, width=7)
v_codigo.pack(side='left', padx=10)
lb_nome = Label(quadro_inserir, text='Nome', padx=20)
lb_nome.pack(side='left')
v_nome = Entry(quadro_inserir)
v_nome.pack(side='left', padx=10)
lb_preco = Label(quadro_inserir, text='Preço', padx=20)
lb_preco.pack(side='left')
v_preco = Entry(quadro_inserir)
v_preco.pack(side='left', padx=10)

btn_inserir = Button(quadro_inserir, text='Inserir', command=inserir, width=12, height=2)
btn_inserir.pack(side='right', padx=10)

######################################################### ATUALIZAR

quadro_att = LabelFrame(app, text='Atualizar Produtos')
quadro_att.configure(font=("Courier", 10, "italic"))
quadro_att.pack(fill='both', expand='yes', padx=10, pady=10)

lb_id_att = Label(quadro_att, text='Id')
lb_id_att.pack(side='left', padx=23)
v_id_att = Entry(quadro_att, width=7)
v_id_att.pack(side='left', padx=10)
lb_codigo_att = Label(quadro_att, text='Código', padx=17)
lb_codigo_att.pack(side='left')
v_codigo_att = Entry(quadro_att, width=7)
v_codigo_att.pack(side='left', padx=10)
lb_nome_att = Label(quadro_att, text='Nome', padx=17)
lb_nome_att.pack(side='left')
v_nome_att = Entry(quadro_att)
v_nome_att.pack(side='left', padx=10)
lb_preco_att = Label(quadro_att, text='Preço', padx=17)
lb_preco_att.pack(side='left')
v_preco_att = Entry(quadro_att, width=9)
v_preco_att.pack(side='left', padx=10)

btn_att = Button(quadro_att, text='Atualizar', command=atualizar, width=12, height=2)
btn_att.pack(side='right', padx=10)

#########################################################  PESQUISAR

quadro_pesquisar = LabelFrame(app, text='Pesquisar Produtos')
quadro_pesquisar.configure(font=("Courier", 10, "italic"))
quadro_pesquisar.pack(fill='both', expand='yes', padx=10, pady=10)

lb_nome_pesquisar = Label(quadro_pesquisar, text='Por nome:')
lb_nome_pesquisar.pack(side='left', padx=4)
v_nome_pesquisar = Entry(quadro_pesquisar)
v_nome_pesquisar.pack(side='left', padx=2)
btn_pesquisar = Button(quadro_pesquisar, text='Pesquisar', command=lambda: pesquisar(1), width=7, height=1)
btn_pesquisar.pack(side='left', padx=20)

lb_esp = Label(quadro_pesquisar, text='')
lb_esp.pack(side='left', padx=10)

lb_cod_pesquisar = Label(quadro_pesquisar, text='Por código:')
lb_cod_pesquisar.pack(side='left')
v_cod_pesquisar = Entry(quadro_pesquisar, width=7)
v_cod_pesquisar.pack(side='left', padx=7)
btn_pesquisar = Button(quadro_pesquisar, text='Pesquisar', command=lambda: pesquisar(2), width=7, height=1)
btn_pesquisar.pack(side='left', padx=10)

btn_mostrar_todos = Button(quadro_pesquisar, text='Mostrar Todos', command=popular, width=12, height=2)
btn_mostrar_todos.pack(side='right', padx=10)

#########################################################  DELETAR

quadro_deletar = LabelFrame(app, text='Deletar Produtos')
quadro_deletar.configure(font=("Courier", 10, "italic"))
quadro_deletar.pack(fill='both', expand='yes', padx=10, pady=10)

lb_id_deletar = Label(quadro_deletar, text='Por Id:')
lb_id_deletar.pack(side='left', padx=10)
v_id_del = Entry(quadro_deletar)
v_id_del.pack(side='left', padx=10)
btn_deletar_id = Button(quadro_deletar, text='Deletar', command=lambda: deletar(1), width=7, height=1)
btn_deletar_id.pack(side='left', padx=10)

lb_esp = Label(quadro_deletar, text='')
lb_esp.pack(side='left', padx=16)

lb_cod_deletar = Label(quadro_deletar, text='Por código:')
lb_cod_deletar.pack(side='left')
v_cod_del = Entry(quadro_deletar, width=7)
v_cod_del.pack(side='left', padx=7)
btn_deletar_cod = Button(quadro_deletar, text='Deletar', command=lambda: deletar(2), width=7, height=1)
btn_deletar_cod.pack(side='left', padx=10)

btn_deletar_cod = Button(quadro_deletar, text='Deletar TODOS', command=lambda: deletar(3), width=12, height=2)
btn_deletar_cod.pack(side='right', padx=10)

#########################################################  SOBRE / SAIR
quadro_info = LabelFrame(app, text='Info')
quadro_info.configure(font=("Courier", 10, "italic"))
quadro_info.pack(fill='both', expand='yes', padx=10, pady=10)

btn_sobre = Button(quadro_info, text='SOBRE', command=sobre, width=11, height=2)
btn_sobre.pack(side='left', padx=200)

btn_sair = Button(quadro_info, text='SAIR', command=sair, width=11, height=2)
btn_sair.pack(side='left')

app.mainloop()
