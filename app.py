from flask import Flask, request, redirect, url_for, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON to CSV Converter</title>
                                  
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #1a1a1a;
                margin: 0;
                color: #fff;
            }
            .container {
                text-align: center;
                padding: 20px;
                background: #333;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
                border-radius: 8px;
            }
            h1 {
                margin-bottom: 20px;
                color: #fff;
            }
            input[type="file"] {
                margin-bottom: 20px;
                padding: 10px;
                background: #444;
                border: none;
                color: #fff;
                border-radius: 4px;
                cursor: pointer;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>JSON to CSV Converter</h1>
            <p>Create By Tenz-M4</p>
            
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".json">
                <button type="submit">Convert</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(json_path)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename.rsplit('.', 1)[0] + '.csv')
        
        try:
            data = pd.read_json(json_path)
            data.to_csv(csv_path, index=False)
            return send_file(csv_path, as_attachment=True)
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)



    
