
import pymysql

# Configura questi valori in base al tuo database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",               # ← Cambia con il tuo username MySQL
    "password": "Coccok99!!",# ← Cambia con la tua password MySQL
    "database": "discoTeca"   # ← Cambia con il nome del tuo DB
}

def mostra_tabelle():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tabelle = cursor.fetchall()
            print("\nTabelle nel database:")
            for tabella in tabelle:
                print(f" - {tabella[0]}")
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    mostra_tabelle()
