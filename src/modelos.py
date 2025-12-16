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
            raise ValueError("O status deve ser uma das opções: NÃO ASSISTIDO, ASSISTINDO OU ASSISTIDO")
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
        
        #Inicializa a estrutura de composição: um dicionário para armazenar Temporada
        self._temporadas = {} #Chave: número da temporada (int), Valor: objeto Temporada

    #Metodo para adicionar temporadas na série
    def adicionar_temporada(self, temporada):

        #Verifica se o objeto recebido é da classe Temporada
        if not isinstance(temporada,Temporada):
            raise TypeError("Somente temporadas podem ser adicionadas a uma série")
        
        #Verifica a unicidade da temporada
        numero_temporada = temporada.numero
        if numero_temporada in self._temporadas:
            raise ValueError(f"A Temporada de número {numero_temporada} já existe nesta série.")
        
        #Adiciona o objeto temporada ao dicionario
        self._temporadas[numero_temporada]= temporada

    #Metodo para calcular a nota média da série com base nas notas de todos os episodios que foram avaliados
    def calcular_nota_serie(self):
        totalNotas=0
        contadorAvaliacao=0
        for temporada in self._temporadas.values():
            for episodio in temporada._episodios.values():
                if episodio.nota is not None:
                     totalNotas+=episodio.nota
                     contadorAvaliacao+=1
        
        if contadorAvaliacao==0:
            return None
        
        media=totalNotas/contadorAvaliacao
        return round(media,2)
    
    #Metodo para atualização automatica do status da série
    #Atualiza o status da Série baseando-se na conclusão dos episódios.
    #Se novos episódios não assistidos forem detectados, o status retrocede de ASSISTIDA para ASSISTINDO.
    
    def atualizar_status_automatico(self):
   
        if not self._temporadas:
            #Se não há temporadas, mantém como está ou define padrão
            return 
            
        todos_concluidos = True
        pelo_menos_um_visto = False
        
        #Percorre a hierarquia de composição: Série -> Temporadas -> Episódios
        for temporada in self._temporadas.values():
            for episodio in temporada._episodios.values(): 
                if episodio.status == "ASSISTIDO":
                    pelo_menos_um_visto = True
                else:
                    todos_concluidos = False

        #Aplicação da Regra de Negócio de Transição de Status
        if todos_concluidos:
            self.status = "ASSISTIDO"
        elif pelo_menos_um_visto:
            self.status = "ASSISTINDO"
        else:
            self.status = "NÃO ASSISTIDO"


          
from datetime import date

class Episodio:
    """
    Representa um Episódio. É a menor unidade de mídia avaliável dentro de uma Série.
    Contém detalhes como número, título, duração, nota e status de visualização.
    """
    def __init__(self, numero: int, titulo: str, duracao: int, data_lancamento=None , nota: float = None, status: str = "NÃO ASSISTIDO"):

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
    def __init__(self,numero_temporada: int):

        self._numero=None
        
        self._episodios={}

        self.numero=numero_temporada

    #getter para número de episodios
    @property
    def numero(self):
        return self._numero
    
    #setter para o numero de episódios, verifica se é um número inteiro positivo
    @numero.setter
    def numero(self,novo_numero:int):
        if not isinstance(novo_numero, int) or novo_numero <= 0:
            raise ValueError("O numero da temporada deve ser um inteiro positivo")
        self._numero=novo_numero


    #Métodos Especias:

    #Método para calcular o número total de episodios por temporada
    def __len__(self):
        return len(self._episodios)
    
    #Método para adicionar episodios
    def adicionar_episodio(self,episodio):

        #Verificação se o objeto recebido pertence a classe Episódio
        if not isinstance(episodio,Episodio):
            raise TypeError("Apenas episodios podem ser adicionados á uma temporada")
        
        #Verificação da unicidade do episódio
        numero_episodio=episodio.numero
        if numero_episodio in self._episodios:
            raise ValueError(f"O Episódio de número {numero_episodio} já existe na Temporada {self.numero}.")

        self._episodios[numero_episodio]=episodio


class Usuario:
    """
    Gerencia as coleções e o histórico de um usuário.
    Possui listas personalizadas (ListaPersonalizada) e registra o histórico de visualização.
    """
    def __init__(self, nome: str, limite_listas: int = 5):
        
        #Inicializa atributos básicos
        self._nome = nome
        self._limite_listas = limite_listas 
        
        #Inicializa as coleções de Composição
        self._listas = {}  
        self._historico = [] 

    #getter para as listas personalizadas
    @property
    def listas(self):
        """Retorna o dicionário de listas personalizadas."""
        return self._listas

    
    def criar_lista(self, nome_lista: str):
        """
        Cria uma nova ListaPersonalizada, aplicando a regra de limite.
        """
        nome_normalizado = nome_lista.strip().upper()
        
        if nome_normalizado in self._listas:
            raise ValueError(f"A lista '{nome_lista}' já existe.")

        #Verifica o limite lido do settings.json
        if len(self._listas) >= self._limite_listas:
            raise ValueError(
                f"Limite de listas atingido. O usuário pode ter no máximo {self._limite_listas} listas."
            )

        #Criação e adição da ListaPersonalizada
        nova_lista = ListaPersonalizada(nome_normalizado)
        self._listas[nome_normalizado] = nova_lista
        return nova_lista

    #Metodo para adicionar uma mídia concluída ao histórico.
    def adicionar_ao_historico(self, midia, data_conclusao):
        #A validação de status 'ASSISTIDO'será feita no construtor do HistoricoItem
        item = HistoricoItem(midia, data_conclusao) 
        self._historico.append(item)

class ListaPersonalizada:
    """
    Define uma lista customizada do usuário ("Para assistir", "Favoritos", etc.).
    Contém uma coleção de objetos Midia. O limite é definido em settings.json.
    """
   
    def __init__(self, nome: str):
            self._nome = nome
            self._midias = [] # Lista de objetos Midia

    
    #Adiciona uma Midia a lista
    def adicionar_midia(self, midia):

        #Validação de tipo
        if not isinstance(midia, Midia):
            raise TypeError("Apenas objetos do tipo Midia (Filme ou Série) podem ser adicionados à lista.")
            
        #Validação de unicidade na lista
        if midia in self._midias:
            raise ValueError(f"'{midia.titulo}' já está na lista '{self._nome}'.")
            
        self._midias.append(midia)

    #Método para remover uma Midia da lista   
    def remover_midia(self, titulo_remover):
        """Procura a mídia pelo título e remove o objeto correspondente."""
        # Normaliza o título para a busca (minúsculas e sem espaços extras)
        titulo_remover = titulo_remover.strip().lower()
        
        midia_encontrada = None
        for midia in self._midias:
            if midia.titulo.lower() == titulo_remover:
                midia_encontrada = midia
                break
        
        if midia_encontrada:
            self._midias.remove(midia_encontrada)
            return True
        else:
            # Lança uma exceção amigável ou retorna False
            raise ValueError(f"Mídia '{titulo_remover}' não encontrada na lista.")

    #Método Especial para retornar o número de mídias na lista
    def __len__(self):
        return len(self._midias)
    

class HistoricoItem:
    """
    Um item no histórico de visualização do usuário.
    Registra a mídia concluída e a data/hora exata de conclusão, essencial para relatórios de consumo.
    """
    def __init__(self,midia, data_conclusao):

        #Verifica se o objeto a ser recebidp é uma Mídia(Filme ou Série)
        if not isinstance(midia, Midia):
            raise TypeError("Apenas objetos Midia podem ser registrados no histórico.")
            
        #Verifica se a mídia está concluída
        if midia.status != "ASSISTIDO":
            raise ValueError("Somente mídias concluídas ('ASSISTIDO') podem ser adicionadas ao histórico.")
        
        self._midia = midia
        self._data_conclusao = data_conclusao

    #getter para a duração da mídia    
    @property
    def duracao_concluida(self):
        #Para Filmes, acessa a propriedade duracao da classe Filme
        if self._midia._tipo == "FILME":
            return self._midia.duracao
        
        #Para Séries, deve-se somar a duração dos episódios assistidos
        if self._midia._tipo == "SERIE":
            duracao_serie = 0
            for temporada in self._midia._temporadas.values():
                for episodio in temporada._episodios.values():
                    # Adiciona a duração de cada episódio
                    duracao_serie += episodio.duracao
            return duracao_serie
        
        #Caso não seja um tipo válido
        return 0
    
    #Método especial para a exibição
    def __str__(self):
        return f"Registro: {self._midia.titulo} concluído em {self._data_conclusao.strftime('%Y-%m-%d')}"
       
    