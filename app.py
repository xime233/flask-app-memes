from flask import Flask, request, send_file, render_template
import pandas as pd
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/archivo-oc')
def archivo_oc():
    return render_template('archivo-oc.html')
@app.route('/calculadora')
def calculadora():
    return render_template('calculadora.html')

@app.route('/memes')
def memes():
    return render_template('memes.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    archivo = request.files.get('archivo')
    if not archivo:
        return "❌ No se subió ningún archivo."

    # Guardar archivo subido
    nombre_seguro = secure_filename(archivo.filename)
    ruta_entrada = os.path.join(UPLOAD_FOLDER, nombre_seguro)
    archivo.save(ruta_entrada)

    try:
        df = pd.read_excel(ruta_entrada, engine='pyxlsb', sheet_name='Consulta')
    except Exception as e:
        return f"❌ Error al leer el archivo: {e}"

    def extraer_oc(texto):
        match = re.search(r'OC\d{8}', str(texto))
        return match.group(0) if match else None

    df["COLUMNA OC"] = df["GLOSA"].apply(extraer_oc)

    ruta_salida = os.path.join(UPLOAD_FOLDER, 'resultado_con_OC.xlsx')
    df.to_excel(ruta_salida, index=False)

    return send_file(ruta_salida, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
