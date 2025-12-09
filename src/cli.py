
import sys
import os
from datetime import datetime

#IMPORTAÇÃO DOS MÓDULOS DO PROJETO
from src.modelos import Filme, Serie, Usuario, HistoricoItem, ListaPersonalizada #Importa todas as classes necessárias
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
    CATALOGO_GLOBAL, HISTORICO_GLOBAL = carregar_catalogo()
    
    #Inicializar Usuário (Injetando o Limite de Listas do settings.json)
    limite = SETTINGS['LIMITE_LISTAS_PERSONALIZADAS']
    USUARIO_ATUAL = Usuario(nome="Davi", limite_listas=limite)
    
    # Anexar Histórico carregado (para que o relatório use o histórico do objeto Usuario)
    USUARIO_ATUAL._historico.extend(HISTORICO_GLOBAL)
    
    print(f"Sistema inicializado. {len(CATALOGO_GLOBAL)} mídias carregadas.")


def salvar_e_encerrar():
    """Encerra o programa após salvar o estado do banco."""
    print("\nEncerrando o sistema...")
    #Aqui, a função salvar_midia() deve ser chamada para CADA objeto modificado.
    print("Dados salvos (se houver modificações).")
    sys.exit(0)

#MENUS E INTERAÇÃO

def exibir_menu_principal():
    """Exibe as opções principais para o usuário."""
    print("\n" + "🎬"*2 + "="*36 + "🎬"*2)
    print(f"CATÁLOGO DE MÍDIAS | Usuário: {USUARIO_ATUAL._nome}")
    print("="*40)
    print("1. Exibir Catálogo Completo")
    print("2. Gerenciar Status/Avaliação")
    print("3. Gerar Relatórios")
    print("4. Gerenciar Listas Personalizadas")
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
            menu_gerenciar_status()
        elif escolha == '3':
            menu_relatorios()
        elif escolha == '4':
            menu_listas_personalizadas()
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
    """Gera o Relatório de Tempo Assistido (Semana 3)."""
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
    """Permite ao usuário atualizar o status e avaliar uma mídia."""
    exibir_catalogo_completo()
    
    midia_input = input("Digite o TÍTULO da mídia para gerenciar: ").strip()
    midia_obj = None
    
    #Busca a mídia pelo título
    for midia in CATALOGO_GLOBAL.values():
        if midia.titulo.lower() == midia_input.lower():
            midia_obj = midia
            break
    
    if not midia_obj:
        print("❌ Mídia não encontrada.")
        return
        
    try:
        #1. Atualizar Status
        novo_status = input(f"Novo status (Atual: {midia_obj.status}) [ASSISTIDO/ASSISTINDO/NÃO ASSISTIDO]: ").strip()
        midia_obj.status = novo_status # Usa o setter com validação
        
        #2. Avaliar (Se for Filme)
        if isinstance(midia_obj, Filme) and midia_obj.status == "ASSISTIDO":
            nota_input = input("Deseja avaliar o filme (0 a 10)? (Deixe em branco para pular): ").strip()
            if nota_input:
                midia_obj.nota = float(nota_input)
                
        #3. Adicionar ao Histórico e Salvar
        if midia_obj.status == "ASSISTIDO":
            # Adiciona ao Histórico (e registra a data atual)
            USUARIO_ATUAL.adicionar_ao_historico(midia_obj, datetime.now())
            print("✅ Mídia adicionada ao Histórico de visualização.")
            
        #4. Persistência
        salvar_midia(midia_obj)
        print(f"Status/Nota de '{midia_obj.titulo}' atualizados com sucesso.")
            
    except ValueError as e:
        print(f"❌ Erro de validação: {e}")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

def menu_listas_personalizadas():
    """Menu para criar e gerenciar listas."""
    print("\n--- Listas Personalizadas ---")
    print("1. Criar Nova Lista")
    print("2. Exibir Listas Existentes")
    print("0. Voltar")
    
    escolha = input("Selecione uma opção: ").strip()
    
    if escolha == '1':
        nome = input("Nome da nova lista: ").strip()
        try:
            USUARIO_ATUAL.criar_lista(nome) # Usa a Regra de Negócio de Limite
        except (ValueError, TypeError) as e:
            print(f"❌ Não foi possível criar a lista: {e}")
    
    elif escolha == '2':
        if not USUARIO_ATUAL.listas:
            print("Nenhuma lista personalizada encontrada.")
            return
        print("\nListas do Usuário:")
        for nome, lista in USUARIO_ATUAL.listas.items():
            print(f"- {nome} ({len(lista)} mídias)")


if __name__ == "__main__":
    main_loop()