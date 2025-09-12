import os
import json
from uuid import UUID

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
# -----------------
# FUNÇÕES AUXILIARES
# -----------------

def get_file_path(id_restaurante: UUID) -> str:
    """Retorna o caminho do arquivo JSON de um restaurante pelo UUID"""
    return os.path.join(DATA_DIR, f"{id_restaurante}.json")

def list_dir() -> list[str]:
    """Lista todos os arquivos de cardápio"""
    return [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

def load_json(id_restaurante: UUID) -> dict | None:
    """Carrega o cardápio JSON"""
    path = get_file_path(id_restaurante)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data: dict, id_restaurante: UUID):
    """Salva o cardápio em JSON"""
    with open(get_file_path(id_restaurante), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
