from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = '118.139.182.3'  # MySQL host (e.g., localhost)
app.config['MYSQL_USER'] = 'sqluser1'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'TGDp0U&[1Y4S'  # MySQL password
app.config['MYSQL_DB'] = 'stocks'  # MySQL database name

mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data')
def get_stock_data():
    # Fetch data from MySQL for a specific table (e.g., adanient_eq)
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, open, high, low, close FROM adanient_eq ORDER BY date ASC")  # Replace with your table name
    data = cur.fetchall()
    cur.close()

    # Prepare data for frontend
    stock_data = []
    for row in data:
        stock_data.append({
            'date': row[0].strftime("%Y-%m-%d %H:%M:%S"),  # Format date as string
            'open': float(row[1]),
            'high': float(row[2]),
            'low': float(row[3]),
            'close': float(row[4])
        })

    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)