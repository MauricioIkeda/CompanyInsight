# Reclame Aqui Web Scraper e Análise de Reclamações

Este projeto é uma ferramenta de web scraping e análise de reclamações do site **Reclame Aqui**. Desenvolvido para a empresa Avivatec, o programa coleta dados de reclamações de empresas parceiras, como Positivo e Habib's, e utiliza uma IA de processamento de linguagem natural (NLP) para analisar e categorizar essas reclamações.

## Funcionalidades

- **Web Scraping**: Extrai dados de reclamações de empresas selecionadas no Reclame Aqui, incluindo:
  - Título da reclamação
  - Local da reclamação
  - Status de resposta (respondida ou não)
  - Status de resolução (resolvida ou não)
  - Data da reclamação

- **Análise de Texto com IA**: Utilizando o SpaCy, um modelo de NLP está em treinamento para processar e classificar as reclamações, com foco em:
  - Identificação do motivo da reclamação
  - Produto, marca e modelo envolvidos
  - Detecção de spam (caso não seja uma reclamação legítima)

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **MySQL**: Armazena os dados de reclamações extraídos.
- **Selenium e WebDriver**: Realiza o scraping automatizado no site do Reclame Aqui.
- **SpaCy**: Treinamento e implementação de modelos de NLP para análise de texto.
- **FuzzyWuzzy**: Suporte para correspondência de texto ao identificar e categorizar informações das reclamações.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   ```
2. Instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Configuração de Empresas**: Escolha as empresas para coleta de dados no arquivo de configuração.
2. **Execução do Scraper**: Inicie o programa para coletar dados de reclamações:
   ```bash
   python BackEnd.ipynb
   ```
3. **Análise de Reclamações**: As reclamações coletadas são analisadas pelo modelo de NLP para classificação e armazenamento no banco de dados.

## Estrutura do Projeto

- `BackEnd.ipynb`: Arquivo principal para execução do scraper e processamento de NLP.
- `requirements.txt`: Arquivo de dependências para instalação do ambiente.
- `Treinar-IA/`: Contém os scripts para scraping de dados no Reclame Aqui para treinamento do modelo de IA (WebScrapingColetaTreinamento.py) e contém scripts e modelos para análise de texto (TreinamentoDoModelo.ipynb).
## Contribuição

Contribuições são bem-vindas! Por favor, envie um pull request com as alterações e melhorias.

## Licença

Esse projeto é licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
