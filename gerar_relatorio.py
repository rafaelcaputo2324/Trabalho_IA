import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas de dois passos para calcular o total de páginas dinamicamente
    e desenhar cabeçalho e rodapé elegantes com paginação correta.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Desenha cabeçalho sutil a partir da página 2
        if self._pageNumber > 1:
            self.drawString(36, 808, "N2-AT2: Inteligência Artificial I — Previsão de Preços de Diamantes")
            self.drawRightString(559, 808, "Regressão Linear × Random Forest")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)

        # Rodapé em todas as páginas
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        self.drawString(36, 30, "Relatório Técnico Comparativo de Aprendizado de Máquina")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(559, 30, page_str)
        self.restoreState()

def gerar_pdf():
    pdf_filename = "Relatorio_Tecnico_N2_AT2.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Paleta de Cores Institucional
    primary = colors.HexColor("#1B365D")    # Azul escuro institucional
    secondary = colors.HexColor("#2C5E8A")  # Azul médio
    dark_text = colors.HexColor("#222222")  # Texto escuro
    muted_text = colors.HexColor("#555555") # Legendas e metadados
    bg_light = colors.HexColor("#F8FAFC")   # Fundo suave
    border_col = colors.HexColor("#CBD5E1") # Borda sutil

    # Estilos Tipográficos
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=secondary,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=muted_text,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.6,
        textColor=dark_text,
        alignment=4, # Justificado
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=12.2,
        textColor=dark_text,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    caption_style = ParagraphStyle(
        "Caption_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.8,
        leading=10.5,
        textColor=muted_text,
        alignment=1, # Centralizado
        spaceBefore=3,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=primary,
        alignment=4
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.5,
        textColor=dark_text,
        alignment=0
    )

    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        parent=table_cell_style,
        alignment=1
    )

    table_cell_right = ParagraphStyle(
        "TableCellRight",
        parent=table_cell_style,
        alignment=2
    )

    story = []

    # CABEÇALHO DO DOCUMENTO
    story.append(Paragraph("RELATÓRIO TÉCNICO COMPARATIVO — N2-AT2", subtitle_style))
    story.append(Paragraph("Previsão de Preços de Diamantes: Regressão Linear × Random Forest", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary, spaceAfter=6, spaceBefore=2))
    
    meta_text = (
        "<b>Disciplina:</b> Inteligência Artificial I &nbsp;|&nbsp; "
        "<b>Modalidade:</b> Aprendizado Supervisionado (Regressão)<br/>"
        "<b>Base de Dados:</b> <i>Diamonds</i> (53.940 registros, 10 atributos) &nbsp;|&nbsp; "
        "<b>Algoritmos:</b> Regressão Linear Múltipla e Random Forest Regressor<br/>"
        "<b>Grupo / Autores:</b> <i>(Preencher com o nome dos integrantes)</i> &nbsp;|&nbsp; "
        "<b>Ambiente:</b> Python 3, Scikit-learn, Pandas, Matplotlib, Seaborn"
    )
    story.append(Paragraph(meta_text, meta_style))

    # Box Resumo Executivo
    resumo_box = [
        [Paragraph("<b>Resumo Executivo:</b> Este trabalho investiga a previsão contínua de preços de diamantes (em US$) baseada nas 4 características gemológicas universais (<i>4Cs: Carat, Cut, Color, Clarity</i>) e medidas tridimensionais. Foram implementados e confrontados dois algoritmos de paradigmas distintos: <b>Regressão Linear Múltipla</b> (paramétrico e interpretável) e <b>Random Forest Regressor</b> (não paramétrico baseado em comitê de árvores). O Random Forest superou amplamente o modelo linear em todas as métricas, alcançando <b>R² de 0,982</b> e <b>RMSE de US$ 524,78</b> no conjunto de teste independente (reduções de 56,8% no RMSE e 66,8% no MAE), além de manter estabilidade percentual entre 5,6% e 7,3% em todas as faixas de valor. Em contrapartida, a Regressão Linear clássica gerou 888 estimativas de preços negativos devido à incapacidade estrutural de capturar a convexidade entre peso e preço.", callout_style)]
    ]
    t_resumo = Table(resumo_box, colWidths=[523])
    t_resumo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, secondary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_resumo)
    story.append(Spacer(1, 8))

    # 1. INTRODUÇÃO
    story.append(Paragraph("1. Introdução", h1_style))
    story.append(Paragraph(
        "A precificação comercial de diamantes representa um dos desafios mais expressivos da avaliação de ativos físicos. O valor de mercado de uma gema lapidada resulta da avaliação conjunta de critérios físicos e gemológicos consolidados pelo <i>Gemological Institute of America</i> (GIA), conhecidos como os <b>4Cs</b>: <b>C</b>arat (massa em quilates), <b>C</b>ut (lapidação), <b>C</b>olor (cor) e <b>C</b>larity (pureza), associados a medidas espaciais tridimensionais (comprimento, largura, profundidade e relações percentuais de topo).",
        body_style
    ))
    story.append(Paragraph(
        "Tradicionalmente, a estimativa do valor é conduzida por peritos e gemólogos. No entanto, a combinação empírica dessas características sofre com subjetividade intrínseca e variações consideráveis entre avaliadores e mercados. O Aprendizado de Máquina surge como uma alternativa quantitativa, rápida e reproduzível para estimar o valor justo de mercado.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Objetivo:</b> Construir modelos preditivos capazes de estimar o preço de venda de diamantes a partir de seus atributos geométricos e de qualidade, realizando uma rigorosa análise comparativa entre um modelo paramétrico linear (<b>Regressão Linear Múltipla</b>) e um modelo não paramétrico baseado em conjunto de árvores de decisão (<b>Random Forest Regressor</b>).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Contribuição de ML:</b> O preço de um diamante não evolui de forma linear com seu tamanho: pedras maiores são exponencialmente mais raras na natureza, fazendo com que a relação peso × preço seja fortemente <b>convexa</b> e envolva interações complexas entre pureza, cor e corte. Avaliar até que ponto um modelo linear é capaz de aproximar essa realidade frente a um ensemble não linear constitui o cerne deste estudo.",
        body_style
    ))

    # 2. BASE DE DADOS
    story.append(Paragraph("2. Base de Dados", h1_style))
    story.append(Paragraph(
        "Utilizou-se o clássico conjunto <i>Diamonds</i>, originalmente introduzido por Hadley Wickham e distribuído na biblioteca <code>seaborn-data</code>. O dataset reúne originalmente <b>53.940 observações</b> e <b>10 atributos</b> (atendendo amplamente à exigência mínima de 4.000 registros).",
        body_style
    ))

    dados_atributos = [
        [Paragraph("Atributo", table_header_style), Paragraph("Tipo", table_header_style), Paragraph("Papel", table_header_style), Paragraph("Descrição e Escala de Valores", table_header_style)],
        [Paragraph("<code>carat</code>", table_cell_style), Paragraph("Numérico contínuo", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Peso em quilates (1 ct = 0,20 g). Varia de 0,20 a 5,01 ct.", table_cell_style)],
        [Paragraph("<code>cut</code>", table_cell_style), Paragraph("Categórico ordinal", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Qualidade do corte: <i>Fair &lt; Good &lt; Very Good &lt; Premium &lt; Ideal</i>.", table_cell_style)],
        [Paragraph("<code>color</code>", table_cell_style), Paragraph("Categórico ordinal", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Gradação de cor: de <i>J</i> (pior, amarelada) até <i>D</i> (melhor, incolor).", table_cell_style)],
        [Paragraph("<code>clarity</code>", table_cell_style), Paragraph("Categórico ordinal", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Pureza: <i>I1 &lt; SI2 &lt; SI1 &lt; VS2 &lt; VS1 &lt; VVS2 &lt; VVS1 &lt; IF</i>.", table_cell_style)],
        [Paragraph("<code>depth</code>", table_cell_style), Paragraph("Numérico contínuo", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Profundidade percentual total: <code>z / média(x, y)</code> (média: 61,7%).", table_cell_style)],
        [Paragraph("<code>table</code>", table_cell_style), Paragraph("Numérico contínuo", table_cell_center), Paragraph("Preditor", table_cell_center), Paragraph("Largura do topo plano relativa ao ponto mais largo (média: 57,5%).", table_cell_style)],
        [Paragraph("<code>price</code>", table_cell_style), Paragraph("Numérico inteiro", table_cell_center), Paragraph("<b>Alvo (y)</b>", table_cell_center), Paragraph("Preço comercial em dólares americanos (US$ 326 a US$ 18.823).", table_cell_style)],
        [Paragraph("<code>x</code>, <code>y</code>, <code>z</code>", table_cell_style), Paragraph("Numérico contínuo", table_cell_center), Paragraph("Preditores", table_cell_center), Paragraph("Comprimento (x), largura (y) e profundidade (z) em milímetros.", table_cell_style)],
    ]
    t_atributos = Table(dados_atributos, colWidths=[65, 85, 55, 318])
    t_atributos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, border_col),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(KeepTogether([t_atributos]))
    story.append(Spacer(1, 8))

    # 3. ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
    story.append(Paragraph("3. Análise Exploratória dos Dados (EDA)", h1_style))
    story.append(Paragraph(
        "<b>Estatísticas Descritivas e Assimetria:</b> A variável-alvo <code>price</code> possui média de US$ 3.932,80, mediana de US$ 2.401,00 e desvio padrão de US$ 3.989,44, exibindo <b>forte assimetria positiva à direita (skewness = 1,62)</b>. A concentração de preços na faixa inferior com uma cauda longa de diamantes de luxo indica que erros quadráticos em pedras raras dominarão o RMSE caso não tratados. Ao aplicar transformação logarítmica em <code>price</code>, a assimetria cai para <b>0,12</b>, aproximando-se de uma distribuição normal (Figura 1).",
        body_style
    ))

    if os.path.exists("figuras/eda_distribuicoes.png"):
        story.append(KeepTogether([
            Image("figuras/eda_distribuicoes.png", width=515, height=128),
            Paragraph("<b>Figura 1:</b> Histograma e densidade do preço (US$), logaritmo do preço e peso em quilates (carat).", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Correlações Lineares e Multicolinearidade:</b> Como destacado na Figura 2, o atributo <code>carat</code> é o preditor com maior correlação linear com o preço (<b>r = 0,92</b>). As dimensões tridimensionais (<code>x</code>, <code>y</code>, <code>z</code>) também se correlacionam intensamente com o preço (0,86 a 0,88). No entanto, a correlação cruzada mútua entre <code>carat</code>, <code>x</code>, <code>y</code> e <code>z</code> supera <b>0,95</b>, configurando <b>severa multicolinearidade</b>. Esse fator desestabiliza a inversão matricial dos Mínimos Quadrados da Regressão Linear, distorcendo a interpretabilidade dos pesos.",
        body_style
    ))

    if os.path.exists("figuras/eda_carat_corr.png"):
        story.append(KeepTogether([
            Image("figuras/eda_carat_corr.png", width=480, height=155),
            Paragraph("<b>Figura 2:</b> Relação Preço vs. Quilates (evidenciando convexidade) e mapa de calor de correlações de Pearson.", caption_style)
        ]))

    story.append(Paragraph(
        "<b>Paradoxo de Simpson e Fator de Confusão:</b> Na exploração das variáveis ordinais (Figura 3), lapidações superiores (<i>Ideal</i>) e tonalidades melhores (<i>D</i>) exibem preços medianos inferiores a pedras de corte <i>Fair</i> e cor <i>J</i>. Isso decorre do peso médio díspar: diamantes de cor <i>J</i> comercializados na base têm peso médio de 1,16 ct, ante 0,66 ct das cores <i>D</i>. O peso atua como variável de confusão fundamental, exigindo que o modelo multivariado controle o impacto do tamanho.",
        body_style
    ))

    if os.path.exists("figuras/eda_categoricas.png"):
        story.append(KeepTogether([
            Image("figuras/eda_categoricas.png", width=500, height=128),
            Paragraph("<b>Figura 3:</b> Distribuição de preços estratificada por lapidação, tonalidade de cor e pureza.", caption_style)
        ]))

    # 4. PRÉ-PROCESSAMENTO DOS DADOS
    story.append(Paragraph("4. Pré-Processamento dos Dados", h1_style))
    story.append(Paragraph(
        "A base não apresenta dados ausentes (<code>NaN</code>), mas auditorias de consistência apontaram registros incompatíveis com a física de gemas reais:",
        body_style
    ))
    story.append(Paragraph("• <b>Remoção de Duplicatas:</b> 146 linhas perfeitamente duplicadas foram eliminadas.", bullet_style))
    story.append(Paragraph("• <b>Expurgo de Inconsistências Físicas:</b> Foram removidos 20 diamantes com medidas zeradas (<code>x=0</code>, <code>y=0</code> ou <code>z=0</code>) e 2 outliers aberrantes (<code>y = 58,9 mm</code> e <code>y = 31,8 mm</code> em gemas pequenas), totalizando 22 exclusões. A base purificada consolidou-se em <b>53.772 registros válidos</b>.", bullet_style))
    story.append(Paragraph("• <b>Codificação Ordinal:</b> As classes <code>cut</code>, <code>color</code> e <code>clarity</code> foram codificadas em inteiros ordenados respeitando a taxonomia do GIA, preservando a ordenação ordinal sem criar alta dimensionalidade esparsa.", bullet_style))
    story.append(Paragraph("• <b>Particionamento Treino/Teste:</b> Divisão estrita em <b>80% para treino (43.017 instâncias)</b> e <b>20% para teste (10.755 instâncias)</b> com <code>random_state=42</code>.", bullet_style))
    story.append(Paragraph("• <b>Padronização de Escala:</b> Emprego de <code>StandardScaler</code> encapsulado em <code>Pipeline</code>, prevenindo vazamento de dados de teste (<i>data leakage</i>).", bullet_style))

    # 5. ALGORITMOS SELECIONADOS
    story.append(Paragraph("5. Algoritmos Selecionados", h1_style))
    story.append(Paragraph(
        "<b>1. Regressão Linear Múltipla (Mínimos Quadrados):</b> Modelo paramétrico clássico de referência: <i>y = Xβ + ε</i>. Apresenta treinamento analítico instantâneo, ausência de hiperparâmetros e interpretação direta, servindo como baseline para quantificar a fração de relação linear presente nos dados.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Random Forest Regressor:</b> Ensemble não paramétrico de 100 árvores de decisão geradas com amostragem bootstrap e partição aleatória de preditores. Capaz de capturar não linearidades agudas e interações entre atributos sem impor premissas de distribuição aos erros.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Variações Experimentais:</b> Avaliou-se uma versão otimizada com <code>RandomizedSearchCV</code> (200 árvores, 70% de features por corte) e um modelo de <i>Regressão Linear com Alvo em Logaritmo</i> (<code>TransformedTargetRegressor</code>).",
        body_style
    ))

    # 6. METODOLOGIA EXPERIMENTAL
    story.append(Paragraph("6. Metodologia Experimental", h1_style))
    story.append(Paragraph(
        "• <b>Validação Cruzada 5-Fold:</b> Executada na partição de treino (43.017 amostras) para apurar a estabilidade e o desvio padrão de cada modelo.<br/>"
        "• <b>Avaliação em Teste Cego:</b> Realizada nas 10.755 amostras reservadas para verificar a capacidade de generalização.<br/>"
        "• <b>Métricas de Desempenho:</b> Erro Absoluto Médio (<b>MAE</b> em US$), Erro Quadrático Médio (<b>MSE</b>), Raiz do Erro Quadrático Médio (<b>RMSE</b> em US$), Coeficiente de Determinação (<b>R²</b>) e tempos de execução.",
        body_style
    ))

    # 7. RESULTADOS EXPERIMENTAIS
    story.append(Paragraph("7. Resultados Experimentais", h1_style))
    story.append(Paragraph(
        "A Tabela 1 apresenta as médias e desvios obtidos na validação cruzada (5 folds no treino). A Tabela 2 apresenta o desempenho definitivo no conjunto de teste independente.",
        body_style
    ))

    # Tabela 1
    t1_data = [
        [Paragraph("Modelo (5-Fold CV Treino)", table_header_style), Paragraph("MAE Médio (US$)", table_header_style), Paragraph("Desvio MAE", table_header_style), Paragraph("RMSE Médio (US$)", table_header_style), Paragraph("Desvio RMSE", table_header_style), Paragraph("R² Médio", table_header_style)],
        [Paragraph("Regressão Linear", table_cell_style), Paragraph("801,06", table_cell_right), Paragraph("± 5,12", table_cell_center), Paragraph("1.207,56", table_cell_right), Paragraph("± 23,91", table_cell_center), Paragraph("0,909 ± 0,003", table_cell_center)],
        [Paragraph("Random Forest (base)", table_cell_style), Paragraph("<b>271,93</b>", table_cell_right), Paragraph("± 4,49", table_cell_center), Paragraph("<b>551,45</b>", table_cell_right), Paragraph("± 14,48", table_cell_center), Paragraph("<b>0,981 ± 0,001</b>", table_cell_center)],
    ]
    t_cv = Table(t1_data, colWidths=[140, 75, 65, 85, 75, 83])
    t_cv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, border_col),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Paragraph("<b>Tabela 1:</b> Desempenho em Validação Cruzada (5 folds) sobre o conjunto de treinamento.", caption_style))
    story.append(KeepTogether([t_cv]))
    story.append(Spacer(1, 6))

    # Tabela 2
    t2_data = [
        [Paragraph("Modelo Avaliado", table_header_style), Paragraph("MAE (US$)", table_header_style), Paragraph("RMSE (US$)", table_header_style), Paragraph("MSE", table_header_style), Paragraph("R² (Teste)", table_header_style), Paragraph("R² (Treino)", table_header_style), Paragraph("T. Treino", table_header_style)],
        [Paragraph("Regressão Linear", table_cell_style), Paragraph("797,91", table_cell_right), Paragraph("1.215,80", table_cell_right), Paragraph("1.478.170", table_cell_right), Paragraph("0,905", table_cell_center), Paragraph("0,909", table_cell_center), Paragraph("0,01 s", table_cell_center)],
        [Paragraph("Random Forest (base)", table_cell_style), Paragraph("<b>264,68</b>", table_cell_right), Paragraph("<b>524,78</b>", table_cell_right), Paragraph("<b>275.390</b>", table_cell_right), Paragraph("<b>0,982</b>", table_cell_center), Paragraph("0,997", table_cell_center), Paragraph("7,55 s", table_cell_center)],
        [Paragraph("Random Forest (ajustado)", table_cell_style), Paragraph("263,00", table_cell_right), Paragraph("519,49", table_cell_right), Paragraph("269.871", table_cell_right), Paragraph("0,983", table_cell_center), Paragraph("0,997", table_cell_center), Paragraph("10,76 s", table_cell_center)],
        [Paragraph("Regressão Linear (log)", table_cell_style), Paragraph("457,79", table_cell_right), Paragraph("876,76", table_cell_right), Paragraph("768.703", table_cell_right), Paragraph("0,951", table_cell_center), Paragraph("0,950", table_cell_center), Paragraph("0,01 s", table_cell_center)],
    ]
    t_test = Table(t2_data, colWidths=[130, 65, 65, 75, 55, 60, 73])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, border_col),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Paragraph("<b>Tabela 2:</b> Resultados finais comparativos sobre o conjunto de teste independente (10.755 amostras).", caption_style))
    story.append(KeepTogether([t_test]))
    story.append(Spacer(1, 6))

    if os.path.exists("figuras/comparacao_metricas.png"):
        story.append(KeepTogether([
            Image("figuras/comparacao_metricas.png", width=515, height=130),
            Paragraph("<b>Figura 4:</b> Comparação gráfica das métricas de erro (MAE e RMSE) e aderência (R²) no teste independente.", caption_style)
        ]))

    if os.path.exists("figuras/previsto_vs_real.png"):
        story.append(KeepTogether([
            Image("figuras/previsto_vs_real.png", width=470, height=165),
            Paragraph("<b>Figura 5:</b> Valores Previstos versus Reais. A dispersão do Random Forest alinha-se estreitamente à diagonal perfeita.", caption_style)
        ]))

    if os.path.exists("figuras/residuos.png"):
        story.append(KeepTogether([
            Image("figuras/residuos.png", width=470, height=150),
            Paragraph("<b>Figura 6:</b> Dispersão de Resíduos (Real − Previsto). Nota-se forte heterocedasticidade e curvatura na Regressão Linear.", caption_style)
        ]))

    # 8. ANÁLISE COMPARATIVA DETALHADA
    story.append(Paragraph("8. Análise Comparativa Detalhada", h1_style))
    story.append(Paragraph(
        "<b>1. Confronto Geral de Performance:</b> O Random Forest superou a Regressão Linear com larga margem: o RMSE caiu de US$ 1.215,80 para US$ 524,78 (<b>redução de 56,8%</b>), o MAE reduziu de US$ 797,91 para US$ 264,68 (<b>redução de 66,8%</b>), e o R² aumentou de 0,905 para <b>0,982</b>. Na validação cruzada, a diferença média de erro entre modelos supera em dezenas de vezes a oscilação entre os folds, comprovando que o ganho é genuíno e independente do particionamento.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Limitação Crítica da Regressão Linear:</b> Por forçar uma reta em uma curva convexa, a Regressão Linear superestima o valor de pedras intermediárias e subestima drasticamente pedras pequenas, gerando <b>888 predições de preços negativos</b> (8,3% do conjunto de teste). Para diamantes abaixo de US$ 1.000, o modelo linear obteve um erro percentual médio de <b>102,2%</b> (Tabela 3), prevendo, por exemplo, <i>−US$ 1.391,00</i> para uma pedra de 0,30 ct.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Consistência do Random Forest:</b> O modelo baseado em árvores manteve uma margem de erro percentual estável (entre <b>5,6% e 7,3%</b>) em todas as categorias de preço (Figura 7), sem produzir nenhuma estimativa negativa.",
        body_style
    ))

    # Tabela 3
    t3_data = [
        [Paragraph("Faixa de Preço Real", table_header_style), Paragraph("Amostras (n)", table_header_style), Paragraph("MAE Reg. Linear", table_header_style), Paragraph("MAPE Reg. Linear", table_header_style), Paragraph("MAE Random Forest", table_header_style), Paragraph("MAPE Random Forest", table_header_style)],
        [Paragraph("&lt; US$ 1.000", table_cell_style), Paragraph("2.926", table_cell_center), Paragraph("US$ 651,70", table_cell_right), Paragraph("<b>102,2%</b>", table_cell_center), Paragraph("<b>US$ 38,80</b>", table_cell_right), Paragraph("<b>5,6%</b>", table_cell_center)],
        [Paragraph("US$ 1.000 – 2.500", table_cell_style), Paragraph("2.544", table_cell_center), Paragraph("US$ 526,70", table_cell_right), Paragraph("35,4%", table_cell_center), Paragraph("US$ 102,80", table_cell_right), Paragraph("6,1%", table_cell_center)],
        [Paragraph("US$ 2.500 – 5.000", table_cell_style), Paragraph("2.384", table_cell_center), Paragraph("US$ 611,70", table_cell_right), Paragraph("17,1%", table_cell_center), Paragraph("US$ 266,50", table_cell_right), Paragraph("7,3%", table_cell_center)],
        [Paragraph("US$ 5.000 – 10.000", table_cell_style), Paragraph("1.917", table_cell_center), Paragraph("US$ 905,70", table_cell_right), Paragraph("12,9%", table_cell_center), Paragraph("US$ 478,90", table_cell_right), Paragraph("6,9%", table_cell_center)],
        [Paragraph("&gt; US$ 10.000", table_cell_style), Paragraph("984", table_cell_center), Paragraph("US$ 2.175,10", table_cell_right), Paragraph("15,5%", table_cell_center), Paragraph("US$ 933,20", table_cell_right), Paragraph("6,9%", table_cell_center)],
    ]
    t_faixas = Table(t3_data, colWidths=[100, 65, 85, 90, 95, 88])
    t_faixas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, border_col),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(Paragraph("<b>Tabela 3:</b> Decomposição de erros monetários (MAE) e percentuais (MAPE) por faixa de preço real no teste.", caption_style))
    story.append(KeepTogether([t_faixas]))
    story.append(Spacer(1, 6))

    if os.path.exists("figuras/erro_por_faixa.png"):
        story.append(KeepTogether([
            Image("figuras/erro_por_faixa.png", width=470, height=148),
            Paragraph("<b>Figura 7:</b> Erro monetário absoluto (MAE) e erro relativo percentual médio (MAPE) por faixa de valor de mercado.", caption_style)
        ]))

    story.append(Paragraph(
        "<b>4. Importância de Atributos e Coeficientes:</b> A decomposição por impureza de Gini no Random Forest (Figura 8) indica que <code>carat</code> (<b>58,98%</b>) e <code>y</code> (<b>29,69%</b>) explicam quase 90% da formação do preço, seguidos por pureza (6,33%) e cor (3,27%). Lapidação (<code>cut</code>) contribui com menos de 0,2%. Na Regressão Linear, devido à multicolinearidade, o coeficiente da largura <code>x</code> resultou negativo, ilustrando o risco de interpretar pesos lineares sem controle de correlações internas.",
        body_style
    ))

    if os.path.exists("figuras/importancia.png"):
        story.append(KeepTogether([
            Image("figuras/importancia.png", width=470, height=150),
            Paragraph("<b>Figura 8:</b> Importância de variáveis no Random Forest e coeficientes lineares padronizados.", caption_style)
        ]))

    story.append(Paragraph(
        "<b>5. Impacto das Otimizações:</b> A Random Forest ajustada (<code>RandomizedSearchCV</code>) obteve RMSE de 519,49 (ganho de apenas 1,0%), demonstrando que o algoritmo com parâmetros padrão já explora com eficácia a informação disponível. A Regressão Linear com alvo em logaritmo melhorou o RMSE para US$ 876,76 (−27,9%) e eliminou as predições negativas, mas ainda permaneceu distante do Random Forest.",
        body_style
    ))

    # 9. CONCLUSÃO E TRABALHOS FUTUROS
    story.append(PageBreak())
    story.append(Paragraph("9. Conclusão", h1_style))
    story.append(Paragraph(
        "O estudo experimental demonstrou conclusivamente que o <b>Random Forest Regressor é a abordagem recomendada</b> para precificação de diamantes. O algoritmo é robusto à multicolinearidade, modela com precisão a convexidade peso × preço e preserva baixíssimo erro percentual em todo o portfólio. A Regressão Linear clássica mostrou-se inviável para uso direto em virtude de subajuste e predições negativas absurdas.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Limitações:</b> Como modelo baseado em árvores, o Random Forest não extrapola tendências além do preço máximo visto no treino (US$ 18.823). Para gemas superiores a 3,5 quilates, a predição atinge um platô artificial. A base também não contempla variáveis de mercado como fluorescência UV e certificado gemológico.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Trabalhos Futuros:</b> Sugere-se a aplicação de <i>Gradient Boosting</i> (XGBoost/LightGBM) com perdas quantílicas para geração de faixas de confiança de preço e a criação de atributos de volume (<code>x·y·z</code>).",
        body_style
    ))

    # 10. REFERÊNCIAS BIBLIOGRÁFICAS
    story.append(Paragraph("10. Referências Bibliográficas", h1_style))
    refs = [
        "BREIMAN, L. Random Forests. <b>Machine Learning</b>, v. 45, n. 1, p. 5–32, 2001.",
        "GÉRON, A. <b>Mãos à Obra: Aprendizado de Máquina com Scikit-Learn, Keras & TensorFlow</b>. 2. ed. Rio de Janeiro: Alta Books, 2021.",
        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. <b>Journal of Machine Learning Research</b>, v. 12, p. 2825–2830, 2011.",
        "WASKOM, M. seaborn-data: Data repository for Seaborn. Disponível em: &lt;https://github.com/mwaskom/seaborn-data&gt;. Acesso em: 23 nov. 2026.",
        "WICKHAM, H. <b>ggplot2: Elegant Graphics for Data Analysis</b>. 2. ed. New York: Springer, 2016.",
        "SCIKIT-LEARN. <b>Scikit-learn User Guide: Supervised learning — Linear Models & Ensemble Methods</b>. Disponível em: &lt;https://scikit-learn.org/stable/&gt;. Acesso em: 23 nov. 2026."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle(
            "RefStyle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.8,
            textColor=dark_text,
            leftIndent=14,
            firstLineIndent=-14,
            spaceAfter=3.5
        )))

    # Constrói o PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório PDF gerado com sucesso: {pdf_filename}")

if __name__ == "__main__":
    gerar_pdf()
