VISÃO GERAL DO PROJETO:

Este projeto consiste no desenvolvimento de um Sistema de Linha de Comando (CLI) (com a possibilidade de uma API mínima opcional, utilizando FastAPI ou Flask) para gerenciar um catálogo pessoal de filmes e séries.



O objetivo principal é permitir ao usuário acompanhar seu consumo de mídia , comparando avaliações e controlando o progresso de séries e episódios.


Requisitos Arquiteturais e Técnicos:
A implementação deve seguir estritamente os princípios da Programação Orientada a Objetos (POO), com foco nos seguintes pilares:


Herança: Modelagem utilizando uma classe base (Midia) herdada por Filme e Serie.


Composição: Estrutura de agregação onde Serie contém Temporada, que contém Episodio.


Encapsulamento e Validação: Uso intensivo de @property para garantir a integridade dos dados, validando atributos como notas (0-10) e duração (>0).



Persistência: Os dados devem ser armazenados de forma simples, utilizando JSON ou SQLite.

O sistema incluirá funcionalidades essenciais como cadastro de mídias , avaliações , listas personalizadas e a geração de relatórios de consumo

UML TEXTUAL:

Classe,Atributos (Privados),Métodos Principais (Públicos),Relacionamentos e Notas
Midia,_titulo: str,__init__(...),"Classe Base. Herança: → Filme, → Serie."
,_tipo: str (FILME/SERIE) ,"@property getters/setters (para validar título não vazio, ano positivo).",Duplicidade: titulo + tipo + ano deve ser único.
,_genero: str ,__eq__(other): bool (Compara por título + tipo).,
,_ano: int ,__str__() / __repr__() (Exibição formatada).,
,_classificacao: str ,,
,_elenco: list[str] ,,
,"_status: str (NÃO ASSISTIDO, ASSISTINDO, ASSISTIDO) ",,
Filme,_duracao: int (minutos) ,__init__(...),Herda de Midia.
,_nota: float (0-10) ,@property duracao (Validação >0).,
,_data_conclusao: datetime,@property nota (Validação 0-10).,
,,avaliar(nota: float).,
,,__lt__(other): bool (Para ordenar por nota média).,
Serie,"_temporadas: dict[int, Temporada]",__init__(...),Herda de Midia.
,,adicionar_temporada(...),Composição: Agrega Temporada.
,,__len__(): int (Total de episódios).,
,,calcular_nota_media_serie() (Média dos episódios).,
,,atualizar_status_automatico() (Muda para 'ASSISTIDA' se todos episódios concluídos).,
Temporada,_numero: int,adicionar_episodio(...),Composição: Contém Episodio.
,"_episodios: dict[int, Episodio]",,
Episodio,_numero: int,@property numero (Validação positiva).,Mídia avaliável (nota 0-10).
,_titulo: str ,@property duracao/nota (Validação >0 e 0-10).,
,_duracao: int ,avaliar(nota: float).,
,_data_lancamento: date ,,
,_status: str ,,
,_nota: float (opcional) ,,
Usuario,_nome: str,__init__(...),Possui listas personalizadas e histórico.
,"_listas: dict[str, ListaPersonalizada]",criar_lista(nome: str).,
,_historico: list[HistoricoItem],adicionar_favorito(...).,
ListaPersonalizada,_nome: str,adicionar_midia(...).,Limite de listas definido em settings.json.
,_midias: list[Midia],remover_midia(...).,
HistoricoItem,_midia: Midia,__init__(...),Usado para registrar data/hora de conclusão.
,_data_conclusao: datetime,,

ESTRUTURA PLANEJADA DE ARQUIVOS:

Arquivo/Pasta,Propósito no Projeto
/projeto_catalogo,Diretório Raiz
├── src/,Contém o código-fonte principal do sistema.
│   ├── modelos.py,"Implementa todas as classes de POO (Midia, Filme, Serie, etc.) e a lógica de negócio (herança, encapsulamento, validações, métodos especiais)."
│   ├── dados.py,"Módulo para persistência (funções salvar/carregar mídias, episódios, usuários e listas em JSON ou SQLite) e a rotina de seed."
│   └── cli.py,"Lógica da Interface de Linha de Comando (CLI) com subcomandos (ex: midia adicionar, serie atualizar-status)."
├── tests/,Armazena os testes unitários (usando pytest) para garantir a integridade das regras e relatórios.
├── settings.json,"Arquivo de configurações do sistema (ex: nota mínima para ""recomendado"", limite de listas personalizadas)."
├── README.md,"Documentação do projeto (UML Textual, instruções de execução)."
└── .gitignore,"Especifica arquivos e pastas a serem ignorados pelo Git (ex: ambientes virtuais, caches, e o arquivo de persistência .db ou .json)."