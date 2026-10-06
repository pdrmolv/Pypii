import pygame
import random
import math

pygame.init()

# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 800
ALTURA = 600

TAMANHO_CELULA = 25

# Área do jogo
MARGEM_X = 25
MARGEM_Y = 50

COLUNAS = (LARGURA - MARGEM_X * 2) // TAMANHO_CELULA
LINHAS = (ALTURA - MARGEM_Y - 25) // TAMANHO_CELULA

AREA_X = MARGEM_X
AREA_Y = MARGEM_Y

FPS = 120

# Tempo de movimento entre uma célula e outra
TEMPO_MOVIMENTO = 0.095

# ============================================================
# CORES
# ============================================================

PRETO = (10, 10, 10)
CINZA_QUADRICULADO = (38, 38, 38)
CINZA_BORDA = (90, 90, 90)

VERMELHO = (220, 20, 30)
VERMELHO_CABECA = (245, 35, 45)
VERMELHO_ESCUR0 = (155, 10, 20)

VERDE = (35, 220, 80)

BRANCO = (240, 240, 240)

# ============================================================
# JANELA
# ============================================================

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 32)
fonte_game_over = pygame.font.Font(None, 70)
fonte_inicio = pygame.font.Font(None, 42)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def centro_da_celula(posicao):
    """Transforma coordenadas de grade em coordenadas da tela."""

    coluna, linha = posicao

    x = AREA_X + coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
    y = AREA_Y + linha * TAMANHO_CELULA + TAMANHO_CELULA // 2

    return pygame.Vector2(x, y)


def criar_comida(cobra):
    """Cria a comida em uma célula que não está ocupada."""

    celulas_livres = []

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            posicao = (coluna, linha)

            if posicao not in cobra:
                celulas_livres.append(posicao)

    if not celulas_livres:
        return None

    return random.choice(celulas_livres)


def reiniciar():

    # Cobra inicial
    cobra = [
        (15, 10),
        (14, 10),
        (13, 10),
        (12, 10)
    ]

    direcao = (1, 0)
    proxima_direcao = (1, 0)

    comida = criar_comida(cobra)

    pontos = 0

    perdeu = False

    return (
        cobra,
        direcao,
        proxima_direcao,
        comida,
        pontos,
        perdeu
    )


# ============================================================
# DESENHAR QUADRICULADO
# ============================================================

def desenhar_quadriculado():

    # Fundo preto
    tela.fill(PRETO)

    # Linhas verticais
    for coluna in range(COLUNAS + 1):

        x = AREA_X + coluna * TAMANHO_CELULA

        pygame.draw.line(
            tela,
            CINZA_QUADRICULADO,
            (x, AREA_Y),
            (x, AREA_Y + LINHAS * TAMANHO_CELULA),
            1
        )

    # Linhas horizontais
    for linha in range(LINHAS + 1):

        y = AREA_Y + linha * TAMANHO_CELULA

        pygame.draw.line(
            tela,
            CINZA_QUADRICULADO,
            (AREA_X, y),
            (AREA_X + COLUNAS * TAMANHO_CELULA, y),
            1
        )

    # Borda externa
    pygame.draw.rect(
        tela,
        CINZA_BORDA,
        (
            AREA_X,
            AREA_Y,
            COLUNAS * TAMANHO_CELULA,
            LINHAS * TAMANHO_CELULA
        ),
        2
    )


# ============================================================
# DESENHAR LÍNGUA
# ============================================================

def desenhar_lingua(cabeca, direcao):

    centro = centro_da_celula(cabeca)

    dx, dy = direcao

    # Começo da língua
    inicio = centro + pygame.Vector2(dx, dy) * 8

    # Comprimento da língua
    fim = centro + pygame.Vector2(dx, dy) * 21

    # Linha principal da língua
    pygame.draw.line(
        tela,
        VERMELHO,
        inicio,
        fim,
        3
    )

    # Bifurcação da língua
    perpendicular = pygame.Vector2(-dy, dx)

    ponta1 = fim + perpendicular * 4
    ponta2 = fim - perpendicular * 4

    pygame.draw.line(
        tela,
        VERMELHO,
        fim,
        ponta1,
        2
    )

    pygame.draw.line(
        tela,
        VERMELHO,
        fim,
        ponta2,
        2
    )


# ============================================================
# DESENHAR COBRA COM INTERPOLAÇÃO
# ============================================================

def desenhar_cobra(cobra, direcao, progresso):

    # --------------------------------------------------------
    # DESENHAR CORPO
    # --------------------------------------------------------

    for i in range(len(cobra) - 1, -1, -1):

        posicao_atual = centro_da_celula(cobra[i])

        # O corpo não precisa interpolar visualmente da mesma
        # maneira que a cabeça porque ele segue a posição anterior.
        if i > 0:

            posicao_anterior = centro_da_celula(cobra[i - 1])

            posicao = posicao_atual.lerp(
                posicao_anterior,
                progresso
            )

        else:

            # Cabeça
            posicao_anterior = centro_da_celula(
                (
                    cobra[0][0] - direcao[0],
                    cobra[0][1] - direcao[1]
                )
            )

            posicao = posicao_anterior.lerp(
                posicao_atual,
                progresso
            )

        raio = TAMANHO_CELULA // 2 - 3

        if i == 0:
            cor = VERMELHO_CABECA
        else:
            cor = VERMELHO

        pygame.draw.circle(
            tela,
            cor,
            (round(posicao.x), round(posicao.y)),
            raio
        )

    # --------------------------------------------------------
    # CABEÇA
    # --------------------------------------------------------

    cabeca_atual = centro_da_celula(cobra[0])

    cabeca_anterior = centro_da_celula(
        (
            cobra[0][0] - direcao[0],
            cobra[0][1] - direcao[1]
        )
    )

    cabeca = cabeca_anterior.lerp(
        cabeca_atual,
        progresso
    )

    dx, dy = direcao

    # --------------------------------------------------------
    # OLHOS
    # --------------------------------------------------------

    frente = pygame.Vector2(dx, dy)
    lado = pygame.Vector2(-dy, dx)

    olho_esquerdo = (
        cabeca
        + frente * 5
        + lado * 5
    )

    olho_direito = (
        cabeca
        + frente * 5
        - lado * 5
    )

    pygame.draw.circle(
        tela,
        BRANCO,
        (round(olho_esquerdo.x), round(olho_esquerdo.y)),
        3
    )

    pygame.draw.circle(
        tela,
        BRANCO,
        (round(olho_direito.x), round(olho_direito.y)),
        3
    )

    # Pupilas
    pygame.draw.circle(
        tela,
        PRETO,
        (
            round(olho_esquerdo.x + dx),
            round(olho_esquerdo.y + dy)
        ),
        1
    )

    pygame.draw.circle(
        tela,
        PRETO,
        (
            round(olho_direito.x + dx),
            round(olho_direito.y + dy)
        ),
        1
    )

    # --------------------------------------------------------
    # LÍNGUA
    # --------------------------------------------------------

    inicio = cabeca + frente * 8
    fim = cabeca + frente * 22

    pygame.draw.line(
        tela,
        VERMELHO_ESCUR0,
        (
            round(inicio.x),
            round(inicio.y)
        ),
        (
            round(fim.x),
            round(fim.y)
        ),
        3
    )

    # Bifurcação
    ponta_esquerda = fim + lado * 4
    ponta_direita = fim - lado * 4

    pygame.draw.line(
        tela,
        VERMELHO_ESCUR0,
        (
            round(fim.x),
            round(fim.y)
        ),
        (
            round(ponta_esquerda.x),
            round(ponta_esquerda.y)
        ),
        2
    )

    pygame.draw.line(
        tela,
        VERMELHO_ESCUR0,
        (
            round(fim.x),
            round(fim.y)
        ),
        (
            round(ponta_direita.x),
            round(ponta_direita.y)
        ),
        2
    )


# ============================================================
# DESENHAR COMIDA
# ============================================================

def desenhar_comida(comida):

    if comida is None:
        return

    centro = centro_da_celula(comida)

    # Pequeno brilho
    pygame.draw.circle(
        tela,
        (15, 100, 40),
        (
            round(centro.x),
            round(centro.y)
        ),
        9
    )

    # Círculo verde
    pygame.draw.circle(
        tela,
        VERDE,
        (
            round(centro.x),
            round(centro.y)
        ),
        6
    )


# ============================================================
# INÍCIO
# ============================================================

(
    cobra,
    direcao,
    proxima_direcao,
    comida,
    pontos,
    perdeu
) = reiniciar()

tempo_movimento = 0

rodando = True

# ============================================================
# LOOP PRINCIPAL
# ============================================================

while rodando:

    dt = clock.tick(FPS) / 1000

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            # Reiniciar
            if evento.key == pygame.K_r and perdeu:

                (
                    cobra,
                    direcao,
                    proxima_direcao,
                    comida,
                    pontos,
                    perdeu
                ) = reiniciar()

                tempo_movimento = 0

            # CIMA
            elif evento.key in (pygame.K_UP, pygame.K_w):

                if direcao != (0, 1):
                    proxima_direcao = (0, -1)

            # BAIXO
            elif evento.key in (pygame.K_DOWN, pygame.K_s):

                if direcao != (0, -1):
                    proxima_direcao = (0, 1)

            # ESQUERDA
            elif evento.key in (pygame.K_LEFT, pygame.K_a):

                if direcao != (1, 0):
                    proxima_direcao = (-1, 0)

            # DIREITA
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):

                if direcao != (-1, 0):
                    proxima_direcao = (1, 0)

    # --------------------------------------------------------
    # ATUALIZAÇÃO DO JOGO
    # --------------------------------------------------------

    if not perdeu:

        tempo_movimento += dt

        progresso = min(
            tempo_movimento / TEMPO_MOVIMENTO,
            1
        )

        # ----------------------------------------------------
        # MOVIMENTAR UMA CÉLULA
        # ----------------------------------------------------

        if tempo_movimento >= TEMPO_MOVIMENTO:

            tempo_movimento -= TEMPO_MOVIMENTO

            # Atualiza direção
            direcao = proxima_direcao

            cabeca_x, cabeca_y = cobra[0]

            nova_cabeca = (
                cabeca_x + direcao[0],
                cabeca_y + direcao[1]
            )

            # ------------------------------------------------
            # COLISÃO COM BORDA
            # ------------------------------------------------

            if (
                nova_cabeca[0] < 0
                or nova_cabeca[0] >= COLUNAS
                or nova_cabeca[1] < 0
                or nova_cabeca[1] >= LINHAS
            ):
                perdeu = True

            # ------------------------------------------------
            # COLISÃO COM O CORPO
            # ------------------------------------------------

            elif nova_cabeca in cobra[:-1]:
                perdeu = True

            else:

                # Adiciona cabeça
                cobra.insert(0, nova_cabeca)

                # ------------------------------------------------
                # COMER
                # ------------------------------------------------

                if nova_cabeca == comida:

                    pontos += 1

                    comida = criar_comida(cobra)

                else:

                    # Remove cauda
                    cobra.pop()

            progresso = 0

    else:

        progresso = 0

    # --------------------------------------------------------
    # DESENHAR
    # --------------------------------------------------------

    desenhar_quadriculado()

    desenhar_comida(comida)

    desenhar_cobra(
        cobra,
        direcao,
        progresso
    )

    # --------------------------------------------------------
    # PONTUAÇÃO
    # --------------------------------------------------------

    texto = fonte.render(
        f"Pontos: {pontos}",
        True,
        BRANCO
    )

    tela.blit(
        texto,
        (AREA_X, 15)
    )

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    if perdeu:

        # Fundo escurecido transparente
        camada = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada.fill((0, 0, 0, 150))

        tela.blit(camada, (0, 0))

        texto_game_over = fonte_game_over.render(
            "GAME OVER",
            True,
            VERMELHO
        )

        texto_r = fonte_inicio.render(
            "Pressione R para jogar novamente",
            True,
            BRANCO
        )

        tela.blit(
            texto_game_over,
            (
                LARGURA // 2 - texto_game_over.get_width() // 2,
                ALTURA // 2 - 60
            )
        )

        tela.blit(
            texto_r,
            (
                LARGURA // 2 - texto_r.get_width() // 2,
                ALTURA // 2 + 20
            )
        )

    pygame.display.flip()

pygame.quit()