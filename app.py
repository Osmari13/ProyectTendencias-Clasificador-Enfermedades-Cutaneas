from __future__ import division, print_function
from flask import Flask, render_template, request, redirect, Response, url_for, session
from werkzeug.utils import secure_filename

import os
import numpy as np
import cv2
import conexion
import tensorflow as tf

from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input

tf.config.set_soft_device_placement(True)

width_shape=224
height_shape = 224

names = ['ACNE', 'MELANOMA MALIGNO', 'NEVUS', 'PIE DE ATLETA',
         'PSORIASIS', 'ROSACEA', 'URTICARIA', 'VARICELA', 'VERRUGA', 'VITILIGO']

app = Flask(__name__)


model_path = './models/model_VGG16.h5' #El directorio .h5 tiene almacenado el modelo para realizar la prediccion 

model = load_model(model_path)

print('Modelo cargado')

#funcion que realiza la preccion
def model_predict(img_path, model):
    img = cv2.resize(cv2.imread(img_path), (width_shape,
                     height_shape), interpolation=cv2.INTER_AREA)
    x = np.asarray(img)
    x = preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds
#pagina de registro
@app.route('/')
def landing():
    return render_template('landingPage/index.html')  
@app.route('/about')
def about():
    return render_template('landingPage/about.html')  
@app.route('/admin')
def admin():
    return render_template('admin.html')  
@app.route('/login')
def home():
    return render_template('index.html')   
 
 
# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        #cur = mysql.connection.cursor()
        conex = conexion.obtener_conexion()
        cur = conex.cursor()
       
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
        cur.close()
        conex.close()
        if account: 
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol']=account['id_rol']
            session['user']=account['user']
            if session['id_rol']==1:
                return render_template("admin.html")
            elif session ['id_rol']==2:
               return redirect("/layout")# return render_template("layout.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro(): 
    nombre=request.form['txtNombre']
    apellido=request.form['txtApellido']
    usuario=request.form['txtUsuario']
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    
    conex = conexion.obtener_conexion()

    with conex.cursor() as cur:
        cur.execute(" INSERT INTO usuarios (nombre, apellido, user, correo, password, id_rol) VALUES (%s,%s,%s,%s, %s, '2')",(nombre, apellido, usuario, correo,password))
    conex.commit()
    conex.close()
    #cur = conex.cursor()
    
    return render_template("index.html",mensaje2="Usuario Registrado Exitosamente")

#pagina principal
@app.route("/layout", methods=['GET'])
def layout():
    username = session.get('user')
    return render_template("layout.html",  username=username )

#funcion que responde al pedido del usario para mostrar la prediccion
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['file']
        user_id = session['id']
        basepath = os.path.dirname(__file__) #la ruta donde se encuentra el archivo actual
        file_name = secure_filename(f.filename) # generar un nombre de archivo seguro

        
        file_path = os.path.join(
            basepath, 'uploads', file_name) #para guardar archivo
        f.save(file_path)

        #inserta los campos en la base de datos
        conex = conexion.obtener_conexion()
        with conex.cursor() as cur:
            cur.execute(" INSERT INTO enfermedades_user (id_usuario, imagen_url) VALUES (%s, %s)",(user_id,file_name))
        conex.commit()
        conex.close()

        #Hace las prediccion
        preds = model_predict(file_path, model)

        print('PREDICCIÓN', names[np.argmax(preds)])

        result = str(names[np.argmax(preds)])
        return result
    return  None


if __name__ == '__main__':
    app.secret_key = "llavesecreta"
    app.run(debug=True, host='localhost', port=5000, threaded=True)
