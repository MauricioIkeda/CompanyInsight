from tkinter import *

class Aplicativo:
    def __init__(self):
        self.janela = Tk()
        self.janela.geometry("1280x720")
        self.janela.resizable(False, False)
        self.janela.title("CompanyInsight")

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
        self.FrameEmpresa = Frame(self.CanvasPrincipal, background="white")
        self.FrameEmpresa.pack(fill='both', expand=True)
        self.Frames.append(self.FrameEmpresa)

        self.NomeEmpresa = Label(self.FrameEmpresa, text=empresa.upper(), font="Impact 50", background=self.FrameEmpresa.cget("bg"))
        self.NomeEmpresa.place(relx=0.99, rely=0.0, anchor="ne")

        self.BotaoVoltar = Button(self.FrameEmpresa, text="Voltar", foreground="white", background="gray", font="Impact 20", command= lambda: (self.destruirFrames(), self.criarTelaInicial()))
        self.BotaoVoltar.place(relx=0.04, rely=0.055, anchor="center")

        self.barrinhaBonita = Frame(self.FrameEmpresa, background="black", width=1280, height=3)
        self.barrinhaBonita.place(relx=0.5, rely=0.11, anchor="center")

    def destruirFrames(self):
        for frame in self.Frames:
            frame.destroy()


Aplicativo()