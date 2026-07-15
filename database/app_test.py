from flask import Flask 
import psycopg2

app = Flask(__name__)
@app.route("/") 
def home(): 
    try: 
        conn = psycopg2.connect( host="ksi_opinion_base", port=5432, database="ksi_opinion_base", user="ksi_opinion_base", password="ksi_opinion_base" ) 
        
        cur = conn.cursor() 
        # cur.execute("SELECT version();") 
        cur.execute("SELECT * FROM subjects") 

        version = cur.fetchone()[1] 
        cur.close() 
        conn.close() 
        return f""" 
        <h1>Połączono z PostgreSQL!</h1>
        <p>{version}</p>   
        """ 
    
    except Exception as e:
            return f"Błąd połączenia: {e}" 
    
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=5000)

