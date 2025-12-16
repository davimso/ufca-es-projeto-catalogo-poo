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

# 🎬 Sistema de Gerenciamento de Catálogo de Mídias

Aplicação de **linha de comando (CLI)** desenvolvida em **Python** para gestão personalizada de **filmes e séries**.  
O sistema permite rastrear progresso de consumo, aplicar **avaliações granulares**, gerar **relatórios de uso** e persistir dados em **SQLite**, utilizando fortemente **Programação Orientada a Objetos (POO)**.

---

## 🚀 Como Executar

### Pré-requisitos
- Python **3.10+**

### Execução
```bash
cd projeto_catalogo
python -m src.cli

projeto_catalogo/
├── src/
│   ├── modelos.py   # Classes de domínio (POO, herança, composição, validações)
│   ├── dados.py     # Camada de persistência (SQLite, CRUD, reconstrução de objetos)
│   ├── cli.py       # Interface de Linha de Comando (menus e interação)
│   └── config.py    # Leitura e centralização de configurações (settings.json)
├── settings.json    # Configurações externas do sistema
└── catalogo.db      # Banco de dados SQLite (gerado automaticamente)
## 🛠️ Funcionalidades Implementadas (Entrega Final)

### 1️⃣ Gestão Completa de Catálogo (CRUD)

#### Cadastro
- Inclusão de **Filmes**
- Inclusão de **Séries**, com suporte a múltiplas **temporadas** e **episódios**

#### Leitura
- Exibição formatada do catálogo
- Ordenação por título

#### Atualização
- Alteração de **status**: `NÃO ASSISTIDO`, `ASSISTINDO`, `ASSISTIDO`
- Atribuição de **notas**

#### Remoção
- Exclusão física de mídias
- Remoção em cascata manual de temporadas e episódios no banco

---

### 2️⃣ Regras de Negócio e POO

#### Atualização Automática de Status (Séries)
- Uma série é marcada como `ASSISTIDO` **somente** quando **todos os episódios** de **todas as temporadas** forem concluídos
- Ao adicionar novos episódios, o status retrocede automaticamente para `ASSISTINDO`

#### Listas Personalizadas
- Criação de listas como **Favoritos**, **Para Ver Depois**, etc.
- Respeita o **limite máximo configurável** em `settings.json`

#### Composição Granular
- Episódios possuem **status** e **nota próprios**, independentes da série

---

### 3️⃣ Relatórios e Configurações

#### Relatório de Tempo Assistido
- Cálculo do tempo total de consumo nos **últimos 30 dias**

#### Configurações Dinâmicas (JSON)
- Multiplicador de conversão de **minutos → horas**
- Limites de listas personalizadas
- Ajustes sem necessidade de alterar o código-fonte

---

## 📊 Modelagem de Dados (Diagrama de Classes)

O sistema utiliza **herança** e **composição profunda**:

- **Midia** (classe base)
  - **Filme**
  - **Serie**
    - **Temporada**
      - **Episodio**

Essa abordagem garante:
- Alto nível de reutilização de código
- Regras de negócio encapsuladas
- Fácil manutenção e extensibilidade

---

## 👤 Autor

**Davi**  
Desenvolvedor Principal

---

## 📌 Tecnologias Utilizadas

- Python 3.10+
- SQLite
- Programação Orientada a Objetos (POO)
- CLI (Interface de Linha de Comando)
