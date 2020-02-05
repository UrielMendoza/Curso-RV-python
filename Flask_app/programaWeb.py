from flask import Flask,request,render_template,url_for
from programa import integra

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def menu():
    mapa = 'latest.png'
    #lon = -99
    #lat = 19
    if request.method == 'POST':

        lon = float(request.form['lon'])
        lat = float(request.form['lat'])
        anio = request.form['anio']

        ruta = 'datos/*/*.shp'
        
        print(type(lon))
        print(type(lat))

        cuandrante = [lon-1,lon+1,lat-1,lat+1]

        path = 'static/'

        mapa = integra(ruta,cuandrante,anio)

    return render_template('index.html',image = mapa)

if __name__ == "__main__":
    app.run(host = '132.247.103.186',port=8080)
