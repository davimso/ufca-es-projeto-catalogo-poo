class Midia:
    """
    Classe base para Filme e Série.
    Define atributos comuns (título, gênero, ano, status) e futuramente os métodos básicos
    """
    def __init__(self,titulo,tipo,genero,ano,duracao_minutos,classificacao_indicativa,elenco,status):

        #Inicializando os atributos que serão validados
        self._titulo=None
        self._ano=None
        self._status=None
        
        #Inicializando os demais atributos
        self._tipo=tipo
        self._genero=genero
        self._duracao=duracao_minutos
        self._classificacao=classificacao_indicativa
        self._elenco=elenco

        #Chamando os setters implementados
        self.titulo=titulo
        self.status=status
        self.ano=ano

    # getter para o título
    @property
    def titulo(self):
        return self._titulo

    # setter para o título, não permite títulos vazios
    @titulo.setter
    def titulo(self,novo_titulo):
        if not novo_titulo or not novo_titulo.strip():
            raise ValueError("Título não pode ser vazio")
        self._titulo=novo_titulo

    # getter para o status
    @property
    def status(self):
        return self._status
    
    #setter para o status, permite apenas os valores definidos: NÃO ASSISTIDO, ASSISTIDO E ASSISTINDO
    @status.setter
    def status(self, novo_status:str):
        opcoes={"NÃO ASSISTIDO", "ASSISTIDO", "ASSISTINDO"}
        if novo_status.strip().upper() not in opcoes:
            raise ValueError("Status inválido")
        self._status=novo_status.strip().upper()
    
    #getter para o ano
    @property
    def ano(self):
        return self._ano
    
    #setter para o ano, permite apenas valores inteiros positivo
    @ano.setter
    def ano(self,novo_ano:int):
        if not isinstance(novo_ano, int) or novo_ano<=0:
            raise ValueError("O ano deve ser um inteiro positivo")
        self._ano=novo_ano

    #Métodos especiais:

    #Compara o título,tipo e ano das midias, se forem iguais as midias são iguais
    def __eq__(self, other):
        if isinstance(other, Midia):
            return (self.titulo.lower() == other.titulo.lower() and 
                    self._tipo == other._tipo and 
                    self.ano == other.ano)
        return False
    
    
    #Retorna uma representação de string legível para o usuário
    def __str__(self):
        # Formato: [TIPO] Título (Ano) - Gênero: Gênero | Status: STATUS
        return f"[{self._tipo}] {self.titulo} ({self.ano}) - Gênero: {self._genero} | Status: {self._status}"
    
    
    #Retorna a representação oficial do objeto
    def __repr__(self):
        # Formato: <Midia(tipo='FILME', titulo='Inception', ano=2010)>
        return f"<Midia(tipo='{self._tipo}', titulo='{self.titulo}', ano={self.ano}, status='{self._status}')>"
    

class Filme(Midia):
    """
    Representa um Filme. Herda características básicas de Midia.
    Contém atributos específicos como duração total e nota individual.
    """
    def __init__(self, titulo, genero, ano, classificacao, elenco, duracao_minutos,status,nota):

        #Chama o construtor da classe base (Midia) e passa os parâmetros que Midia trata
        super().__init__(titulo, "FILME", genero, ano, duracao_minutos, classificacao, elenco, status)
        
        #Inicializando os atributos que serão validados
        self._nota = None
        self._data_conclusao = None 
        
        #Chama os setters para validar e armazenar os valores de Filme
        self.duracao = duracao_minutos
        self.nota = nota

    #getter para a duração
    @property
    def duracao(self):
        return self._duracao
    
    #setter para a duração, verifica se é um numero inteiro posistivo
    @duracao.setter
    def duracao(self,nova_duracao):
        if  not isinstance(nova_duracao,int) or nova_duracao <=0:
            raise ValueError("Duração deve ser um numero inteiro posistivo")
        self._duracao=nova_duracao


    #getter para a nota
    @property
    def nota(self):
        return self._nota
    
    #setter para a nota, verifica se é NONE, em caso negativo, verifica se é um float entre 0 e 10
    @nota.setter
    def nota(self, nova_nota):
        if nova_nota is not None:
            if not isinstance(nova_nota,float) or nova_nota < 0 or nova_nota > 10:
                raise ValueError("A nota deve ser deixada em branco ou um número entre 0 e 10")
        self._nota=nova_nota

    #Métodos especiais:

    #Define a ordenação para Filmes. Retorna True se o self.nota for menor que o other.nota
    def __lt__(self, other):
        if isinstance(other, Filme) and self.nota is not None and other.nota is not None:
            return self.nota < other.nota
        return False

    
    
class Serie(Midia):
    """
    Representa uma Série. Herda características básicas de Midia e contém a estrutura de Temporadas e Episódios.
    É responsável por calcular sua nota média e gerenciar a mudança automática de status 
    (torna-se 'ASSISTIDA' quando todos os episódios forem concluídos).
    """
    def __init__(self, titulo, genero, ano, classificacao, elenco):

        #Chama o construtor da clsse base
        super().__init__(titulo, "SERIE", genero, ano, 0, classificacao, elenco, "NÃO ASSISTIDO")
        
        #2. Inicializa a estrutura de composição: um dicionário para armazenar Temporada
        self._temporadas = {} #Chave: número da temporada (int), Valor: objeto Temporada
        
          
from datetime import date

class Episodio:
    """
    Representa um Episódio. É a menor unidade de mídia avaliável dentro de uma Série.
    Contém detalhes como número, título, duração, nota e status de visualização.
    """
    def __init__(self, numero: int, titulo: str, duracao: int, data_lancamento: date, nota: float = None, status: str = "NÃO ASSISTIDO"):

        #Inicializando atributos que serão validados
        self._numero = None
        self._duracao = None
        self._nota = None
        self._status = None

        self._titulo = titulo
        self._data_lancamento = data_lancamento

        # Chamando os setters para validar os valores
        self.numero = numero
        self.duracao = duracao
        self.status = status
        self.nota = nota


    #getter para o numero
    @property
    def numero(self):
        return self._numero

    #setter para o numero, vereifica se é um numero inteiro positivo 
    @numero.setter
    def numero(self, novo_numero: int):
        if not isinstance(novo_numero, int) or novo_numero <= 0:
            raise ValueError("O número do episódio deve ser um inteiro positivo.")
        self._numero = novo_numero

    
    #getter para a duração
    @property
    def duracao(self):
        return self._duracao

    #setter para a duração, verifica se é um numero inteiro positivo    
    @duracao.setter
    def duracao(self, nova_duracao: int):
        if not isinstance(nova_duracao, int) or nova_duracao <= 0:
            raise ValueError("A duração deve ser um número inteiro positivo.")
        self._duracao = nova_duracao


    #getter para a nota
    @property
    def nota(self):
        return self._nota

    #setter para a nota, verifica se é um numero entre 0 e 10  
    @nota.setter
    def nota(self, nova_nota: float):
        if nova_nota is not None:
            if not isinstance(nova_nota, (int, float)) or nova_nota < 0 or nova_nota > 10:
                raise ValueError("A nota deve ser um valor numérico entre 0 e 10.")
        self._nota = nova_nota


    #getter para o status
    @property
    def status(self):
        return self._status

    #setter para o status,verifica se está em uma das opções válidas
    @status.setter
    def status(self, novo_status: str):
        OPCOES_VALIDAS = {"NÃO ASSISTIDO", "ASSISTIDO", "ASSISTINDO"}
        status_normalizado = novo_status.strip().upper() 
        
        if status_normalizado not in OPCOES_VALIDAS:
            raise ValueError("Status inválido para episódio.")    
        self._status = status_normalizado


        #Métodos especiais:

        #Exibição formatada do episódio.
        def __str__(self):
            nota_str = f"Nota: {self.nota}" if self.nota is not None else "Não Avaliado"
            return f"Ep. {self.numero}: {self._titulo} ({self.duracao} min) - Status: {self.status} | {nota_str}"

class Temporada:
    """
    Uma das estruturas de composição da Série.
    Representa uma Temporada de uma Série.
    Atua como um container que agrega objetos Episodio.
    """
    def __init__(self,numero_episodios, duracao_total_minutos,numero_temporada):
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
    