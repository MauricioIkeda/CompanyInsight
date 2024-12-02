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
import os

from dotenv import load_dotenv

class Aplicativo:
    def __init__(self):
        # Configuração da janela
        self.janela = Tk()
        self.janela.geometry("1280x720")
        self.janela.resizable(False, False) 
        self.janela.title("CompanyInsight")
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_tudo)

        # Carregando dados importantes
        load_dotenv()

        # Caminho Do Programa
        self.base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

        # Carregando os dados do banco de dados para se conectar
        HOST = os.getenv("HOST")
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        DATABASE = os.getenv("DATABASE")

        try:
            self.conexao = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            print("Conexão bem sucedida")
        except mysql.connector.Error as err:
            print(f"Erro na conexão do banco de dados {err}")

        self.cursor = self.conexao.cursor()

        # Variáveis para o scraping
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

        # "Logo" do programa
        self.Logo = Label(self.FrameInicial, text="Company Insight", font="Impact 54", foreground="black", background="white")
        self.Logo.place(relx=0.5, rely=0.4, anchor="center")

        # Campo de pesquisa
        self.CampoPesquisa = Entry(self.FrameInicial, width=45, font="24", background="#d5d7db", justify="center")
        self.CampoPesquisa.place(relx=0.5, rely=0.5, anchor="center")
        self.CampoPesquisa.focus_set()

        # Caminho das imagens
        imagem_botao_positivo = os.path.join(self.base_path, 'Interface', 'Botoes', 'BotaoPositivo.png')
        imagem_botao_habibs = os.path.join(self.base_path, 'Interface', 'Botoes', 'BotaoHabibs.png')

        # Botão Positivo
        self.imagemBotaoPositivo = PhotoImage(file=imagem_botao_positivo)
        self.PositivoBotao = Button(self.FrameInicial, image=self.imagemBotaoPositivo, relief="flat", background=self.FrameInicial.cget("bg"), activebackground=self.FrameInicial.cget("bg"), borderwidth=0, command=lambda: (self.destruirFrames(), self.criarTelaEmpresa("positivo")))
        self.PositivoBotao.place(relx=0.4, rely=0.65, anchor="center")

        # Botão Habibs
        self.imagemBotaoHabibs = PhotoImage(file=imagem_botao_habibs)
        self.HabibsBotao = Button(self.FrameInicial, image=self.imagemBotaoHabibs, relief="flat", background=self.FrameInicial.cget("bg"), activebackground=self.FrameInicial.cget("bg"), borderwidth=0, command=lambda: (self.destruirFrames(), self.criarTelaEmpresa("habibs")))
        self.HabibsBotao.place(relx=0.6, rely=0.65, anchor="center")

    def criarTelaEmpresa(self, empresa):
        # Frames da Tela de Empresa
        self.FrameEmpresa = Frame(self.CanvasPrincipal, background="white")
        self.FrameEmpresa.pack(fill='both', expand=True)
        self.Frames.append(self.FrameEmpresa)

        # Pega os dados da empresa alvo
        self.cursor.execute(f"SELECT * FROM {empresa}")
        self.resultadosBancoDeDado = self.cursor.fetchall()

        self.listinhaRankProduto = []
        self.listinhaProduto = []
        produtos_processados = set()

        for resultado in self.resultadosBancoDeDado:
            produto = resultado[6]

            if produto not in produtos_processados:
                produtos_processados.add(produto)
                self.listinhaProduto.append(produto)

                for resultado2 in self.resultadosBancoDeDado:
                    produto2 = resultado2[6]
                    if produto2 == produto:
                        self.listinhaRankProduto.append(produto)
                        
        self.ranking_produtos = Counter(self.listinhaRankProduto).most_common()

        ranking_text = ""
        for index, (produto, quantidade) in enumerate(self.ranking_produtos[0:5], start=1):
            ranking_text += f"{index}. {produto}\n"

        produtos = [produto for produto, quantidade in self.ranking_produtos[:5]]
        quantidades = [quantidade for produto, quantidade in self.ranking_produtos[:5]]

        # Montando o grafico de pizza
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(quantidades, labels=produtos, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})

        ax.axis('equal')

        #plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.FrameEmpresa)
        canvas.draw()

        canvas_widget = canvas.get_tk_widget()

        canvas_widget.place(relx=0.25, rely=0.65, anchor="center", width=400, height=265)

        # Montando a tela
        self.NomeEmpresa = Label(self.FrameEmpresa, text=empresa.upper(), font="Impact 50", background=self.FrameEmpresa.cget("bg"))
        self.NomeEmpresa.place(relx=0.99, rely=0.0, anchor="ne")

        # Botão para Scrapping
        self.BotaoScrap = Button(self.FrameEmpresa, text="Fazer Scrapping", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaScrapping(empresa)))
        self.BotaoScrap.place(relx=0.5, rely=0.055, anchor="center")

        # Botão para voltar para tela inicial
        self.BotaoVoltar = Button(self.FrameEmpresa, text="Voltar", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaInicial()))
        self.BotaoVoltar.place(relx=0.04, rely=0.055, anchor="center")

        # Barrinhas para deixar a interface separadinha
        self.barrinhaBonita = Frame(self.FrameEmpresa, background="black", width=1280, height=3)
        self.barrinhaBonita.place(relx=0.5, rely=0.11, anchor="center")

        self.barrinhaBonita2 = Frame(self.FrameEmpresa, background="black", width=3, height=640)
        self.barrinhaBonita2.place(relx=0.5, rely=1, anchor="s")

        # Ranqueamento de produtos
        self.LabelzinhoRankProduto = Label(self.FrameEmpresa, text="Rank Dos Mais Reclamados", font="Impact 18", background=self.FrameEmpresa.cget("bg"))
        self.LabelzinhoRankProduto.place(relx=0.05, rely=0.2, anchor="w")

        self.Rank = Label(self.FrameEmpresa, text=ranking_text, font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.Rank.place(relx=0.05, rely=0.23, anchor="nw")

        # Barra de seleção do produto para exibir na tabela
        self.SeletorReclamacoes = ttk.Combobox(self.FrameEmpresa, values=self.listinhaProduto)
        self.SeletorReclamacoes.set(self.listinhaProduto[0])
        self.SeletorReclamacoes.bind("<<ComboboxSelected>>", lambda event: (self.mudarTabela(self.SeletorReclamacoes.get()), self.mudarRanqueamentoRegiao(self.SeletorReclamacoes.get())))
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

        # Ranqueamento de localidade reclamada
        self.LabelzinhoRankRegiao = Label(self.FrameEmpresa, text="Rank Das Regiões Mais Reclamadas", font="Impact 18", background=self.FrameEmpresa.cget("bg"))
        self.LabelzinhoRankRegiao.place(relx=0.55, rely=0.65, anchor="w")

        self.RankRegiao = Label(self.FrameEmpresa, text="", font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.RankRegiao.place(relx=0.55, rely=0.68, anchor="nw")

        self.mudarRanqueamentoRegiao(self.SeletorReclamacoes.get())
    
    def formatar_texto(self, texto, largura_maxima):
        palavras = texto.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            if len(linha_atual) + len(palavra) + 1 <= largura_maxima:
                linha_atual += " " + palavra if linha_atual else palavra
            else:
                linhas.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        return "\n".join(linhas)


    def mudarTabela(self, produto):
        largura_maxima = 90
        for item in self.tree.get_children():
            self.tree.delete(item)

        motivos_inseridos = set()

        for motivo, produto_reclamado in zip(self.resultadosMotivoReclamacao, self.resultadosProdutoReclamado):
            if produto_reclamado[0] == produto:
                if motivo[0] != "None" and motivo[0] not in motivos_inseridos:
                    motivos_inseridos.add(motivo[0])
                    texto_formatado = self.formatar_texto(motivo[0], largura_maxima)
                    linhas = texto_formatado.split("\n")

                    for linha in linhas:
                        self.tree.insert("", "end", values=(linha,))
                    self.tree.insert("", "end", values=(" ",))

    def mudarRanqueamentoRegiao(self, produto):
        self.listinhaRankRegiao = []

        for resultado in self.resultadosBancoDeDado:
            if produto == resultado[6]:
                self.listinhaRankRegiao.append(resultado[3])
        
        self.rankingRegiao_text = ""
        for index, (produto, quantidade) in enumerate(Counter(self.listinhaRankRegiao).most_common()[0:5], start=1):
            self.rankingRegiao_text += f"{index}. {produto}\n"
            self.listinhaProduto.append(produto)
        
        self.RankRegiao.config(text=self.rankingRegiao_text)

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
        
        resultado = process.extractOne(lematizado, self.produtos_conhecidos, score_cutoff=75)
        
        if resultado:
            produto_correspondente, similaridade = resultado
            return produto_correspondente
        else:
            self.produtos_conhecidos.append(lematizado)
        
        return lematizado
    
    def fazerScrapping(self, empresa):
        self.cursor.execute(f"SELECT produto_reclamado FROM {empresa}")
        resultadosProdutosConhecidos = self.cursor.fetchall()

        for resultado in resultadosProdutosConhecidos:

            self.produtos_conhecidos.append(resultado[0])

        self.service = Service(ChromeDriverManager().install())  

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")

        self.driver = uc.Chrome(options=options)
     
        model_path = os.path.join(self.base_path, 'Treinar IA', f'IA {empresa.capitalize()}','model-best')

        self.IA = spacy.load(model_path)

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
                                motivo_identificado = ent.text.capitalize()
                                break
                        
                        if produto_identificado:
                            produto_normalizado = self.normalizar_produto(produto_identificado)
                        elif empresa == "habibs":
                            produto_normalizado = "Geral"
                        
                        comando = f'INSERT INTO {empresa} (titulo_reclamacao, reclamacao, local_reclamacao, data_reclamacao, status_reclamacao, produto_reclamado, motivo_reclamado) VALUES ("{titulo}", "{reclamacao_texto}", "{local_reclamacao}", "{data_reclamacao}", "{status_reclamacao}", "{produto_normalizado}", "{motivo_identificado}")'
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