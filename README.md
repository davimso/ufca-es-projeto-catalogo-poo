VISÃO GERAL DO PROJETO:

Este projeto consiste no desenvolvimento de um Sistema de Linha de Comando (CLI) para gerenciar um catálogo pessoal de filmes e séries.



O objetivo principal é permitir ao usuário acompanhar seu consumo de mídia , comparando avaliações e controlando o progresso de séries e episódios.


Requisitos Arquiteturais e Técnicos:
A implementação deve seguir estritamente os princípios da Programação Orientada a Objetos (POO), com foco nos seguintes pilares:


Herança: Modelagem utilizando uma classe base (Midia) herdada por Filme e Serie.


Composição: Estrutura de agregação onde Serie contém Temporada, que contém Episodio.


Encapsulamento e Validação: Uso intensivo de @property para garantir a integridade dos dados, validando atributos como notas (0-10) e duração (>0).



Persistência: Os dados devem ser armazenados de forma simples, utilizando JSON ou SQLite.

O sistema incluirá funcionalidades essenciais como cadastro de mídias , avaliações , listas personalizadas e a geração de relatórios de consumo

UML TEXTUAL:

Classe: Midia (Classe Base)

Atributos Privados

_titulo: str

_tipo: str (FILME / SERIE)

_genero: str

_ano: int

_classificacao: str

_elenco: list[str]

_status: str (NÃO ASSISTIDO, ASSISTINDO, ASSISTIDO)

Métodos Públicos

__init__(...)

@property getters/setters

valida título não vazio

ano deve ser positivo

__eq__(other) -> bool (compara por título + tipo)

__str__() / __repr__() (formatação de exibição)

Relacionamentos e Notas

Herança: classe base de → Filme, → Serie

Regra de duplicidade: combinação (título + tipo + ano) deve ser única

Classe: Filme (Herda de Midia)

Atributos Privados

_duracao: int (minutos)

_nota: float (0–10)

_data_conclusao: datetime

Métodos Públicos

__init__(...)

@property duracao (validar > 0)

@property nota (validar 0–10)

avaliar(nota: float)

__lt__(other) -> bool (ordenação por nota média)

Relacionamentos e Notas

Herda completamente a estrutura de Midia

Classe: Serie (Herda de Midia)

Atributos Privados

_temporadas: dict[int, Temporada]

Métodos Públicos

__init__(...)

adicionar_temporada(...)

__len__() -> int (total de episódios)

calcular_nota_media_serie()

atualizar_status_automatico()

marca “ASSISTIDA” se todos os episódios concluídos

Relacionamentos e Notas

Composição: contém várias Temporada

A série agrega temporadas, que agregam episódios

Classe: Temporada

Atributos Privados

_numero: int

_episodios: dict[int, Episodio]

Métodos Públicos

adicionar_episodio(...)

Relacionamentos e Notas

Composição forte: possui vários Episodio

Classe: Episodio

Atributos Privados

_numero: int

_titulo: str

_duracao: int

_data_lancamento: date

_status: str

_nota: float | None

Métodos Públicos

@property numero (validar positivo)

@property duracao (validar > 0)

@property nota (validar 0–10)

avaliar(nota: float)

Relacionamentos e Notas

Episódio é uma entidade avaliável (nota 0–10)

Classe: Usuario

Atributos Privados

_nome: str

_listas: dict[str, ListaPersonalizada]

_historico: list[HistoricoItem]

Métodos Públicos

__init__(...)

criar_lista(nome: str)

adicionar_favorito(...)

Relacionamentos e Notas

Possui listas personalizadas

Mantém histórico (com data de conclusão)

Classe: ListaPersonalizada

Atributos Privados

_nome: str

_midias: list[Midia]

Métodos Públicos

adicionar_midia(...)

remover_midia(...)

Relacionamentos e Notas

Limite de listas é definido em settings.json

Classe: HistoricoItem

Atributos Privados

_midia: Midia

_data_conclusao: datetime

Métodos Públicos

__init__(...)

Relacionamentos e Notas

Usado para registrar a conclusão de mídias

ESTRUTURA PLANEJADA DE ARQUIVOS:

/projeto_catalogo                # Diretório raiz do projeto
├── src/                         # Código-fonte principal
│   ├── modelos.py               # Classes de POO (Midia, Filme, Serie, etc.)
│   │                             # + Lógica de negócio: herança, validações,
│   │                             #   encapsulamento, métodos especiais
│   ├── dados.py                 # Persistência (JSON/SQLite)
│   │                             # + Funções para salvar/carregar mídias,
│   │                             #   episódios, usuários e listas
│   │                             # + Rotina de seed
│   └── cli.py                   # Interface de Linha de Comando (CLI)
│                                 #   com subcomandos (ex: midia adicionar,
│                                 #   serie atualizar-status)
│
├── tests/                       # Testes unitários (pytest)
│                                 # Garantem integridade das regras e relatórios
│
├── settings.json                # Configurações do sistema
│                                 # (nota mínima p/ “recomendado”,
│                                 #  limite de listas personalizadas, etc.)
│
├── README.md                    # Documentação geral
│                                 # + UML textual
│                                 # + instruções de execução
│
└── .gitignore                   # Arquivos/pastas ignorados pelo Git
                                  # (venvs, caches, arquivo de persistência .db/.json)
