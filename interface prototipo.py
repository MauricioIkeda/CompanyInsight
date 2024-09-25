import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QRadialGradient, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class JanelaComGradiente(QMainWindow):
    def __init__(self):
        super().__init__()

        # Propriedades da janela
        self.esquerda = 400
        self.topo = 200
        self.largura = 1000
        self.altura = 600
        self.titulo = 'Janela com Imagens Redimensionadas'

        # Carregar as imagens
        self.pixmap1 = QPixmap('Esquerda_00000.png')
        self.pixmap2 = QPixmap('Direita meio_00119.png')

        # Labels para as imagens
        self.labelEsquerda = QLabel(self)
        self.labelDireita = QLabel(self)

        # Configurando a janela
        self.carregar_janela()

    def carregar_janela(self):
        self.setGeometry(self.esquerda, self.topo, self.largura, self.altura)
        self.setWindowTitle(self.titulo)
        self.show()

    def resizeEvent(self, event):
        # Redimensionar as imagens individualmente
        self.redimensionar_imagem(self.labelEsquerda, self.pixmap1, 1)  # Ajuste a proporção desejada
        self.redimensionar_imagem(self.labelDireita, self.pixmap2, 0.8)   # Ajuste a proporção desejada

        # Manter a label da esquerda na frente
        self.labelEsquerda.raise_()

        self.update()  # Solicita uma nova atualização da janela

    def redimensionar_imagem(self, label, pixmap, proporcao):
        # Redimensionar o QPixmap e definir na QLabel
        largura_imagem = int(self.width() * proporcao)  # Largura baseada na proporção
        altura_imagem = int(self.height() * proporcao)  # Altura baseada na proporção
        pixmap_redimensionado = pixmap.scaled(largura_imagem, altura_imagem, Qt.KeepAspectRatio)
        label.setPixmap(pixmap_redimensionado)

        # Centralizar a imagem na janela
        label.resize(pixmap_redimensionado.width(), pixmap_redimensionado.height())

        # Ajuste a posição da imagem da esquerda
        if label == self.labelEsquerda:
            # Move a imagem da esquerda para a esquerda
            label.move(-10, (self.height() - label.height()) // 2)  # Altere o valor 50 conforme necessário
        else:
            label.move((self.width() - label.width()) // 2, 
                        (self.height() - label.height()) // 2)

    def paintEvent(self, event):
        # Desenha o fundo com gradiente radial
        pintor = QPainter(self)
        gradiente_fundo = QRadialGradient(self.width() / 2, self.height() / 2, self.width() / 2)
        gradiente_fundo.setColorAt(0, QColor('#004080'))
        gradiente_fundo.setColorAt(1, QColor('#000F1E'))
        pintor.fillRect(self.rect(), gradiente_fundo)

        # Desenha a barra no topo
        bar_height = 50
        top_bar_gradient = QRadialGradient(self.width() / 2, bar_height / 2, self.width() / 2)
        top_bar_gradient.setColorAt(0, QColor('#004080'))
        top_bar_gradient.setColorAt(1, QColor('#000F1E'))
        pintor.fillRect(0, 0, self.width(), bar_height, top_bar_gradient)

        # Linha reta amarela na parte inferior da barra superior
        pintor.setPen(QPen(QColor(255, 223, 0), 3))  # Cor da linha
        pintor.drawLine(0, bar_height, self.width(), bar_height)  # Linha na parte inferior da barra superior

        # Desenha as linhas verticais na barra
        pen = QPen(QColor('#FFDF00'), 3)  # Linhas amarelas
        pintor.setPen(pen)
        for i in range(10, 40, 10):  # Exemplo com 3 linhas espaçadas
            pintor.drawLine(i, 0, i, bar_height - 10)  # Ajuste para desenhar dentro da barra
            
# Inicializa o aplicativo e a janela
aplicacao = QApplication(sys.argv)
janela = JanelaComGradiente()
sys.exit(aplicacao.exec_())
