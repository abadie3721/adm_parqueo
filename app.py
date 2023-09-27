import os
from flask import Flask
from flask import render_template, request,redirect,session 
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__)
app.secret_key='python'
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='adm_parqueo'
mysql.init_app(app)

@app.route('/')
def inicio():   
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):  
    print(imagen) 
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):  
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)

@app.route('/registros')
def registros(): 

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select * from `registro`")
    registros=cursor.fetchall()
    conexion.commit()

    return render_template('sitio/registros.html', registros = registros)

@app.route('/nosotros')
def nosotros():   
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index(): 
  
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():   
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post(): 
    _usuario=request.form['txtUsuario']  
    _password=request.form['txtPassword'] 
    print(_usuario)
    print(_password)

    if _usuario=="abadie3721" and _password=="1273-esoJ":
        session["login"]=True
        session["usuario"]="Administrador"
        return redirect("/admin")

    return render_template('admin/login.html', mensaje="Acceso denegado")

@app.route('/admin/cerrar')
def admin_login_cerrar(): 
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/registros')
def admin_registros():  
    if not 'login' in session:
     return redirect('/admin/login')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select * from `registro`")
    registros=cursor.fetchall()
    conexion.commit()
    print(registros)

    return render_template('admin/registros.html',registros=registros)


@app.route('/admin/registros/guardar',methods=['POST'])
def admin_registros_guardar(): 

    if not 'login' in session:
     return redirect('/admin/login')


    _marca=request.form['txtMarca']
    _placa=request.form['txtPlaca']
    _entrada=request.form['txtEntrada']
    _salida=request.form['txtSalida'] 
    _archivo=request.files['txtImagen']

    tiempo= datetime.now()
    horaActual= tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre= horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)

    sql = "INSERT INTO `registro` (`id`, `marca`, `placa`, `entrada`, `salida`, `imagen`) VALUES (NULL,%s,%s,%s,%s,%s);"
    datos = (_marca, _placa, _entrada, _salida, nuevoNombre)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_marca)
    print(_placa)
    print(_entrada)
    print(_salida)

    return redirect('/admin/registros')

@app.route('/admin/registros/borrar', methods=['POST'])
def admin_registros_borrar(): 

    if not 'login' in session:
     return redirect('/admin/login')


    _id=request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select imagen from `registro` where id=%s",(_id))
    registros=cursor.fetchall()
    conexion.commit()
    print(registros) 

    if os.path.exists("templates/sitio/img/"+str(registros[0][0])):
        os.unlink("templates/sitio/img/"+str(registros[0][0]))

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Delete from registro where id=%s",(_id))
    conexion.commit()

    return redirect('/admin/registros')


if __name__=='__main__':
    app.run(debug=True)

