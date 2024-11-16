from tkinter import *
from tkinter import ttk

import mysql.connector

import undetected_chromedriver as uc

from selenium import webdriver  
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from collections import Counter

import spacy

from fuzzywuzzy import process

import traceback

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys

class Aplicativo:
    def __init__(self):
        # Configuração da janela
        self.janela = Tk()
        self.janela.geometry("1280x720")
        self.janela.resizable(False, False)
        self.janela.title("CompanyInsight")
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_tudo)

        # Banco De Dados
        self.conexao = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'BancoDeDado123',
            database = 'projetoUnimar'
        )

        self.cursor = self.conexao.cursor()

        # Variaveis para o scraping
        self.produtos_conhecidos = []

        # Criação do Canvas e Frames do Aplicativo
        self.CanvasPrincipal = Canvas(self.janela)
        self.CanvasPrincipal.pack(fill='both', expand=True)

        self.Frames = []

        self.criarTelaInicial()

        self.janela.mainloop()

    def criarTelaInicial(self):
        self.FrameInicial = Frame(self.CanvasPrincipal, background="white")
        self.FrameInicial.pack(fill='both', expand=True)
        self.Frames.append(self.FrameInicial)

        self.Logo = Label(self.FrameInicial, text="Company Insight", font="Impact 54", foreground="black", background="white")
        self.Logo.place(relx=0.5, rely=0.4, anchor="center")

        self.CampoPesquisa = Entry(self.FrameInicial, width=45, font="24", background="#d5d7db", justify="center")
        self.CampoPesquisa.place(relx=0.5, rely=0.5, anchor="center")
        self.CampoPesquisa.focus_set()

        self.imagemBotaoPositivo = PhotoImage(file="T:\\Faculdade\\Projeto Ageis\\CompanyInsight\\Interface\\Botoes\\BotaoPositivo.png")
        self.PositivoBotao = Button(self.FrameInicial, image=self.imagemBotaoPositivo, relief="flat", background=self.FrameInicial.cget("bg"), activebackground=self.FrameInicial.cget("bg"), borderwidth=0, command=lambda: (self.destruirFrames(), self.criarTelaEmpresa("positivo")))
        self.PositivoBotao.place(relx=0.4, rely=0.65, anchor="center")

        self.imagemBotaoHabibs = PhotoImage(file="T:\\Faculdade\\Projeto Ageis\\CompanyInsight\\Interface\\Botoes\\BotaoHabibs.png")
        self.HabibsBotao = Button(self.FrameInicial, image=self.imagemBotaoHabibs, relief="flat", background=self.FrameInicial.cget("bg"), activebackground=self.FrameInicial.cget("bg"), borderwidth=0, command=lambda: (self.destruirFrames(), self.criarTelaEmpresa("habibs")))
        self.HabibsBotao.place(relx=0.6, rely=0.65, anchor="center")

    def criarTelaEmpresa(self, empresa):
        # Frames da Tela de Empresa
        self.FrameEmpresa = Frame(self.CanvasPrincipal, background="white")
        self.FrameEmpresa.pack(fill='both', expand=True)
        self.Frames.append(self.FrameEmpresa)

        # Pegando os dados de rankeamento para ser exibido no grafico
        self.cursor.execute(f"SELECT * FROM {empresa}_rank")
        resultadosRank = self.cursor.fetchall()

        self.listinhaRank = []
        self.listinhaProduto = []

        for resultado in resultadosRank:
            produto = resultado[1]
            quantidade = int(resultado[2])

            for _ in range(quantidade):
                self.listinhaRank.append(produto)
        
        self.contador_produtos = Counter(self.listinhaRank)
        self.ranking_produtos = self.contador_produtos.most_common()

        ranking_text = ""
        for index, (produto, quantidade) in enumerate(self.ranking_produtos[:5], start=1):
            ranking_text += f"{index}. {produto}\n"
            self.listinhaProduto.append(produto)

        produtos = [produto for produto, quantidade in self.ranking_produtos[:5]]
        quantidades = [quantidade for produto, quantidade in self.ranking_produtos[:5]]

        # Montando o grafico de pizza
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(quantidades, labels=produtos, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})

        ax.axis('equal')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.FrameEmpresa)
        canvas.draw()

        canvas_widget = canvas.get_tk_widget()

        canvas_widget.place(relx=0.25, rely=0.65, anchor="center", width=500, height=500)

        # Montando a tela
        self.NomeEmpresa = Label(self.FrameEmpresa, text=empresa.upper(), font="Impact 50", background=self.FrameEmpresa.cget("bg"))
        self.NomeEmpresa.place(relx=0.99, rely=0.0, anchor="ne")

        self.BotaoScrap = Button(self.FrameEmpresa, text="Fazer Scrapping", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaScrapping(empresa)))
        self.BotaoScrap.place(relx=0.5, rely=0.055, anchor="center")

        self.BotaoVoltar = Button(self.FrameEmpresa, text="Voltar", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaInicial()))
        self.BotaoVoltar.place(relx=0.04, rely=0.055, anchor="center")

        self.barrinhaBonita = Frame(self.FrameEmpresa, background="black", width=1280, height=3)
        self.barrinhaBonita.place(relx=0.5, rely=0.11, anchor="center")

        self.barrinhaBonita2 = Frame(self.FrameEmpresa, background="black", width=3, height=640)
        self.barrinhaBonita2.place(relx=0.5, rely=1, anchor="s")

        self.LabelzinhoRank = Label(self.FrameEmpresa, text="Rank Dos Mais Reclamados", font="Impact 18", background=self.FrameEmpresa.cget("bg"))
        self.LabelzinhoRank.place(relx=0.05, rely=0.2, anchor="w")

        self.Rank = Label(self.FrameEmpresa, text=ranking_text, font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.Rank.place(relx=0.05, rely=0.37, anchor="w")

        self.SeletorReclamacoes = ttk.Combobox(self.FrameEmpresa, values=self.listinhaProduto)
        self.SeletorReclamacoes.set(self.listinhaProduto[0])
        self.SeletorReclamacoes.bind("<<ComboboxSelected>>", lambda event: self.mudarTabela(self.SeletorReclamacoes.get()))
        self.SeletorReclamacoes.place(relx=0.75, rely=0.17, anchor="center")

        # Criando e colocando os dados da tabela de reclamações
        self.tree = ttk.Treeview(self.FrameEmpresa, columns=("Reclamações"), show='headings')
        self.tree.column("Reclamações", width=500)
        self.tree.heading("Reclamações", text="Reclamações".capitalize())
        self.tree.place(relx=0.75, rely=0.4, anchor="center")

        self.cursor.execute(f"SELECT motivo_reclamado FROM {empresa}")
        self.resultadosMotivoReclamacao = self.cursor.fetchall()
        self.cursor.execute(f"SELECT produto_reclamado FROM {empresa}")
        self.resultadosProdutoReclamado = self.cursor.fetchall()

        estilo = ttk.Style()
        estilo.configure("Treeview", rowheight=25)

        self.mudarTabela(self.SeletorReclamacoes.get())
    
    def mudarTabela(self, produto):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        motivos_inseridos = set()

        for motivo, produto_reclamado in zip(self.resultadosMotivoReclamacao, self.resultadosProdutoReclamado):
            if produto_reclamado[0] == produto:
                if motivo[0] != "None" and motivo[0] not in motivos_inseridos:
                    motivos_inseridos.add(motivo[0])
                    self.tree.insert("", "end", values=(motivo[0],))


    def criarTelaScrapping(self, empresa):
        self.FrameScrapping = Frame(self.CanvasPrincipal, background="white")
        self.FrameScrapping.pack(fill='both', expand=True)
        self.Frames.append(self.FrameScrapping)

        self.TextoInformativo = Label(self.FrameScrapping, text="Digite a quantidade de paginas que deseja!", font="Impact 45", background=self.FrameScrapping.cget("bg"))
        self.TextoInformativo.place(relx=0.5, rely=0.4, anchor="center")

        self.QuantidadePaginas = Entry(self.FrameScrapping, width=25, font="10", background="#d5d7db", justify="center")
        self.QuantidadePaginas.place(relx=0.5, rely=0.5, anchor="center")
        self.QuantidadePaginas.bind("<Return>", lambda event: self.fazerScrapping(empresa))

    def normalizar_produto(self, produto):
        produto = produto.lower()
        doc = self.IA(produto)
        
        lematizado = " ".join([token.lemma_ for token in doc])
        
        if not lematizado.strip():
            lematizado = produto

        if lematizado.endswith('s'):
            lematizado = lematizado.rstrip('s')
        
        resultado = process.extractOne(lematizado, self.produtos_conhecidos, score_cutoff=80)
        
        if resultado:
            produto_correspondente, similaridade = resultado
            return produto_correspondente
        else:
            self.produtos_conhecidos.append(lematizado)
        
        return lematizado
    
    def fazerScrapping(self, empresa):
        self.cursor.execute(f"SELECT produto_rank FROM {empresa}_rank")
        resultadosProdutosConhecidos = self.cursor.fetchall()

        for resultado in resultadosProdutosConhecidos:
            self.produtos_conhecidos.append(resultado)

        self.service = Service(ChromeDriverManager().install())  

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")

        self.driver = uc.Chrome(options=options)

        self.IA = spacy.load("Treinar IA/model-last") 

        self.produtos_reclamados = []

        self.dicionarioEmpresas = {
            "positivo" : "positivo-informatica",
            "habibs" : "habibs"
        }

        for pagina in range(int(self.QuantidadePaginas.get())):
            url = f"https://www.reclameaqui.com.br/empresa/{self.dicionarioEmpresas.get(empresa)}/lista-reclamacoes/?pagina={pagina + 1}"
            self.driver.get(url)
            
            try:
                WebDriverWait(self.driver, 20).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')) > 0)
                reclamacoes = self.driver.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')

                self.driver.execute_script("arguments[0].click();", reclamacoes[0])
                self.driver.get(url)
                
                for index in range(len(reclamacoes)):
                    try:
                        reclamacoes = self.driver.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')
                        reclamacao = reclamacoes[index]
                        
                        self.driver.execute_script("arguments[0].click();", reclamacao)

                        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-lzlu7c-3')))
                        
                        titulo = self.driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-3').text
                        reclamacao_texto = self.driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-17').text.replace('\n', ' ').replace('"', ' ').replace("'", ' ')
                        local_reclamacao = self.driver.find_elements(By.CLASS_NAME, 'sc-lzlu7c-6')[0].text
                        data_reclamacao = self.driver.find_elements(By.CLASS_NAME, 'sc-lzlu7c-6')[1].text
                        status_reclamacao = self.driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-18').text

                        produto_identificado = None
                        motivo_identificado = None

                        doc = self.IA(reclamacao_texto)
                        for ent in doc.ents:
                            if ent.label_ == "PRODUTO":
                                produto_identificado = ent.text
                                break

                        for ent in doc.ents:
                            if ent.label_ == "MOTIVO":
                                motivo_identificado = ent.text
                                break
                        
                        if produto_identificado:
                            produto_normalizado = self.normalizar_produto(produto_identificado)
                            self.produtos_reclamados.append(produto_normalizado)
                        
                        comando = f'INSERT INTO positivo (titulo_reclamacao, reclamacao, local_reclamacao, data_reclamacao, status_reclamacao, produto_reclamado, motivo_reclamado) VALUES ("{titulo}", "{reclamacao_texto}", "{local_reclamacao}", "{data_reclamacao}", "{status_reclamacao}", "{produto_normalizado}", "{motivo_identificado}")'
                        self.cursor.execute(comando)
                        self.conexao.commit()
                        
                        self.driver.get(url)
                        WebDriverWait(self.driver, 20).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')) > 0)
                    
                    except Exception as e:
                        print("Erro no processamento de uma reclamação:", e)
                        print(traceback.format_exc())
                        self.driver.get(url)
                        WebDriverWait(self.driver, 20).until(lambda d: len(d.find_elements(By.CLASS_NAME, 'sc-1pe7b5t-1')) > 0)

            except Exception as e:
                print("Erro ao acessar a página:", e)
                print(traceback.format_exc())
                self.driver.get(url)

        self.contador_produtos1 = Counter(self.produtos_reclamados)
        self.ranking_produtos1 = self.contador_produtos1.most_common()

        for produto, frequencia in self.ranking_produtos1:
            print(f"{produto}: {frequencia} reclamações")
            comando = f'''
                INSERT INTO positivo_rank (produto_rank, quantidade_rank) 
                VALUES ("{produto}", "{frequencia}") 
                ON DUPLICATE KEY UPDATE 
                quantidade_rank = quantidade_rank + {frequencia};
            '''
            self.cursor.execute(comando)
            self.conexao.commit()

        self.driver.quit()
        self.destruirFrames()
        self.criarTelaEmpresa(empresa)

    def destruirFrames(self):
        for frame in self.Frames:
            frame.destroy()

    def fechar_tudo(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.janela.destroy()
        sys.exit()

Aplicativo()