from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_SECRETA = os.getenv("CHAVE_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")
TEMPO_EXP = int(os.getenv("TEMP_CHAVE_ACESSO"))