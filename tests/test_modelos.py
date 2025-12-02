

import pytest
from src.modelos import Midia, Filme, Serie, Temporada, Episodio
from datetime import datetime, date

# --- Fixture de Dados Comuns (Ajudam a reutilizar objetos) ---

@pytest.fixture
def midia_valida():
    """Retorna uma Midia base válida para testes."""
    return Midia(
        titulo="O Ponto Fixo", 
        tipo="FILME", 
        genero="Sci-Fi", 
        ano=2024, 
        duracao_minutos=120, 
        classificacao_indicativa="16+", 
        elenco=[], 
        status="NÃO ASSISTIDO"
    )

@pytest.fixture
def filme_valido():
    """Retorna um Filme válido para testes."""
    return Filme(
        titulo="Matrix", 
        genero="Sci-Fi", 
        ano=1999, 
        classificacao="14+", 
        elenco=[], 
        duracao_minutos=136, 
        status="ASSISTIDO", 
        nota=9.0
    )

# ==============================================================================
# TESTES DE ENCAPSULAMENTO E VALIDAÇÃO (CRITÉRIO 1)
# ==============================================================================

### TESTES PARA CLASSE MIDIA (VALIDAÇÕES HERDADAS)

def test_midia_cria_com_sucesso(midia_valida):
    """Verifica se uma Midia base é criada corretamente."""
    assert midia_valida.titulo == "O Ponto Fixo"
    assert midia_valida.ano == 2024
    assert midia_valida.status == "NÃO ASSISTIDO"

def test_titulo_nao_pode_ser_vazio():
    """Testa se o setter de título rejeita strings vazias ou apenas espaços."""
    with pytest.raises(ValueError, match="Título não pode ser vazio"):
        Midia("", "FILME", "Acao", 2020, 100, "12+", [], "ASSISTINDO")
    with pytest.raises(ValueError):
        Midia("   ", "FILME", "Acao", 2020, 100, "12+", [], "ASSISTINDO")

def test_ano_deve_ser_positivo():
    """Testa se o setter de ano rejeita valores não inteiros ou negativos/zero."""
    with pytest.raises(ValueError, match="inteiro positivo"):
        Midia("Filme", "FILME", "Acao", 0, 100, "12+", [], "ASSISTINDO")
    with pytest.raises(ValueError):
        Midia("Filme", "FILME", "Acao", -2020, 100, "12+", [], "ASSISTINDO")

def test_status_deve_ser_valido():
    """Testa se o setter de status rejeita strings fora das opções válidas."""
    with pytest.raises(ValueError):
        midia_valida.status = "PENDENTE"
    
    midia_valida.status = "  assistinDO " # Deve normalizar e aceitar
    assert midia_valida.status == "ASSISTINDO"

### TESTES PARA CLASSE FILME (VALIDAÇÕES ESPECÍFICAS)

def test_filme_duracao_deve_ser_positivo(filme_valido):
    """Testa se o setter de duração rejeita valores não positivos."""
    with pytest.raises(ValueError, match="inteiro posistivo"):
        filme_valido.duracao = 0
    with pytest.raises(ValueError):
        filme_valido.duracao = -10

def test_filme_nota_deve_estar_entre_0_e_10(filme_valido):
    """Testa se o setter de nota rejeita valores acima de 10 ou abaixo de 0."""
    with pytest.raises(ValueError, match="entre 0 e 10"):
        filme_valido.nota = 10.1
    with pytest.raises(ValueError):
        filme_valido.nota = -0.5
        
    filme_valido.nota = 5.5 # Deve aceitar float
    assert filme_valido.nota == 5.5
    filme_valido.nota = None # Deve aceitar None
    assert filme_valido.nota is None

### TESTES PARA CLASSE EPISODIO (VALIDAÇÕES DE COMPOSIÇÃO)

def test_episodio_nota_duracao_valida():
    """Testa se o episódio rejeita valores inválidos de duração e nota."""
    with pytest.raises(ValueError):
        Episodio(1, "Ep", 0, date.today(), 9.0, "NÃO ASSISTIDO") # Duracao 0
    with pytest.raises(ValueError):
        Episodio(1, "Ep", 45, date.today(), 11, "NÃO ASSISTIDO") # Nota > 10

# ==============================================================================
# TESTES DE MÉTODOS ESPECIAIS (__eq__, __lt__)
# ==============================================================================

def test_igualdade_eq_funciona_para_duplicidade():
    """Testa se __eq__ retorna True apenas para duplicidade (titulo, tipo, ano)."""
    # Mídias IDÊNTICAS
    m1 = Midia("Filme X", "FILME", "A", 2024, 100, "L", [], "ASSISTIDO")
    m2 = Midia("Filme X", "FILME", "A", 2024, 100, "L", [], "ASSISTIDO")
    assert m1 == m2

    # Títulos Diferentes, Mas Outros Atributos Iguais
    m3 = Midia("Filme Y", "FILME", "A", 2024, 100, "L", [], "ASSISTIDO")
    assert m1 != m3

    # Tipo Diferente (Regra crucial)
    m4 = Midia("Filme X", "SERIE", "A", 2024, 100, "L", [], "ASSISTIDO")
    assert m1 != m4

    # Teste Case-Insensitive
    m5 = Midia("FILME X", "FILME", "A", 2024, 100, "L", [], "ASSISTIDO")
    assert m1 == m5

def test_ordenacao_lt_funciona_por_nota(filme_valido):
    """Testa se __lt__ ordena corretamente Filmes por nota."""
    filme_a = filme_valido
    filme_a.nota = 7.5
    filme_b = Filme("B", "C", 2020, "L", [], 90, "ASSISTIDO", 9.0)
    filme_c = Filme("C", "C", 2020, "L", [], 90, "ASSISTIDO", 6.0)

    # Verifica se a nota 7.5 é menor que 9.0 (True)
    assert filme_a < filme_b 
    
    # Verifica se a nota 9.0 NÃO é menor que 7.5 (False)
    assert not (filme_b < filme_a) 

    # Teste de ordenação (o menor vem primeiro)
    lista_filmes = [filme_a, filme_b, filme_c]
    lista_ordenada = sorted(lista_filmes) # Ordena usando __lt__
    
    # A ordem esperada é C (6.0), A (7.5), B (9.0)
    assert lista_ordenada[0].nota == 6.0
    assert lista_ordenada[-1].nota == 9.0

# ==============================================================================
# TESTES DE COMPOSIÇÃO BÁSICA E ESTRUTURA (SEMANA 3)
# ==============================================================================

def test_adicionar_episodio_temporada_funciona():
    """Testa se a Temporada adiciona e conta Episódios corretamente."""
    temporada = Temporada(numero_temporada=1)
    
    # Cria os episódios (a classe Episodio deve ser usada aqui)
    ep1 = Episodio(numero=1, titulo="Piloto", duracao=45, data_lancamento=date.today(), nota=8.0)
    ep2 = Episodio(numero=2, titulo="Fim", duracao=40, data_lancamento=date.today(), nota=9.0)
    
    temporada.adicionar_episodio(ep1)
    temporada.adicionar_episodio(ep2)
    
    # Testa o método especial __len__ na Temporada
    assert len(temporada) == 2 
    
    # Testa erro de duplicidade
    with pytest.raises(ValueError, match="já existe"):
        temporada.adicionar_episodio(Episodio(numero=1, titulo="Duplicado", duracao=30, data_lancamento=date.today()))

def test_adicionar_temporada_serie_funciona():
    """Testa se a Serie adiciona Temporadas e se o __len__ da Serie agrega corretamente."""
    serie = Serie("Série Z", "Drama", 2022, "10+", [])
    temp_a = Temporada(1)
    ep3 = Episodio(numero=3, titulo="Fim", duracao=30, data_lancamento=date.today())
    
    temp_a.adicionar_episodio(ep3) # len(temp_a) == 1
    
    serie.adicionar_temporada(temp_a)
    
    # Testa o len total da Serie (que deve somar os len das Temporadas)
    assert len(serie) == 1 
    
    # Testa erro de tipo
    with pytest.raises(TypeError, match="Somente temporadas"):
        serie.adicionar_temporada(filme_valido)