
import sys
import os
from datetime import datetime

#IMPORTAÇÃO DOS MÓDULOS DO PROJETO
from src.modelos import Filme, Serie, Usuario,Temporada,Episodio, HistoricoItem, ListaPersonalizada #Importa todas as classes necessárias
from src.dados import carregar_catalogo, salvar_midia, gerar_relatorio_tempo_assistido
from src.config import SETTINGS #Importa as configurações do settings.json

#VARIÁVEIS GLOBAIS DE ESTADO
CATALOGO_GLOBAL = {} 
HISTORICO_GLOBAL = []
USUARIO_ATUAL = None 

#FUNÇÕES DE CONTROLE

def inicializar_sistema():
    """Carrega dados persistidos do SQLite e inicializa o usuário."""
    global CATALOGO_GLOBAL, HISTORICO_GLOBAL, USUARIO_ATUAL
    
    print("Iniciando sistema...")
    
    #Carregar Catálogo e Histórico
    # CATALOGO_GLOBAL aqui recebe o dicionário com IDs como chaves {id: objeto}
    CATALOGO_GLOBAL, HISTORICO_GLOBAL = carregar_catalogo()
    
    #Inicializar Usuário
    limite = SETTINGS['LIMITE_LISTAS_PERSONALIZADAS']
    USUARIO_ATUAL = Usuario(nome="Davi", limite_listas=limite)
    
    #Anexar Histórico carregado
    USUARIO_ATUAL._historico.extend(HISTORICO_GLOBAL)

    from src.dados import carregar_listas_personalizadas
    carregar_listas_personalizadas(USUARIO_ATUAL, CATALOGO_GLOBAL)
    

    CATALOGO_GLOBAL = {midia.titulo: midia for midia in CATALOGO_GLOBAL.values()}
    
    print(f"Sistema inicializado. {len(CATALOGO_GLOBAL)} mídias e listas carregadas.")

def salvar_e_encerrar():
    """Salva todo o estado do sistema no SQLite antes de sair."""
    print("\n💾 Salvando dados no banco de dados...")
    
    try:
        #Salva cada mídia (Filmes/Séries)
        for midia in CATALOGO_GLOBAL.values():
            salvar_midia(midia)
            
        #Salva as Listas Personalizadas
        from src.dados import salvar_listas_usuario
        salvar_listas_usuario(USUARIO_ATUAL)
        
        #Salva o Histórico de visualização
        from src.dados import salvar_historico_usuario
        salvar_historico_usuario(USUARIO_ATUAL)
        
        print("✅ Tudo foi salvo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

    print("Encerrando o sistema. Até logo!")
    sys.exit(0)

#MENUS E INTERAÇÃO

def menu_exibir_detalhes_serie():
    """
    Exibe informações detalhadas de uma série específica, 
    incluindo temporadas e o status de cada episódio.
    """
    midia_obj = selecionar_midia_por_titulo()
    
    if not midia_obj:
        return

    if not isinstance(midia_obj, Serie):
        print(f"⚠️ '{midia_obj.titulo}' é um Filme. Use a exibição geral para filmes.")
        return

    print("\n" + "="*50)
    print(f"📺 DETALHES DA SÉRIE: {midia_obj.titulo.upper()}")
    print(f"📂 Gênero: {midia_obj._genero} | 📅 Ano: {midia_obj.ano}")
    print(f"📊 Status Geral: {midia_obj.status}")
    print(f"🔢 Total de Temporadas: {len(midia_obj._temporadas)}")
    print("="*50)

    if not midia_obj._temporadas:
        print("ℹ️ Nenhuma temporada cadastrada para esta série.")
    else:
        # Ordena as temporadas por número para exibição correta
        for num_temp in sorted(midia_obj._temporadas.keys()):
            temporada = midia_obj._temporadas[num_temp]
            print(f"\n🔹 Temporada {num_temp}")
            print("-" * 20)
            
            if not temporada._episodios:
                print("  (Sem episódios cadastrados)")
            else:
                # Ordena os episódios por número
                for num_ep in sorted(temporada._episodios.keys()):
                    ep = temporada._episodios[num_ep]
                    status_icon = "✅" if ep.status == "ASSISTIDO" else "⏳"
                    nota_str = f" | Nota: {ep.nota}" if ep.nota is not None else ""
                    
                    print(f"  {status_icon} Ep {num_ep}: {ep._titulo} ({ep.duracao} min){nota_str}")
    
    print("\n" + "="*50)
    input("Pressione Enter para voltar...")

def exibir_menu_principal():
    """Exibe as opções principais para o usuário."""
    print("\n" + "🎬"*2 + "="*36 + "🎬"*2)
    print(f"CATÁLOGO DE MÍDIAS | Usuário: {USUARIO_ATUAL._nome}")
    print("="*40)
    print("1. Exibir Catálogo Completo")
    print("2. Adicionar Nova Mídia (Filme/Série)")
    print("3. Gerenciar Status/Avaliação")        
    print("4. Gerar Relatórios")
    print("5. Gerenciar Listas Personalizadas")
    print("6. Menu de Séries detalhadas")  
    print("7. Remover Mídia do Catálogo") 
    print("0. Sair e Salvar")
    print("=" * 40)

def main_loop():
    """Loop principal de execução do CLI."""
    inicializar_sistema()
    
    while True:
        exibir_menu_principal()
        escolha = input("Selecione uma opção: ").strip()
        
        if escolha == '1':
            exibir_catalogo_completo()
        elif escolha == '2':
            menu_adicionar_midia() 
        elif escolha == '3':
            menu_gerenciar_status()
        elif escolha == '4':
            menu_relatorios()
        elif escolha == '5':
            menu_listas_personalizadas()
        elif escolha == '6':
            menu_exibir_detalhes_serie()
        elif escolha == '7':
            menu_remover_midia_do_catalogo()
        elif escolha == '0':
            salvar_e_encerrar()
        else:
            print("❌ Opção inválida. Tente novamente.")

#FUNÇÕES DE VISUALIZAÇÃO/RELATÓRIOS

def exibir_catalogo_completo():
    """Exibe todas as mídias carregadas na memória, formatadas pelo __str__."""
    if not CATALOGO_GLOBAL:
        print("O catálogo está vazio.")
        return
        
    print("\n--- Catálogo de Mídias ---")
    
    #Acessar os valores (objetos Midia) do dicionário CATALOGO_GLOBAL
    midias_ordenadas = sorted(CATALOGO_GLOBAL.values(), key=lambda x: x.titulo)
    
    for i, midia in enumerate(midias_ordenadas, 1):
        #Utiliza o __str__ de Midia/Filme/Serie
        print(f"  {i}. {midia}") 
    print("--------------------------")

def menu_relatorios():
    """Gera o Relatório de Tempo Assistido ."""
    print("\n--- Relatórios ---")
    print("1. Tempo Total Assistido (Últimos 30 dias)")
    print("0. Voltar")
    
    escolha = input("Selecione o relatório: ").strip()
    
    if escolha == '1':
        try:
            #Chama a função de dados, que usa a constante do settings.json (via config.py)
            minutos, horas = gerar_relatorio_tempo_assistido(USUARIO_ATUAL._historico, 'mes')
            print(f"\n✅ Relatório de Tempo Assistido (Últimos 30 dias):")
            print(f"   Total assistido: **{horas:.2f} horas** ({minutos} minutos)")
        except ValueError as e:
            print(f"Erro ao gerar relatório: {e}")
    elif escolha == '0':
        return
    else:
        print("❌ Opção inválida.")

#FUNÇÕES DE GESTÃO

def menu_gerenciar_status():
    """
    Interface para atualizar o progresso de visualização e avaliações.
    Diferencia a lógica entre Filmes (simples) e Séries (hierárquica).
    """
    exibir_catalogo_completo()
    
    midia_obj = selecionar_midia_por_titulo() #Usa a função auxiliar já criada
    
    if not midia_obj:

        return
        
    try:
        #Logica para filmes
        if isinstance(midia_obj, Filme):
            print(f"\n🎬 Gerenciando Filme: {midia_obj.titulo}")
            novo_status = input(f"Novo status (Atual: {midia_obj.status}) [ASSISTIDO/ASSISTINDO/NÃO ASSISTIDO]: ").strip().upper()
            midia_obj.status = novo_status 
            
            if midia_obj.status == "ASSISTIDO":
                nota_input = input("Nota (0 a 10) ou Enter para pular: ").strip()
                if nota_input:
                    midia_obj.nota = float(nota_input)
                
                #Registra no histórico para o relatório de tempo
                USUARIO_ATUAL.adicionar_ao_historico(midia_obj, datetime.now())
                print("✅ Filme marcado como assistido e adicionado ao histórico.")

        #Logica para series
        elif isinstance(midia_obj, Serie):
            while True:
                print(f"\n📺 Gerenciando Série: {midia_obj.titulo}")
                print(f"Status Atual: {midia_obj.status}")
                print("1. Adicionar Nova Temporada")
                print("2. Gerenciar Episódio Específico (Status/Nota)")
                print("3. Marcar Série Inteira como Assistida")
                print("0. Voltar")
                
                sub_opcao = input("Escolha uma ação: ").strip()

                if sub_opcao == '1':
                    num_temp = int(input("Número da nova temporada: "))
                    nova_temp = Temporada(num_temp)
                    
                    qtd_eps = int(input(f"Quantos episódios tem a Temporada {num_temp}? "))
                    for i in range(1, qtd_eps + 1):
                        nome_ep = input(f"Nome do Episódio {i}: ").strip()
                        duracao_ep = int(input(f"Duração do Ep {i} (min): "))
                        episodio = Episodio(i, nome_ep, duracao_ep, None) 
                        nova_temp.adicionar_episodio(episodio)
                    
                    midia_obj.adicionar_temporada(nova_temp)
                    midia_obj.atualizar_status_automatico()
                    salvar_midia(midia_obj)

                    print(f"✅ Temporada {num_temp} adicionada!")
                    print(f"Status da série atualizado para: {midia_obj.status}")

                elif sub_opcao == '2':
                    if not midia_obj._temporadas:
                        print("❌ Esta série não possui temporadas cadastradas.")
                        continue
                        
                    temp_num = int(input("Número da Temporada: "))
                    if temp_num in midia_obj._temporadas:
                        temp_obj = midia_obj._temporadas[temp_num]
                        ep_num = int(input("Número do Episódio: "))
                        
                        if ep_num in temp_obj._episodios:
                            ep_obj = temp_obj._episodios[ep_num]
                            ep_obj.status = "ASSISTIDO"
                            
                            nota = input("Nota do Episódio (0-10) ou Enter para pular: ").strip()
                            if nota:
                                ep_obj.nota = float(nota)
                            
                            #REGRA DE NEGÓCIO: A série atualiza seu status baseada nos episódios
                            midia_obj.atualizar_status_automatico()
                            salvar_midia(midia_obj)
                            print(f"✅ Episódio {ep_num} da Temporada {temp_num} atualizado!")
                        else:
                            print("❌ Episódio não encontrado.")
                    else:
                        print("❌ Temporada não encontrada.")

                elif sub_opcao == '3':
                    #Atalho para marcar tudo como concluído
                    midia_obj.status = "ASSISTIDO"
                    USUARIO_ATUAL.adicionar_ao_historico(midia_obj, datetime.now())
                    salvar_midia(midia_obj)
                    print("✅ Série marcada como assistida.")

                elif sub_opcao == '0':
                    break
                else:
                    print("❌ Opção inválida.")

        
        #Salva qualquer alteração (seja Filme ou Série/Episódios) no SQLite
        salvar_midia(midia_obj)
        print(f"💾 Alterações em '{midia_obj.titulo}' salvas no banco de dados.")

    except ValueError as e:
        print(f"❌ Erro de validação: {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

def selecionar_midia_por_titulo():
    """
    Busca uma mídia no catálogo global (CATALOGO_GLOBAL) pelo título, 
    permitindo que o usuário a adicione ou remova de uma lista.
    """
    midia_input = input("Digite o TÍTULO da mídia: ").strip()
    
    # Itera sobre os objetos Midia no dicionário global
    for midia in CATALOGO_GLOBAL.values():
        if midia.titulo.lower() == midia_input.lower():
            return midia
    
    print("❌ Mídia não encontrada no catálogo. Verifique o título.")
    return None

def menu_listas_personalizadas():
    """
    Menu para criar, exibir e gerenciar a adição de mídias em listas personalizadas.
    Aplica a Regra de Negócio de limite de listas do objeto Usuario.
    """
    while True:
        print("\n--- 📝 Gerenciamento de Listas Personalizadas ---")
        print("1. Criar Nova Lista")
        print("2. Exibir Listas Existentes (e seu conteúdo)")
        print("3. Adicionar Mídia a uma Lista")
        print("4. Remover Mídia de uma Lista")
        print("0. Voltar ao Menu Principal")
        
        escolha = input("Selecione uma opção: ").strip()

        if escolha == '1':
            # --- CRIAR NOVA LISTA (Usa a Regra de Negócio) ---
            nome = input("Nome da nova lista: ").strip()
            try:
                USUARIO_ATUAL.criar_lista(nome) 
                print(f"✅ Lista '{nome}' criada com sucesso.")
            except (ValueError, TypeError) as e:
                print(f"❌ Não foi possível criar a lista: {e}")
        
        elif escolha == '2':
            if not USUARIO_ATUAL.listas:
                print("Nenhuma lista personalizada encontrada.")
                continue
                
            print("\nListas do Usuário:")
            for nome, lista in USUARIO_ATUAL.listas.items():
                print(f"\n--- Lista: {nome} ({len(lista)} mídias) ---")
                
                if not lista._midias:
                    print("  (Vazia)")
                    continue
                    
                #Exibe o conteúdo de cada lista
                for i, midia in enumerate(lista._midias, 1):
                    #Utiliza o __str__ de Midia/Filme/Serie
                    print(f"  {i}. {midia}") 

        elif escolha == '3':
            
            if not USUARIO_ATUAL.listas:
                print("❌ Crie uma lista antes de adicionar mídias.")
                continue

            lista_nome = input("Digite o NOME da lista para adicionar: ").strip().upper()
            
            #Verifica se a lista existe no objeto Usuario
            if lista_nome not in USUARIO_ATUAL.listas:
                print(f"❌ Lista '{lista_nome}' não encontrada.")
                continue

            #Seleciona a mídia e verifica se existe no catálogo global
            midia_obj = selecionar_midia_por_titulo()
            if midia_obj:
                try:
                    #Chama o método da classe ListaPersonalizada para adicionar
                    USUARIO_ATUAL.listas[lista_nome].adicionar_midia(midia_obj)
                    print(f"✅ '{midia_obj.titulo}' adicionada à lista '{lista_nome}'.")
                except ValueError as e:
                    print(f"❌ Erro ao adicionar: {e}") #Captura erro de duplicidade

        elif escolha == '4':
            menu_remover_midia_da_lista()
        
        elif escolha == '0':
            return
            
        else:
            print("❌ Opção inválida. Tente novamente.")

def menu_adicionar_midia():
    """
    Guia o usuário para criar um novo objeto Filme ou Série e persistí-lo.
    """
    print("\n--- Adicionar Nova Mídia ---")
    tipo = input("Tipo de Mídia (FILME ou SERIE): ").strip().upper()

    if tipo not in ["FILME", "SERIE"]:
        print("❌ Tipo de mídia inválido. Escolha FILME ou SERIE.")
        return

    try:
        titulo = input("Título: ").strip()
        
        #Verifica se a mídia já existe para evitar duplicatas
        if titulo in CATALOGO_GLOBAL:
            print(f"❌ A mídia '{titulo}' já existe no catálogo.")
            return
            
        genero = input("Gênero: ").strip()
        ano = int(input("Ano de Lançamento: "))
        classificacao = input("Classificação Indicativa (ex: 12, L): ").strip()
        
        nova_midia = None

        if tipo == "FILME":
            duracao = int(input("Duração (minutos): "))
            
            # Cria a instância do Filme
            nova_midia = Filme(
                titulo, genero, ano, classificacao, elenco=[], 
                duracao_minutos=duracao, status="NÃO ASSISTIDO", nota=None
            )
            
        elif tipo == "SERIE":
            #Cria o objeto Série
            nova_midia = Serie(titulo, genero, ano, classificacao, elenco=[])
            print("--- Adicionar Primeira Temporada ---")
            
            #Captura os dados da primeira Temporada
            num_temporada = int(input("Número da 1ª Temporada: "))
            
            #Cria a instância da Temporada
            nova_temporada = Temporada(num_temporada)
            
            #Adiciona pelo menos um Episódio
            num_episodios = int(input(f"Quantos episódios tem a Temporada {num_temporada}? "))
            for i in range(1, num_episodios + 1):
                nome_episodio = input(f"Nome do Episódio {i}: ").strip()
                duracao_episodio = int(input(f"Duração do Episódio {i} (minutos): "))
                
                #Cria e adiciona o Episódio
                episodio = Episodio(i, nome_episodio, duracao_episodio)
                nova_temporada.adicionar_episodio(episodio)
                
            #Adiciona a Temporada à Série
            nova_midia.adicionar_temporada(nova_temporada)
            
        #Persistência e Atualização do Estado Global
        if nova_midia:
            #Persistência: salvar_midia deve fazer um INSERT
            salvar_midia(nova_midia) 
            
            #Atualiza a memória
            CATALOGO_GLOBAL[nova_midia.titulo] = nova_midia 
            
            print(f"✅ Mídia '{nova_midia.titulo}' adicionada com sucesso ao catálogo.")

    except ValueError:
        print("❌ Erro de entrada: Garanta que Ano, Duração e Número de Episódios sejam números inteiros válidos.")
    except Exception as e:
        print(f"❌ Ocorreu um erro desconhecido: {e}")

def menu_remover_midia_da_lista():
    """
    Remove uma mídia de uma lista personalizada específica do usuário.
    """
    if not USUARIO_ATUAL.listas:
        print("❌ Você não possui listas criadas.")
        return

    print("\nSuas listas:", ", ".join(USUARIO_ATUAL.listas.keys()))
    lista_nome = input("De qual lista deseja remover? ").strip().upper()

    if lista_nome in USUARIO_ATUAL.listas:
        lista_obj = USUARIO_ATUAL.listas[lista_nome]
        
        #Exibe o que tem na lista para ajudar o usuário
        if not lista_obj._midias:
            print(f"⚠️ A lista '{lista_nome}' já está vazia.")
            return

        print(f"\nConteúdo de {lista_nome}:")
        for i, m in enumerate(lista_obj._midias, 1):
            print(f"  {i}. {m.titulo}")

        titulo_remover = input("\nDigite o TÍTULO exato da mídia para remover: ").strip()
        
        try:
            #Chama o método da classe ListaPersonalizada
            lista_obj.remover_midia(titulo_remover)
            print(f"✅ '{titulo_remover}' removido da lista '{lista_nome}'.")
        except ValueError as e:
            print(f"❌ Erro: {e}")
    else:
        print("❌ Lista não encontrada.")

from src.dados import excluir_midia_do_banco

def menu_remover_midia_do_catalogo():
    """
    Interface para remover uma mídia do sistema permanentemente.
    """
    print("\n--- 🗑️ Remover Mídia do Catálogo ---")
    exibir_catalogo_completo()
    
    midia_obj = selecionar_midia_por_titulo() # Reutiliza sua função de busca
    
    if midia_obj:
        confirmar = input(f"⚠️ Tem certeza que deseja excluir '{midia_obj.titulo}'? (S/N): ").strip().upper()
        
        if confirmar == 'S':
            #Remove do Banco de Dados
            sucesso = excluir_midia_do_banco(midia_obj.titulo, midia_obj.ano)
            
            if sucesso:
                #Remove da Memória (Dicionário Global
                if midia_obj.titulo in CATALOGO_GLOBAL:
                    del CATALOGO_GLOBAL[midia_obj.titulo]
                
                print(f"✅ '{midia_obj.titulo}' foi removida com sucesso de todos os registros.")
            else:
                print("❌ Erro ao processar a exclusão no banco de dados.")
        else:
            print("Operação cancelada.")

if __name__ == "__main__":
    main_loop()