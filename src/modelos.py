class Midia:
    """
    Classe base para Filme e Série.
    Define atributos comuns (título, gênero, ano, status) e futuramente os métodos básicos
    """
    def __init__(self,titulo,tipo,genero,ano,duracao_minutos,classificacao_indicativa,elenco,status):
        pass
    

class Filme(Midia):
    """
    Representa um Filme. Herda características básicas de Midia.
    Contém atributos específicos como duração total e nota individual.
    """
    def __init__(self, titulo, genero, ano, classificacao, elenco, duracao_minutos):
        pass
    
    
class Serie(Midia):
    """
    Representa uma Série. Herda características básicas de Midia e contém a estrutura de Temporadas e Episódios.
    É responsável por calcular sua nota média e gerenciar a mudança automática de status 
    (tornar-se 'ASSISTIDA' quando todos os episódios forem concluídos).
    """
    def __init__(self, titulo, genero, ano, classificacao, elenco):
        pass
    

class Temporada:
    """
    Uma das estruturas de composição da Série.
    Representa uma Temporada de uma Série.
    Atua como um container que agrega objetos Episodio.
    """
    def __init__(self,numero_episodios, duracao_total_minutos,numero_temporada):
        pass
    

class Episodio:
    """
    Representa um Episódio. É a menor unidade de mídia avaliável dentro de uma Série.
    Contém detalhes como número, título, duração, nota e status de visualização.
    """
    def __init__(self,numero_episodio,titulo,duraco,data_lancamento):
        pass
    

class Usuario:
    """
    Gerencia as coleções e o histórico de um usuário.
    Possui listas personalizadas (ListaPersonalizada) e registra o histórico de visualização.
    """
    def __init__(self,nome,listas,historico):
        pass
    

class ListaPersonalizada:
    """
    Define uma lista customizada do usuário ("Para assistir", "Favoritos", etc.).
    Contém uma coleção de objetos Midia. O limite é definido em settings.json.
    """
    def __init__(self,nome,midias):
        pass
    
class HistoricoItem:
    """
    Um item no histórico de visualização do usuário.
    Registra a mídia concluída e a data/hora exata de conclusão, essencial para relatórios de consumo.
    """
    def __init__(self,midia, data_conclusao):
        pass
    