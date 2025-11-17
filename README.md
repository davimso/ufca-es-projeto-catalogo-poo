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

Abaixo está a representação **UML Textual** das classes principais do sistema, incluindo atributos, métodos e relacionamentos.

---

## 🎬 Classe: Midia (Classe Base)

### **Atributos Privados**
- `_titulo: str`
- `_tipo: str` (FILME / SERIE)
- `_genero: str`
- `_ano: int`
- `_classificacao: str`
- `_elenco: list[str]`
- `_status: str` (NÃO ASSISTIDO, ASSISTINDO, ASSISTIDO)

### **Métodos Públicos**
- `__init__(...)`
- `@property` getters/setters  
  - valida título não vazio  
  - valida ano positivo
- `__eq__(other) -> bool` (compara por título + tipo)
- `__str__()` / `__repr__()` (exibição formatada)

### **Notas e Regras**
- Classe Base das classes **Filme** e **Serie**.
- **Duplicidade não permitida:** título + tipo + ano devem ser únicos.

---

## 🎥 Classe: Filme (Herda de Midia)

### **Atributos Privados**
- `_duracao: int` (minutos)
- `_nota: float` (0–10)
- `_data_conclusao: datetime`

### **Métodos Públicos**
- `__init__(...)`
- `@property duracao` (validação > 0)
- `@property nota` (validação 0–10)
- `avaliar(nota: float)`
- `__lt__(other) -> bool` (usado para ordenar por nota média)

---

## 📺 Classe: Serie (Herda de Midia)

### **Atributos Privados**
- `_temporadas: dict[int, Temporada]`

### **Métodos Públicos**
- `__init__(...)`
- `adicionar_temporada(...)`
- `__len__() -> int` (total de episódios)
- `calcular_nota_media_serie()`
- `atualizar_status_automatico()`  
  - Muda para **ASSISTIDA** se todos os episódios estiverem concluídos.

### **Relacionamentos**
- **Composição:** agrega várias `Temporada`.

---

## 📦 Classe: Temporada

### **Atributos Privados**
- `_numero: int`
- `_episodios: dict[int, Episodio]`

### **Métodos Públicos**
- `adicionar_episodio(...)`

### **Relacionamentos**
- **Composição:** contém vários `Episodio`.

---

## 🎞️ Classe: Episodio

### **Atributos Privados**
- `_numero: int`
- `_titulo: str`
- `_duracao: int`
- `_data_lancamento: date`
- `_status: str`
- `_nota: float | None`

### **Métodos Públicos**
- `@property numero` (validação > 0)
- `@property duracao` (validação > 0)
- `@property nota` (validação 0–10)
- `avaliar(nota: float)`

---

## 👤 Classe: Usuario

### **Atributos Privados**
- `_nome: str`
- `_listas: dict[str, ListaPersonalizada]`
- `_historico: list[HistoricoItem]`

### **Métodos Públicos**
- `__init__(...)`
- `criar_lista(nome: str)`
- `adicionar_favorito(...)`

### **Relacionamentos**
- Possui **listas personalizadas**.
- Mantém **histórico** de mídias concluídas.

---

## 🗂️ Classe: ListaPersonalizada

### **Atributos Privados**
- `_nome: str`
- `_midias: list[Midia]`

### **Métodos Públicos**
- `adicionar_midia(...)`
- `remover_midia(...)`

### **Notas**
- O limite máximo de listas vem de `settings.json`.

---

## 🕒 Classe: HistoricoItem

### **Atributos Privados**
- `_midia: Midia`
- `_data_conclusao: datetime`

### **Métodos Públicos**
- `__init__(...)`

### **Função**
- Registro de conclusões no histórico do usuário.

ESTRUTURA PLANEJADA DE ARQUIVOS:

/projeto_catalogo # Diretório Raiz
├── src/ # Código-fonte principal
│ ├── modelos.py # Implementa classes de POO (Midia, Filme, Serie, etc.)
│ │ # + Lógica de negócio: herança, encapsulamento,
│ │ # validações, métodos especiais.
│ ├── dados.py # Módulo de persistência
│ │ # + Funções salvar/carregar mídias, episódios,
│ │ # usuários e listas (JSON ou SQLite).
│ │ # + Rotina de seed.
│ └── cli.py # Interface de Linha de Comando (CLI)
│ # com subcomandos (ex.: midia adicionar,
│ # serie atualizar-status).
│
├── tests/ # Testes unitários (pytest)
│ # Garante integridade das regras e relatórios.
│
├── settings.json # Arquivo de configurações
│ # (nota mínima para "recomendado",
│ # limite de listas personalizadas, etc.)
│
├── README.md # Documentação do projeto
│ # UML Textual + instruções de execução.
│
└── .gitignore # Arquivos ignorados pelo Git
# (ambientes virtuais, caches,
# arquivos .db ou .json de persistência).