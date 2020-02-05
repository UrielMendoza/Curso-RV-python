import matplotlib
matplotlib.use('Agg')
import geopandas as gpd
from shapely import ops
from glob import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def reproyecta(archivo,epsg):  
  agua = gpd.read_file(archivo)
  rios = gpd.read_file('hidro4mgw_c/hidro4mcw.shp')
  muni = gpd.read_file('muni_2018gw_c/muni_2018cw.shp')
  
  agua = agua.to_crs({'init':'epsg:'+epsg})
  rios = rios.to_crs({'init':'epsg:'+epsg})
  muni = muni.to_crs({'init':'epsg:'+epsg})
  
  return agua,rios,muni

def noMonitoreo(buff,agua,rios):

  aguab = agua.buffer(buff)
  aguab = ops.unary_union(aguab)

  dif = rios.difference(aguab)

  return dif

def mapa(anio,cuadrante,agua,rios,muni,dif,nombre):
  plt.figure(figsize=(20,20))
  ax = plt.axes(projection=ccrs.Mercator())
  ax.coastlines(resolution='50m')
  ax.set_extent(cuadrante, crs=ccrs.PlateCarree())
  agua.plot(ax=ax, marker= '+', markersize=50,zorder=2,column='dbo_clas',legend=True)
  rios.plot(ax=ax, linestyle='--',markersize=0.5,zorder=1,color='b',legend=True)
  muni.plot(ax=ax,alpha=0.1,color='white',edgecolor='black',zorder=0)
  dif.plot(ax=ax,color = 'red')
  plt.title(anio)
  plt.savefig('static/'+nombre+str(cuadrante[0])+'.png',bbox_inches='tight', pad_inches=0)

  return nombre+str(cuadrante[0])+'.png'

def integra(ruta,cuandrante,anioU):
  archivos = glob(ruta)
  archivos.sort()

  for i in archivos: 

    nombre = i.split('/')[-1].split('.')[0]
    anio = i.split('/')[-1].split('.')[0][-4:]

    if anio == anioU:

      print('Procesando:',nombre,anio)

      print('Reproyecta:')
      agua,rios,muni = reproyecta(i,'3857')

      print('No Monitore:')
      dif = noMonitoreo(10000,agua,rios)
      
      print('Mapeo:')
      image = mapa(anio,cuandrante,agua,rios,muni,dif,nombre)

  print('Finalizado')
  return image
#ruta = '/content/drive/My Drive/Curso-RV-python/datos/*/*.shp'
#cuandrante = [-101,-98,18,19.5]
#anio = '2006'

#integra(ruta,cuandrante,anio)
