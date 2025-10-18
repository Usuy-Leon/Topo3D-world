<div align="center">
<div style="background-color: #1a1b1e; padding: 20px; border-radius: 8px; margin-bottom: 20px;">

# Mundo-Topo3D

</div>
<div align="left">
 
Obtén datos topográficos de cualquier parte del mundo y transfórmalos en un archivo STL 3D listo para imprimir. Mejora la resolución más allá del archivo Geotiff original.

La Agencia Nacional de Inteligencia Geoespacial (NGA) y la NASA crearon el mapa topográfico de la Tierra más completo y de alta resolución, que es muy útil para muchos propósitos científicos y prácticos. La Misión de Topografía de Radar Transbordador (SRTM) recopiló datos detallados de elevación para casi toda la Tierra. Utilizó un sistema de radar especial volando en el Transbordador Espacial Endeavour. Los datos de este proyecto son de código abierto y gratuitos.

</div>
<div align="center">
 
<img width="2549" height="1499" alt="Captura de pantalla del 2025-07-25 15-05-38" src="https://github.com/user-attachments/assets/33391e51-d3ba-4ac2-a8c7-47787a2e39a9" />

Convierte archivos de Modelo Digital de Elevación (DEM) en modelos de montañas imprimibles en 3D con escalado adecuado y dimensionamiento automático.

![salida](https://github.com/user-attachments/assets/1f0f4a4a-ba7b-4223-95a6-be187c9740d0)

</div>
<div align="left">
<hr>
 
# Cómo descargar un GeoTIFF de OpenTopography
 
  1. Ve al sitio web: Visita el enlace específico de OpenTopography para los datos de la Misión de Topografía de Radar Transbordador.

</div>
<div align="center">

https://portal.opentopography.org/raster?opentopoID=OTSRTM.082016.4326.1

<img width="1600" height="800" alt="imagen" src="https://github.com/user-attachments/assets/b91c2ebe-1121-4f75-aa67-418287d594e6" />

</div>
<div align="left">
 
  2. Elige tu área: Usa el mapa o las herramientas en el sitio para seleccionar el área exacta de la que quieres los datos de elevación.
  3. Selecciona el formato de datos: Asegúrate de elegir el formato GeoTIFF si hay una opción, ya que este es un tipo de archivo estándar para datos de elevación y raster (no agregues características de visualización adicionales).

# Usa el Script
El script realiza cuatro modificaciones principales:
(1) Cambia todas las unidades a metros
(2) Escala la altura para visualización
(3) Mejora la resolución (solo para visualización, no datos reales)
(4) Transforma GeoTiff a STL
(5) Agrega una base y paredes para hacerlo compatible con impresión 3D

## Instala los paquetes de Python requeridos

```python
pip install numpy rasterio numpy-stl
```

## 2. Ruta al archivo
Modifica estas rutas en el script
python

```python
raw_geotiff = "ruta/tusarchivos/terreno.tif"
output_stl = "ruta/tusarchivos/modelo.stl"
```
## 3. Ejecuta el script
```python

python geotiff_to_stl.py

```
Por favor colabora para hacerlo más fácil para nuevos usuarios

¡Disfruta!
Siéntete libre de agregar o cambiar este repositorio!
</div>
