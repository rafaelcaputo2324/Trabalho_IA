### 1. Descrição do Problema
O valor de mercado de um diamante é tradicionalmente estimado através dos **4Cs** (*Carat*, *Cut*, *Color*, *Clarity*) e de suas medições tridimensionais (*depth*, *table*, *x*, *y*, *z*). A determinação humana de preço está sujeita a alta subjetividade e discrepâncias. O aprendizado de máquina oferece uma abordagem quantitativa, objetiva e escalável. 

A relação entre o peso em quilates (*carat*) e o preço é estritamente **não linear** e acelerada, tornando este problema ideal para avaliar os limites de um modelo linear paramétrico versus a capacidade de adaptação de um modelo não paramétrico baseado em comitês de árvores de decisão.

---

### 2. Base de Dados
- **Dataset:** *Diamonds* (disponível via `seaborn-data` / `ggplot2`).
- **Tamanho Original:** 53.940 registros e 10 colunas (9 variáveis preditoras e 1 variável-alvo).
- **Atributos:**
  - `carat`: peso do diamante em quilates (numérico contínuo).
  - `cut`: qualidade da lapidação (Fair, Good, Very Good, Premium, Ideal).
  - `color`: gradação de cor de J (pior) a D (melhor).
  - `clarity`: pureza/clareza (I1, SI2, SI1, VS2, VS1, VVS2, VVS1, IF).
  - `depth`: profundidade percentual total (`z / média(x, y)`).
  - `table`: largura do topo da pedra em relação ao ponto mais largo (%).
  - `price`: preço em dólares americanos (US$) — **variável-alvo**.
  - `x`, `y`, `z`: comprimento, largura e profundidade em milímetros (mm).
- **Pré-processamento Realizado:**
  - Remoção de 146 linhas duplicadas.
  - Eliminação de 22 registros fisicamente inconsistentes (dimensões `x`, `y` ou `z` zeradas ou outliers extremos `y > 20 mm`, `z > 10 mm`).
  - Base final tratada: **53.772 registros** (atende com folga ao requisito mínimo de 4.000 amostras).
  - Codificação ordinal respeitando a ordem natural de qualidade para `cut`, `color` e `clarity`.
  - Separação em treino (80% — 43.017 amostras) e teste (20% — 10.755 amostras) com semente aleatória reproduzível (`random_state=42`).
  - Padronização de escala (`StandardScaler`) encapsulada em `Pipeline` para evitar vazamento de dados (*data leakage*).

---

### 3. Algoritmos Implementados e Avaliados
1. **Regressão Linear Múltipla:** modelo paramétrico, determinístico e linear, atuando como *baseline*.
2. **Random Forest Regressor:** *ensemble* não paramétrico de 100 árvores de decisão (`n_estimators=100`), capaz de capturar relações não lineares e interações entre atributos.
3. **Melhorias Experimentais:**
   - **Random Forest Ajustado:** otimização com `RandomizedSearchCV` (`n_estimators=200`, `max_features=0.7`).
   - **Regressão Linear com Alvo Logarítmico:** modelagem de `log(price)` via `TransformedTargetRegressor` para lidar com a assimetria da variável-alvo.

---

### 4. Resultados Comparativos no Conjunto de Teste

| Modelo | MAE (US$) | RMSE (US$) | MSE | R² | Tempo de Treino (s) |
|---|---|---|---|---|---|
| **Regressão Linear** | 797,91 | 1.215,80 | 1.478.169,73 | 0,905 | 0,013 |
| **Random Forest (base)** | **264,68** | **524,78** | **275.390,42** | **0,982** | 7,55 |
| **Random Forest (ajustado)** | 263,00 | 519,49 | 269.871,14 | 0,983 | 10,76 |
| **Regressão Linear (log)** | 457,79 | 876,76 | 768.702,58 | 0,951 | 0,014 |

#### Principais Conclusões:
- O **Random Forest** superou a Regressão Linear com folga em todas as métricas, reduzindo o **RMSE em 56,8%** e o **MAE em 66,8%**, elevando o $R^2$ de 0,905 para **0,982**.
- A Regressão Linear apresentou limitações severas na cauda inferior, gerando **888 previsões de preço negativo** no conjunto de teste e erro percentual médio de **102,2%** para pedras de até US$ 1.000.
- O Random Forest manteve erro percentual médio extremamente estável (entre **5,6% e 7,3%**) em todas as faixas de preço.
- Na análise de importância, os atributos de tamanho/peso (`carat` com 59,0% e `y` com 29,7%) dominaram a formação do preço.

---

### 5. Estrutura do Repositório
```text
Trabalho_IA-main/
│
├── diamonds.csv                     # Base de dados (53.940 registros)
├── N2-AT2_IA_Diamonds.ipynb         # Notebook Google Colab executável de ponta a ponta
├── Relatorio_Tecnico_N2_AT2.pdf     # Relatório técnico comparativo completo em PDF
├── resultados.json                  # Métricas e dados numéricos consolidados
├── README.md                        # Documentação completa do projeto
│
└── figuras/                         # Gráficos de alta resolução gerados pelo notebook
    ├── eda_distribuicoes.png
    ├── eda_carat_corr.png
    ├── eda_categoricas.png
    ├── comparacao_metricas.png
    ├── previsto_vs_real.png
    ├── residuos.png
    ├── erro_por_faixa.png
    └── importancia.png
```

---

### 6. Como Executar

#### Opção A — Google Colab (Recomendado)
1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Faça o upload do arquivo `N2-AT2_IA_Diamonds.ipynb`.
3. Faça o upload do arquivo `diamonds.csv` no menu lateral de arquivos (caso não faça o upload, o notebook baixará a base automaticamente do repositório oficial).
4. No menu superior, clique em **Ambiente de execução** → **Executar tudo** (`Ctrl + F9`).

#### Opção B — Execução Local
1. Certifique-se de ter o Python 3.9+ instalado.
2. Instale as dependências:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```
3. Inicie o Jupyter Notebook ou JupyterLab:
   ```bash
   jupyter notebook N2-AT2_IA_Diamonds.ipynb
   ```
4. Execute todas as células.

---

### 7. Integrantes do Grupo
*(Preencher com o nome e matrícula dos integrantes do grupo)*
