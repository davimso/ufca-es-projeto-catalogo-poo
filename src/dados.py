from src.modelos import Midia, Filme, Serie, Temporada, Episodio, Usuario, HistoricoItem
import sqlite3
from datetime import datetime
from datetime import timedelta

DB_NAME = 'catalogo.db'

def get_conn():
    """Retorna a conexão com o banco de dados SQLite."""
    # A conexão é estabelecida, e o arquivo .db é criado se não existir
    return sqlite3.connect(DB_NAME)

# ----------------------------------------------------
# 1. CRIAÇÃO DE TABELAS (ESQUEMA SQL)
# ----------------------------------------------------

def criar_tabelas():
    """
    Cria todas as tabelas necessárias para persistir a estrutura de POO (Midia, Composicao, Historico).
    """
    conn = get_conn()
    cursor = conn.cursor()

    # Tabela 1: MIDIAS (Base para Filmes e Séries)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS midias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL, 
            genero TEXT,
            ano INTEGER,
            classificacao TEXT,
            duracao INTEGER,
            status TEXT
        )
    """)
    
    # Tabela 2: TEMPORADAS (Relacionamento 1:N com Midias (Serie))
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temporadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serie_id INTEGER,
            numero INTEGER NOT NULL,
            UNIQUE(serie_id, numero), 
            FOREIGN KEY(serie_id) REFERENCES midias(id)
        )
    """)
    
    # Tabela 3: EPISODIOS (Relacionamento 1:N com Temporadas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temporada_id INTEGER,
            numero INTEGER NOT NULL,
            titulo TEXT,
            duracao INTEGER,
            nota REAL, 
            status TEXT,
            UNIQUE(temporada_id, numero),
            FOREIGN KEY(temporada_id) REFERENCES temporadas(id)
        )
    """)
    
    # Tabela 4: HISTORICO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            midia_id INTEGER,
            data_conclusao TEXT,
            FOREIGN KEY(midia_id) REFERENCES midias(id)
        )
    """)
    
    # Tabela 5: LISTAS_PERSONALIZADAS
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listas_conteudo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_lista TEXT NOT NULL,
            midia_id INTEGER,
            FOREIGN KEY(midia_id) REFERENCES midias(id)
        )
    """)

    conn.commit()
    conn.close()

# Garante que as tabelas existem ao iniciar o módulo
criar_tabelas()

# ----------------------------------------------------
# 2. ROTINA DE SEED (DADOS DE TESTE)
# ----------------------------------------------------

def rotina_seed():
    """
    Popula o banco de dados com filmes e séries pré-cadastradas para testes.
    IMPORTANTE: Rodar APENAS UMA VEZ.
    """
    conn = get_conn()
    cursor = conn.cursor()
    
    print("Iniciando rotina de seed...")
    
    try:
        # --- A. FILME DE TESTE (CONCLUÍDO) ---
        cursor.execute("""
            INSERT INTO midias (titulo, tipo, genero, ano, duracao, status)
            VALUES (?, 'FILME', ?, ?, ?, ?)
        """, ('Parasita', 'Drama/Suspense', 2019, 132, 'ASSISTIDO'))
        filme_parasita_id = cursor.lastrowid 

        # Adiciona o filme ao Histórico (Essencial para o Relatório de Tempo)
        hoje = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO historico (midia_id, data_conclusao) VALUES (?, ?)", 
                       (filme_parasita_id, hoje))

        # --- B. SÉRIE DE TESTE (EM ANDAMENTO) ---
        cursor.execute("""
            INSERT INTO midias (titulo, tipo, genero, ano, duracao, status)
            VALUES (?, 'SERIE', ?, ?, ?, ?)
        """, ('Stranger Things', 'Sci-Fi', 2016, 0, 'ASSISTINDO'))
        serie_st_id = cursor.lastrowid

        # Temporada 1 da Série
        cursor.execute("INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                       (serie_st_id, 1))
        temp1_st_id = cursor.lastrowid

        # Episódio 1 (ASSISTIDO e AVALIADO)
        cursor.execute("""
            INSERT INTO episodios (temporada_id, numero, titulo, duracao, nota, status)
            VALUES (?, 1, 'O Desaparecimento de Will Byers', 49, 9.2, 'ASSISTIDO')
        """, (temp1_st_id,))
        
        # Episódio 2 (NÃO ASSISTIDO)
        cursor.execute("""
            INSERT INTO episodios (temporada_id, numero, titulo, duracao, nota, status)
            VALUES (?, 2, 'A Estranha da Rua Maple', 50, NULL, 'NÃO ASSISTIDO')
        """, (temp1_st_id,))
        
        conn.commit()
        print("Seed concluída com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro no SQLite durante o seed (pode ser duplicidade se rodou 2x): {e}")
        conn.rollback()
    
    finally:
        conn.close()

# Descomente e execute esta linha UMA VEZ para popular o banco de dados para testes
# rotina_seed()

# ----------------------------------------------------
# 3. CARREGAR/SALVAR DADOS E RELATÓRIOS
# ----------------------------------------------------

# Necessário que as classes de modelos.py estejam importadas no topo.

def carregar_catalogo():
    """
    Carrega todos os dados do SQLite e reconstrói a hierarquia de objetos de POO.
    """
    conn = get_conn()
    cursor = conn.cursor()

    # Dicionários para armazenar e facilitar a reconstrução
    episodios_por_temp = {}
    temporadas_por_serie = {}
    
    midias_catalogo = {} # Dicionário final de todas as Midias (Filmes e Séries)
    historico_items = []
    
    # ----------------------------------------------------
    # 1. CARREGAR EPISÓDIOS
    # ----------------------------------------------------
    cursor.execute("SELECT id, temporada_id, numero, titulo, duracao, nota, status FROM episodios")
    for row in cursor.fetchall():
        ep_id, temp_id, numero, titulo, duracao, nota, status = row
        
        # Cria a instância do objeto Episodio
        # Nota: É crucial que o __init__ do Episodio seja capaz de receber os dados brutos.
        episodio = Episodio(numero, titulo, duracao, None, nota, status)
        
        # Agrupa os episódios pelo ID da temporada
        if temp_id not in episodios_por_temp:
            episodios_por_temp[temp_id] = []
        episodios_por_temp[temp_id].append(episodio)

    # ----------------------------------------------------
    # 2. CARREGAR TEMPORADAS
    # ----------------------------------------------------
    cursor.execute("SELECT id, serie_id, numero FROM temporadas")
    for row in cursor.fetchall():
        temp_id, serie_id, numero = row
        
        # Cria a instância do objeto Temporada
        temporada = Temporada(numero) 
        
        # Adiciona os episódios reconstruídos à temporada
        if temp_id in episodios_por_temp:
            for episodio in episodios_por_temp[temp_id]:
                temporada.adicionar_episodio(episodio) # Usa o método de Composição
                
        # Agrupa as temporadas pelo ID da série
        if serie_id not in temporadas_por_serie:
            temporadas_por_serie[serie_id] = []
        temporadas_por_serie[serie_id].append(temporada)
        
    # ----------------------------------------------------
    # 3. CARREGAR MÍDIAS (Filmes e Séries)
    # ----------------------------------------------------
    cursor.execute("SELECT id, titulo, tipo, genero, ano, classificacao, duracao, status FROM midias")
    for row in cursor.fetchall():
        midia_id, titulo, tipo, genero, ano, classificacao, duracao, status = row
        
        # Reconstrução de Séries
        if tipo == 'SERIE':
            serie = Serie(titulo, genero, ano, classificacao, [])
            serie.status = status
            
            # Adiciona as temporadas reconstruídas à série
            if midia_id in temporadas_por_serie:
                for temporada in temporadas_por_serie[midia_id]:
                    serie.adicionar_temporada(temporada) # Usa o método de Composição
            
            midias_catalogo[midia_id] = serie
            
        # Reconstrução de Filmes
        elif tipo == 'FILME':
            # Nota: O construtor do Filme precisa do parâmetro 'status' que você já definiu.
            filme = Filme(titulo, genero, ano, classificacao, [], duracao, status, None) # nota é None
            midias_catalogo[midia_id] = filme
            
    # ----------------------------------------------------
    # 4. CARREGAR HISTÓRICO
    # ----------------------------------------------------
    cursor.execute("SELECT midia_id, data_conclusao FROM historico")
    for midia_id, data_conclusao_str in cursor.fetchall():
        # Converte a string de volta para objeto datetime
        data_conclusao = datetime.strptime(data_conclusao_str, '%Y-%m-%d %H:%M:%S')
        
        # Associa o item de histórico ao objeto Midia reconstruído
        if midia_id in midias_catalogo:
            midia_obj = midias_catalogo[midia_id]
            
            # Cria a instância do HistoricoItem
            historico_item = HistoricoItem(midia_obj, data_conclusao)
            historico_items.append(historico_item)
            
    conn.close()
    
    # Retornar o catálogo reconstruído e o histórico para a aplicação principal
    return midias_catalogo, historico_items

# NOTA: O carregamento de Usuário e Listas Personalizadas seria feito em paralelo,
# mas esta função já cobre a complexidade da estrutura de Mídias/Composição.

# src/dados.py

# ... (restante das funções e imports) ...

def gerar_relatorio_tempo_assistido(historico: list, periodo: str = 'mes'):
    """
    Calcula o tempo total assistido (em minutos e horas) no período especificado.
    O período pode ser 'semana' ou 'mes' (ou datas específicas, se o CLI filtrar).
    
    Args:
        historico (list): Lista de objetos HistoricoItem.
        periodo (str): String indicando o período ('mes' ou 'semana').
        
    Returns:
        tuple: (total_minutos, total_horas_arredondado)
    """
    total_minutos = 0
    hoje = datetime.now()
    
    # Define o ponto de corte para o filtro de tempo
    if periodo.lower() == 'semana':
        data_corte = hoje - timedelta(weeks=1)
    elif periodo.lower() == 'mes':
        data_corte = hoje - timedelta(days=30)
    else:
        raise ValueError("Período inválido. Use 'semana' ou 'mes'.")

    # 1. Itera sobre os itens do histórico
    for item in historico:
        
        # 2. Verifica se a conclusão ocorreu dentro do período
        if item._data_conclusao >= data_corte:
            
            # 3. Soma a duração concluída (que já calcula Filmes e Séries)
            # Nota: O HistoricoItem.duracao_concluida deve ser acessado.
            total_minutos += item.duracao_concluida

    # 4. Conversão para Horas (Requisito: Conversão de tempo total em horas )
    # O multiplicador de duração pode vir do settings.json (multiplicador para min -> horas [cite: 40])
    
    # Para fins da Entrega 3, assumimos o multiplicador padrão (60 minutos por hora)
    multiplicador_horas = 60 
    total_horas = total_minutos / multiplicador_horas
    
    # O arredondamento é configurável (Requisito: arredondamento configurável )
    total_horas_arredondadas = round(total_horas, 2) 

    return total_minutos, total_horas_arredondadas

def salvar_midia(midia_obj):
    """
    Persiste (INSERT ou UPDATE) um objeto Midia (Filme/Serie) e seus detalhes
    no banco de dados SQLite.
    """
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        # 1. BUSCA O ID: Garante que o objeto seja vinculado ao registro correto no banco
        cursor.execute("SELECT id FROM midias WHERE titulo = ? AND ano = ?", 
                       (midia_obj.titulo, midia_obj.ano))
        midia_id_result = cursor.fetchone()
        
        if midia_id_result:
            # --- RAMO DE UPDATE (Mídia Existente) ---
            midia_id = midia_id_result[0]
            
            # ATUALIZAÇÃO CRUCIAL: Salva o status consolidado da série (ex: 'ASSISTINDO')
            cursor.execute("""
                UPDATE midias 
                SET status = ?, genero = ?, classificacao = ?, duracao = ?
                WHERE id = ?
            """, (midia_obj.status, midia_obj._genero, midia_obj._classificacao, 
                  midia_obj._duracao, midia_id))
            
            # Atualiza ou Insere novos elementos da composição (Temporadas/Episódios)
            if midia_obj._tipo == 'SERIE':
                _atualizar_composicao_serie(cursor, midia_obj, midia_id)
                
            print(f"✅ Banco: '{midia_obj.titulo}' atualizado com sucesso.")

        else:
            # --- RAMO DE INSERT (Nova Mídia) ---
            cursor.execute("""
                INSERT INTO midias (titulo, tipo, genero, ano, classificacao, duracao, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (midia_obj.titulo, midia_obj._tipo, midia_obj._genero, midia_obj.ano, 
                  midia_obj._classificacao, midia_obj._duracao, midia_obj.status))
            
            midia_id = cursor.lastrowid

            if midia_obj._tipo == 'SERIE':
                _inserir_composicao_serie(cursor, midia_obj, midia_id)
                
            print(f"🚀 Banco: '{midia_obj.titulo}' inserido com sucesso.")
            
        conn.commit() # Confirma a transação no arquivo .db
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao salvar dados no SQLite: {e}")
        conn.rollback() # Reverte em caso de erro para evitar dados corrompidos
        
    finally:
        conn.close()

def _inserir_composicao_serie(cursor, serie_obj, serie_id):
    """Função auxiliar para inserir Temporadas e Episódios de uma nova Série."""
    for temporada in serie_obj._temporadas.values():
        # INSERT Temporada
        cursor.execute("INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                       (serie_id, temporada.numero))
        temp_id = cursor.lastrowid
        
        # INSERT Episódios
        for episodio in temporada._episodios.values():
            cursor.execute("""
                INSERT INTO episodios (temporada_id, numero, titulo, duracao, nota, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (temp_id, episodio.numero, episodio._titulo, episodio.duracao, episodio.nota, episodio.status))

def _atualizar_composicao_serie(cursor, serie_obj, serie_id):
    """
    Função auxiliar que lida com a atualização de episódios existentes 
    E a inserção de temporadas novas em séries já cadastradas.
    """
    for temporada in serie_obj._temporadas.values():
        # Verifica se esta temporada específica já existe no banco
        cursor.execute("SELECT id FROM temporadas WHERE serie_id = ? AND numero = ?",
                       (serie_id, temporada.numero))
        temp_id_result = cursor.fetchone()
        
        if temp_id_result:
            # TEMPORADA EXISTE: Apenas atualiza status/notas dos episódios
            temp_id = temp_id_result[0]
            for episodio in temporada._episodios.values():
                cursor.execute("""
                    UPDATE episodios SET status = ?, nota = ?
                    WHERE temporada_id = ? AND numero = ?
                """, (episodio.status, episodio.nota, temp_id, episodio.numero))
        else:
            # TEMPORADA NOVA: Insere a temporada e todos os seus episódios
            cursor.execute("INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                           (serie_id, temporada.numero))
            nova_temp_id = cursor.lastrowid
            
            for episodio in temporada._episodios.values():
                cursor.execute("""
                    INSERT INTO episodios (temporada_id, numero, titulo, duracao, nota, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nova_temp_id, episodio.numero, episodio._titulo, 
                      episodio.duracao, episodio.nota, episodio.status))
                
def salvar_listas_usuario(usuario_obj):
    """Percorre as listas personalizadas do usuário e salva no SQLite."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # Limpa as listas antigas para evitar duplicatas ao salvar novamente
        cursor.execute("DELETE FROM listas_conteudo")
        
        for nome_lista, lista_obj in usuario_obj.listas.items():
            for midia in lista_obj._midias:
                # Busca o ID da mídia para salvar a referência
                cursor.execute("SELECT id FROM midias WHERE titulo = ?", (midia.titulo,))
                res = cursor.fetchone()
                if res:
                    midia_id = res[0]
                    cursor.execute("""
                        INSERT INTO listas_conteudo (nome_lista, midia_id) 
                        VALUES (?, ?)
                    """, (nome_lista, midia_id))

        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao salvar listas: {e}")
    finally:
        conn.close()

def salvar_historico_usuario(usuario_obj):
    """
    Percorre a lista de objetos HistoricoItem do usuário 
    e persiste no banco de dados.
    """
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        # Limpamos o histórico antigo para evitar duplicatas (ou use uma lógica de UPSERT)
        cursor.execute("DELETE FROM historico")
        
        for item in usuario_obj._historico:
            # Precisamos do ID da mídia no banco para criar a relação
            cursor.execute("SELECT id FROM midias WHERE titulo = ?", (item.midia.titulo,))
            res = cursor.fetchone()
            
            if res:
                midia_id = res[0]
                # item.data_conclusao é um objeto datetime, o SQLite aceita como string
                cursor.execute("""
                    INSERT INTO historico (midia_id, data_conclusao)
                    VALUES (?, ?)
                """, (midia_id, item.data_conclusao.strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Erro ao salvar histórico: {e}")
    finally:
        conn.close()

def carregar_listas_personalizadas(usuario_obj, midias_catalogo):
    """Lê a tabela listas_conteudo e preenche o objeto Usuario."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT nome_lista, midia_id FROM listas_conteudo")
    
    for nome_lista, midia_id in cursor.fetchall():
        if nome_lista not in usuario_obj.listas:
            usuario_obj.criar_lista(nome_lista)
        
        if midia_id in midias_catalogo:
            midia_obj = midias_catalogo[midia_id]
            usuario_obj.listas[nome_lista].adicionar_midia(midia_obj)
    conn.close()
    
def excluir_midia_do_banco(titulo, ano):
    """
    Remove a mídia e todas as suas dependências (temporadas/episódios/histórico) do SQLite.
    """
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # 1. Busca o ID da mídia para localizar as dependências
        cursor.execute("SELECT id FROM midias WHERE titulo = ? AND ano = ?", (titulo, ano))
        res = cursor.fetchone()
        
        if res:
            midia_id = res[0]
            
            # 2. Deletar episódios vinculados às temporadas desta série
            cursor.execute("""
                DELETE FROM episodios WHERE temporada_id IN 
                (SELECT id FROM temporadas WHERE serie_id = ?)
            """, (midia_id,))
            
            # 3. Deletar temporadas
            cursor.execute("DELETE FROM temporadas WHERE serie_id = ?", (midia_id,))
            
            # 4. Deletar registros no histórico
            cursor.execute("DELETE FROM historico WHERE midia_id = ?", (midia_id,))
            
            # 5. Deletar a mídia principal
            cursor.execute("DELETE FROM midias WHERE id = ?", (midia_id,))
            
            conn.commit()
            return True
        return False
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir no banco de dados: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()