# src/config.py

import json
import os

SETTINGS_FILE = 'settings.json'

def load_settings():
    """
    Carrega as configurações do arquivo JSON que está na raiz do projeto.
    """
    # 1. Obter o diretório do arquivo ATUAL (src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Navegar para o diretório PAI (raiz do projeto)
    root_dir = os.path.dirname(current_dir)
    
    # 3. Construir o caminho completo para settings.json
    settings_path = os.path.join(root_dir, SETTINGS_FILE)
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de configuração '{SETTINGS_FILE}' não encontrado em {root_dir}. Usando padrões.")
        # Retorna valores padrão em caso de erro para não quebrar o programa
        return {
            "NOTA_MINIMA_RECOMENDADO": 8.0,
            "LIMITE_LISTAS_PERSONALIZADAS": 5,
            "MULTIPLICADOR_MIN_PARA_HORAS": 60
        }

SETTINGS = load_settings()