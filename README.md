# BERT vs JEV — Sentiment Analysis

Este repositório apresenta um experimento de **classificação de sentimentos em textos**, comparando duas abordagens diferentes de Machine Learning:

* **JEV**, da TypeSafe.ai
* **ModernBERT**, utilizando fine-tuning para classificação de sentimentos

O objetivo é comparar as abordagens utilizando o mesmo problema e, principalmente, o mesmo conjunto de dados de avaliação.

---

## 🎯 Objetivo

O experimento utiliza o **IMDB Dataset of 50K Movie Reviews**, composto por 50.000 avaliações de filmes classificadas como:

* `positive`
* `negative`

A ideia é observar como diferentes estratégias de modelos de linguagem podem resolver o mesmo problema de classificação. Esse experimento foi inpirado no artigo *Language Models for Text Classification: From Bag-of-Words to Jev* do pesquisador **Sebastian Raschka** .

* https://magazine.sebastianraschka.com/p/classifier-history-and-jev

### Abordagens utilizadas

**JEV**

O JEV é utilizado para realizar a classificação dos textos sem a necessidade de realizar um processo tradicional de fine-tuning específico para o dataset.

**ModernBERT**

O ModernBERT parte de um modelo pré-treinado e passa por um processo de **fine-tuning** utilizando as avaliações do IMDB.

O fluxo é:

```text
IMDB Dataset
     │
     ├── Treinamento
     │       │
     │       ▼
     │   ModernBERT
     │   Fine-tuning
     │
     └── Teste
             │
             ├── ModernBERT
             │
             └── JEV
                     │
                     ▼
             Comparação de resultados
```

---

## 📂 Estrutura do repositório

```text
.
├── .gitignore
├── requiremntes.txt
├── BERT-versus-jev.ipynb
├── app.py
└── kaggle_imdb_sentimental_analysis.py
```

### `.gitignore`

Define os arquivos e diretórios que não devem ser versionados pelo Git.

Entre eles estão arquivos potencialmente grandes, como:

* Dataset do IMDB
* Modelo fine-tuned
* Checkpoints de treinamento
* Ambientes virtuais
* Arquivos temporários do Jupyter

O dataset e os pesos do modelo não são armazenados diretamente neste repositório.

---

### `BERT-versus-jev.ipynb`

Notebook principal do experimento.

Ele contém o fluxo de treinamento e avaliação do **ModernBERT**, incluindo:

1. Carregamento do dataset
2. Preparação dos dados
3. Separação entre treinamento e teste
4. Tokenização
5. Fine-tuning do ModernBERT
6. Avaliação do modelo
7. Accuracy
8. Precision
9. Recall
10. F1-score
11. Matriz de confusão
12. Testes de classificação
13. Comparação dos Resultados

---

### `app.py`

Aplicação utilizada para executar a classificação fora do ambiente do notebook.

A ideia é separar o experimento exploratório realizado no Jupyter da utilização do modelo em uma aplicação Python.

Dependendo da configuração do projeto, o aplicativo pode ser utilizado para enviar textos e obter a classificação correspondente.

Exemplo conceitual:

```text
Texto
  │
  ▼
Aplicação
  │
  ▼
Modelo de classificação
  │
  ▼
Positive / Negative
```

---

### `kaggle_imdb_sentimental_analysis.py`

Módulo Python responsável pela implementação da classificação utilizando JEV.

Ele encapsula a lógica necessária para processar as avaliações e utilizar o modelo para determinar o sentimento de cada texto.

A separação dessa lógica em um módulo independente permite reutilizar a implementação tanto no notebook quanto na aplicação.

---

## 🧠 Sobre o ModernBERT

O ModernBERT é uma arquitetura moderna baseada em BERT, utilizada neste projeto através de um modelo pré-treinado que posteriormente recebe **fine-tuning para classificação de sentimentos**.

O processo pode ser representado da seguinte forma:

```text
Modelo pré-treinado
       │
       ▼
   ModernBERT
       │
       │ Fine-tuning
       ▼
IMDB Movie Reviews
       │
       ▼
Modelo especializado
em análise de sentimentos
```

O modelo não é treinado do zero.

Durante o fine-tuning, seus pesos são ajustados utilizando os exemplos do conjunto de treinamento.

---

## 📊 Avaliação

O modelo é avaliado utilizando um conjunto de teste separado dos dados utilizados durante o treinamento.

As principais métricas utilizadas são:

### Accuracy

Percentual de classificações corretas.

```text
Accuracy = classificações corretas / total de classificações
```

### Precision

Mede a proporção das previsões positivas que realmente são positivas.

### Recall

Mede a proporção dos exemplos positivos que foram corretamente identificados.

### F1-score

Combina Precision e Recall em uma única métrica.

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Além das métricas numéricas, o projeto utiliza uma **matriz de confusão** para visualizar os erros e acertos do classificador.

---

## 🗂️ Dataset

O experimento utiliza o:

**IMDB Dataset of 50K Movie Reviews**

O dataset contém aproximadamente 50.000 avaliações de filmes, divididas entre sentimentos positivos e negativos.

Por questões de tamanho, o dataset **não é versionado neste repositório**.

O arquivo esperado localmente é:

```text
data/
└── imdb-dataset.csv
```

Para donwload dos dados:

* https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

---

## 🚀 Executando o projeto

### 1. Clone o repositório

```bash
git clone git@github.com:armindoguerra/jev-test.git
cd jev-test
```

### 2. Crie um ambiente virtual

Por exemplo:

```bash
python -m venv .venv
```

Ative o ambiente:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

---

### 3. Instale as dependências

As principais bibliotecas utilizadas pelo experimento incluem:

```bash
pip install torch
pip install transformers
pip install datasets
pip install scikit-learn
pip install pandas
pip install matplotlib
```

Para utilizar Jupyter:

```bash
pip install jupyter
```

Caso queira instalar a partir do terminal, use o arquivo **requirements.txt**.

---

## 🍎 Apple Silicon

O treinamento do ModernBERT pode utilizar a GPU dos Macs com Apple Silicon através do **MPS (Metal Performance Shaders)**.

Para verificar se o PyTorch reconhece a GPU:

```python
import torch

print(torch.backends.mps.is_available())
```

Se retornar:

```text
True
```

o ambiente possui suporte a MPS.

O notebook pode então utilizar:

```python
device = "mps"
```

para executar o modelo na GPU do Apple Silicon.

---

## 🔬 Reprodutibilidade

Para que a comparação seja consistente, recomenda-se utilizar:

* O mesmo dataset
* A mesma divisão de treinamento e teste
* Os mesmos exemplos de avaliação
* As mesmas métricas

Dessa forma, a comparação procura medir as diferenças entre as abordagens sob condições equivalentes.

---

## ⚠️ Modelos e arquivos grandes

Os pesos do ModernBERT fine-tuned podem ocupar centenas de megabytes e, por isso, não fazem parte do repositório Git.

Da mesma forma, o dataset do IMDB não é versionado.

Isso mantém o repositório focado em:

* Código
* Notebook
* Experimento
* Documentação

Os modelos treinados podem ser armazenados separadamente em uma plataforma apropriada para artefatos de Machine Learning.

---

## 👤 Autor

**Armindo Guerra**

AI & Machine Learning Engineering

GitHub:

`https://github.com/armindoguerra`
