import sqlite3
import os

def converter_sql_para_db():
    arquivo_sql = 'Banco de dados - PREPARA CALDAPRO.sql' # <--- ESCREVA O NOME EXATO DO SEU ARQUIVO AQUI
    arquivo_db = 'preparacalda2.db'

    # Remove o banco antigo se ele já existir para não duplicar dados
    if os.path.exists(arquivo_db):
        os.remove(arquivo_db)

    try:
        # Conecta ao arquivo de banco de dados (que será criado agora)
        conn = sqlite3.connect(arquivo_db)
        cursor = conn.cursor()

        # Lê o seu arquivo .sql
        with open(arquivo_sql, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Executa todos os comandos do seu arquivo SQL de uma vez
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Sucesso! O arquivo '{arquivo_db}' foi gerado com sucesso.")
        print("Agora você já pode rodar o seu app.py")

    except Exception as e:
        print(f"❌ Erro ao gerar o banco: {e}")

if __name__ == "__main__":
    converter_sql_para_db()
