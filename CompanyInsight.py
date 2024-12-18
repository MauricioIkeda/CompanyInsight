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

import re

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

        # Carregando e conectando com o banco de dados
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
        # Obtendo todos os dados do banco de dado da empresa especifica
        self.cursor.execute(f"SELECT motivo_reclamado FROM {empresa}")
        self.resultadosMotivoReclamacao = self.cursor.fetchall()
        self.cursor.execute(f"SELECT produto_reclamado FROM {empresa}")
        self.resultadosProdutoReclamado = self.cursor.fetchall()
        self.cursor.execute(f"SELECT data_reclamacao FROM {empresa}")
        self.resultadosDataReclamacao = self.cursor.fetchall()
        self.cursor.execute(f"SELECT status_reclamacao FROM {empresa}")
        self.resultadosStatusReclamacao = self.cursor.fetchall()

        # Criar um container para o Canvas e Scrollbar
        self.FrameEmpresaContainer = Frame(self.CanvasPrincipal, background="white")
        self.FrameEmpresaContainer.pack(fill='both', expand=True)
        self.Frames.append(self.FrameEmpresaContainer)

        # Canvas para conteúdo scrollável
        self.FrameEmpresaCanvas = Canvas(self.FrameEmpresaContainer, background="white")
        self.FrameEmpresaCanvas.pack(side=LEFT, fill='both', expand=True)

        # Scrollbar vinculada ao Canvas
        self.scrollbar = Scrollbar(self.FrameEmpresaContainer, orient=VERTICAL, command=self.FrameEmpresaCanvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Configurar o Canvas para usar a Scrollbar
        self.FrameEmpresaCanvas.configure(yscrollcommand=self.scrollbar.set)

        # Criar um Frame interno para o Canvas
        self.FrameEmpresa = Frame(self.FrameEmpresaCanvas, background="white")
        self.FrameEmpresaCanvas.create_window((0, 0), window=self.FrameEmpresa, anchor="nw", width=1280, height=1440)

        # Atualizar o scrollregion sempre que o Frame interno for redimensionado
        self.FrameEmpresa.bind("<Configure>", lambda e: self.FrameEmpresaCanvas.configure(scrollregion=self.FrameEmpresaCanvas.bbox("all")))

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
                    if resultado2[6] == produto and resultado[6] != "Nao identificado":
                        self.listinhaRankProduto.append(produto)

        self.ranking_produtos = Counter(self.listinhaRankProduto).most_common()

        ranking_text = ""
        for index, (produto, quantidade) in enumerate(self.ranking_produtos[0:5], start=1):
            ranking_text += f"{index}. {produto}\n"

        produtos = [produto for produto, quantidade in self.ranking_produtos[:5]]
        quantidades = [quantidade for produto, quantidade in self.ranking_produtos[:5]]

        # Montando o gráfico de pizza
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(quantidades, labels=produtos, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})

        ax.axis('equal')

        # plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.FrameEmpresa)
        canvas.draw()

        canvas_widget = canvas.get_tk_widget()

        canvas_widget.place(relx=0.25, rely=0.2, anchor="n", width=500, height=275)

        # Montando a tela
        self.NomeEmpresa = Label(self.FrameEmpresa, text=empresa.upper(), font="Impact 50", background=self.FrameEmpresa.cget("bg"))
        self.NomeEmpresa.place(relx=0.985, rely=0.0, anchor="ne")

        # Botão para Scrapping
        self.BotaoScrap = Button(self.FrameEmpresa, text="Fazer Scrapping", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaScrapping(empresa)))
        self.BotaoScrap.place(relx=0.5, rely=0.03, anchor="center")

        # Botão para voltar para tela inicial
        self.BotaoVoltar = Button(self.FrameEmpresa, text="Voltar", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaInicial()))
        self.BotaoVoltar.place(relx=0.04, rely=0.03, anchor="center")

        # Barrinhas para deixar a interface separadinha
        self.barrinhaBonita = Frame(self.FrameEmpresa, background="black", width=1280, height=3)
        self.barrinhaBonita.place(relx=0.5, rely=0.06, anchor="center")

        self.barrinhaBonita2 = Frame(self.FrameEmpresa, background="black", width=3, height=1354)
        self.barrinhaBonita2.place(relx=0.5, rely=1, anchor="s")

        # Barra de seleção do produto para exibir na tabela
        self.SeletorReclamacoes = ttk.Combobox(self.FrameEmpresa, values=self.listinhaProduto)
        self.SeletorReclamacoes.set(self.listinhaProduto[0])
        self.SeletorReclamacoes.bind("<<ComboboxSelected>>", lambda event: (self.mudarTabela(self.SeletorReclamacoes.get()), self.mudarRanqueamentoRegiao(self.SeletorReclamacoes.get()), self.montarGraficoReclamacoesData(self.SeletorReclamacoes.get()), self.mudarRanqueamentoStatus(self.SeletorReclamacoes.get())))
        self.SeletorReclamacoes.place(relx=0.75, rely=0.1, anchor="center")

        # Criando e colocando os dados da tabela de reclamações
        self.tree = ttk.Treeview(self.FrameEmpresa, columns=("Reclamações"), show='headings')
        self.tree.column("Reclamações", width=500)
        self.tree.heading("Reclamações", text="Reclamações".capitalize())
        self.tree.place(relx=0.75, rely=0.13, anchor="n")

        estilo = ttk.Style()
        estilo.configure("Treeview", rowheight=25)

        self.mudarTabela(self.SeletorReclamacoes.get())

        # RANQUEAMENTOS

        # Ranqueamento de produtos
        self.tituloRankProduto = Label(self.FrameEmpresa, text="Rank Dos Mais Reclamados", font="Impact 20", background=self.FrameEmpresa.cget("bg"))
        self.tituloRankProduto.place(relx=0.05, rely=0.1, anchor="w")

        self.rank = Label(self.FrameEmpresa, text=ranking_text, font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.rank.place(relx=0.05, rely=0.11, anchor="nw")

        # Ranqueamento de localidade reclamada
        self.tituloRankRegiao = Label(self.FrameEmpresa, text=f"Rank Das Regiões Mais Reclamadas De {(self.SeletorReclamacoes.get()).capitalize()}", font="Impact 18", background=self.FrameEmpresa.cget("bg"))
        self.tituloRankRegiao.place(relx=0.55, rely=0.33, anchor="nw")

        self.rankRegiao = Label(self.FrameEmpresa, text="", font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.rankRegiao.place(relx=0.55, rely=0.35, anchor="nw")

        # Ranqueamento Geral dos status das reclamações
        listaDeStatus = []
        for status in self.resultadosStatusReclamacao:
            listaDeStatus.append(status[0])

        self.rankingStatusGeralText = ""
        for produto, quantidade in Counter(listaDeStatus).most_common():
            self.rankingStatusGeralText += f"{quantidade} - {produto}.\n"

        self.tituloRankStatusGeral = Label(self.FrameEmpresa, text=f"Status Das Reclamações Geral", font="Impact 20", background=self.FrameEmpresa.cget("bg"))
        self.tituloRankStatusGeral.place(relx=0.05, rely=0.4, anchor="nw")

        self.rankStatusGeral = Label(self.FrameEmpresa, text=self.rankingStatusGeralText, font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.rankStatusGeral.place(relx=0.05, rely=0.425, anchor="nw")

        # Grafico das datas das reclamações do produto
        self.tituloGraficoDataReclamacoes = Label(self.FrameEmpresa, text=f"Gráfico Das Datas Das Reclamações de {(self.SeletorReclamacoes.get()).capitalize()}", font="Impact 20", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.tituloGraficoDataReclamacoes.place(relx=0.55, rely=0.47, anchor="nw")

        self.montarGraficoReclamacoesData(self.SeletorReclamacoes.get())

        # Ranqueamento dos Status das reclamações do Produto selecionado
        self.tituloRankStatusProduto = Label(self.FrameEmpresa, text=f"Status Das Reclamações de {(self.SeletorReclamacoes.get()).capitalize()}", font="Impact 20", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.tituloRankStatusProduto.place(relx=0.55, rely=0.72, anchor="nw")

        self.rankStatusProduto = Label(self.FrameEmpresa, text="", font="Impact 18", background=self.FrameEmpresa.cget("bg"), justify='left')
        self.rankStatusProduto.place(relx=0.55, rely=0.745, anchor="nw")

        # Chamada das funções iniciais
        self.mudarRanqueamentoRegiao(self.SeletorReclamacoes.get())
        self.mudarRanqueamentoStatus(self.SeletorReclamacoes.get())

    def mudarRanqueamentoStatus(self, produto):
        self.tituloRankStatusProduto.lift()
        self.tituloRankStatusProduto.config(text=f"Status Das Reclamações de {(self.SeletorReclamacoes.get()).capitalize()}")
        listaDeStatus = []

        for status_reclacamao, produto_reclamado in zip(self.resultadosStatusReclamacao, self.resultadosProdutoReclamado):
            if produto == produto_reclamado[0]:
                listaDeStatus.append(status_reclacamao[0])

        self.rankingStatusProdutoText = ""
        for status, quantidade in Counter(listaDeStatus).most_common():
            self.rankingStatusProdutoText += f"{quantidade} - {status}.\n"

        self.rankStatusProduto.config(text=self.rankingStatusProdutoText)

    def montarGraficoReclamacoesData(self, produto):
        if hasattr(self, 'CanvasGraficoReclamacoesData'):
            CanvasGraficoReclamacoesData.place_forget()

        # Criando Grafico Das Datas Reclamações
        GraficoReclamacoesData = plt.figure(figsize=(6, 3), dpi=100)
        CanvasGraficoReclamacoesData = FigureCanvasTkAgg(GraficoReclamacoesData, master=self.FrameEmpresa)
        CanvasGraficoReclamacoesData.draw()
        CanvasGraficoReclamacoesData.get_tk_widget().place(relx=0.75, rely=0.52, anchor="n")
        
        self.DataReclamada = []  # Lista para armazenar as datas
        for data, produto_reclamado in zip(self.resultadosDataReclamacao, self.resultadosProdutoReclamado):
            if produto_reclamado[0] == produto:
                self.DataReclamada.append(data[0])
        
        # Contando a quantidade de reclamações para cada data
        data_contagem = Counter(self.DataReclamada)
        
        # Colocando as datas em ordem
        datas_ordenadas = sorted(data_contagem.keys())
        
        # Criando listas para as datas e quantidades de reclamações
        quantidades = [data_contagem[date] for date in datas_ordenadas]
        
        # Configurando o grafico
        plt.plot(datas_ordenadas, quantidades, 'o-r')
        plt.xlabel('Data')
        plt.ylabel('Quantidade')
        plt.xticks(datas_ordenadas, [str(date) for date in datas_ordenadas], rotation=45)
        plt.yticks(range(max(quantidades) + 1))
        plt.grid(True)
        plt.tight_layout(pad=2.0)

        self.tituloGraficoDataReclamacoes.config(text=f"Gráfico Das Datas Das Reclamações\nde {(self.SeletorReclamacoes.get()).capitalize()}")
    
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

        self.tituloRankRegiao.config(text=f"Rank Das Regiões Mais Reclamadas De {str(produto).capitalize()}")

        for resultado in self.resultadosBancoDeDado:
            if produto == resultado[6]:
                self.listinhaRankRegiao.append(resultado[3])
        
        self.rankingRegiao_text = ""
        for index, (produto, quantidade) in enumerate(Counter(self.listinhaRankRegiao).most_common()[0:5], start=1):
            self.rankingRegiao_text += f"{quantidade} Reclamações - {produto}\n"
            self.listinhaProduto.append(produto)
        
        self.rankRegiao.config(text=self.rankingRegiao_text)

    def criarTelaScrapping(self, empresa):
        self.FrameScrapping = Frame(self.CanvasPrincipal, background="white")
        self.FrameScrapping.pack(fill='both', expand=True)
        self.Frames.append(self.FrameScrapping)

        self.TextoInformativo = Label(self.FrameScrapping, text="Digite a quantidade de paginas que deseja!", font="Impact 45", background=self.FrameScrapping.cget("bg"))
        self.TextoInformativo.place(relx=0.5, rely=0.4, anchor="center")
        
        # Montando a tela
        self.NomeEmpresa = Label(self.FrameScrapping, text=empresa.upper(), font="Impact 50", background=self.FrameScrapping.cget("bg"))
        self.NomeEmpresa.place(relx=0.99, rely=0.0, anchor="ne")

        # Barrinhas para deixar a interface separadinha
        self.barrinhaBonita = Frame(self.FrameScrapping, background="black", width=1280, height=3)
        self.barrinhaBonita.place(relx=0.5, rely=0.11, anchor="center")

        # Botão para voltar para tela inicial
        self.BotaoVoltar = Button(self.FrameScrapping, text="Voltar", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaEmpresa(empresa)))
        self.BotaoVoltar.place(relx=0.04, rely=0.055, anchor="center")

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
        
        resultado = process.extractOne(lematizado, self.produtos_conhecidos, score_cutoff=90)
        
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
                        data_reclamacao_cru = self.driver.find_elements(By.CLASS_NAME, 'sc-lzlu7c-6')[1].text
                        status_reclamacao = self.driver.find_element(By.CLASS_NAME, 'sc-lzlu7c-18').text

                        data_reclamacao = re.match(r'(\d{2}/\d{2}/\d{4})', data_reclamacao_cru)

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
                        else:
                            produto_normalizado = "Nao identificado"
                        
                        comando = f'INSERT INTO {empresa} (titulo_reclamacao, reclamacao, local_reclamacao, data_reclamacao, status_reclamacao, produto_reclamado, motivo_reclamado) VALUES ("{titulo}", "{reclamacao_texto}", "{local_reclamacao}", "{data_reclamacao.group(1)}", "{status_reclamacao}", "{produto_normalizado}", "{motivo_identificado}")'
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