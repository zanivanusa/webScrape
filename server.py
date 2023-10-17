from flask import Flask, render_template
import psycopg2
import os
  
#this way is presumably better  
DATABASE_URL = os.environ.get('DATABASE_URL')
print("Database URL:", os.environ.get('DATABASE_URL'))

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    # Fetch data from the database
    cur = conn.cursor()
    print("DATABASE_UL")
    print("Database URL:", os.environ.get('DATABASE_URL'))
    cur.execute("SELECT * FROM listings")

    print(DATABASE_URL)
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('index.html', estates=data)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
