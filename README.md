# 🚜 PreparaCalda Pro 

O **PreparaCalda Pro** é uma solução digital desenvolvida para auxiliar produtores rurais e agrônomos na gestão eficiente da mistura de defensivos agrícolas. O software automatiza o cálculo de dosagens e, principalmente, define a **ordem química correta de mistura**, prevenindo perdas financeiras e danos ambientais.

## 🚀 Funcionalidades

* **Busca Inteligente:** Seleção de produtos a partir de um banco de dados SQLite.
* **Cálculo de Dosagem:** Conversão automática de doses (p/ 100L ou sachês) para o volume total do tanque.
* **Ordem de Mistura:** Algoritmo baseado em prioridades químicas (Adjuvantes > WG > WP > SC > EC > SL).
* **Alertas de Manejo:** Avisos automáticos para pré-diluição de sólidos e abastecimento de água.
* **Histórico de Consultas:** Log local das últimas misturas realizadas.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Interface Web:** [Streamlit](https://streamlit.io/)
* **Banco de Dados:** SQLite3
* **Manipulação de Dados:** Pandas

## 📦 Como Rodar o Projeto Localmente

1. **Clone o repositório:**
2. ```
   git clone [https://github.com/seu-usuario/preparacalda.git](https://github.com/seu-usuario/preparacalda.git)






**📋 Estrutura de Arquivos**
**app.py**: Código principal da interface e lógica de negócio.

**gerar_db.py**: Script de criação e alimentação do banco de dados.

**preparacalda.db**: Arquivo do banco de dados SQLite.

**requirements.txt**: Lista de bibliotecas necessárias para execução.

👨‍💻 **Desenvolvedor**
**Estudante: André Lucas**

**Instituição: IF Sertão - Campus Petrolina**

**Curso: Análise e Desenvolvimento de Sistemas (ADS)**


**1- Instale as dependências:**
bash :
pip install -r requirements.txt


**2- Inicie o banco de dados (caso necessário):**
bash :
python gerar_db.py

**3- Execute o App:**
bash :
python -m streamlit run app.py



