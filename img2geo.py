import sys
import numpy as np
import pyproj
import geopy
import gdal
import osr
from math import sqrt,atan,pi
from PIL import Image


### Exemple
python img2geo.py 20200101143500_12_binary.png -22.68918 -45.00655 15000 15000
gdal_translate -of netCDF -co "FORMAT=NC4" 20200101143500_12_binary.tif output.nc



def read_img(img):
	img = Image.open(img)
	return np.array(img)

def calc_bbox(center_lat,center_lon,width,height):
	#Get WKT Polygon
	geod = pyproj.Geod(ellps='WGS84')

	# width = 15000. # m
	# height = 15000. # m
	rect_diag = sqrt( width**2 + height**2 )

	# center_lon = -45.00655
	# center_lat = -22.68918

	azimuth1 = atan(width/height)
	azimuth2 = atan(-width/height)
	azimuth3 = atan(width/height)+pi # first point + 180 degrees
	azimuth4 = atan(-width/height)+pi # second point + 180 degrees

	pt1_lon, pt1_lat, _ = geod.fwd(center_lon, center_lat, azimuth1*180/pi, rect_diag)
	pt2_lon, pt2_lat, _ = geod.fwd(center_lon, center_lat, azimuth2*180/pi, rect_diag)
	pt3_lon, pt3_lat, _ = geod.fwd(center_lon, center_lat, azimuth3*180/pi, rect_diag)
	pt4_lon, pt4_lat, _ = geod.fwd(center_lon, center_lat, azimuth4*180/pi, rect_diag)

	wkt_poly = [[pt1_lon, pt1_lat], [pt2_lon, pt2_lat], [pt3_lon, pt3_lat], [pt4_lon, pt4_lat]]

	## Coordinates
	top_right = np.asarray(wkt_poly[0])
	top_left = np.asarray(wkt_poly[1])
	bot_left = np.asarray(wkt_poly[2])
	bot_right = np.asarray(wkt_poly[3])

	return [bot_left.min(),bot_left.max(),top_right.min(),top_right.max()]

def create_tiff(data,bbox):
    BBOX = bbox

    xres = abs(BBOX[0]-BBOX[2]) / data.shape[1]
    yres = abs(BBOX[1]-BBOX[3]) / data.shape[0]

    geotransform = (BBOX[0], xres, 0, BBOX[3], 0, -yres)
    
    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(img_dir[:-4]+'.tif', 
                                                  data.shape[1], data.shape[0], 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(4326)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(data)   # write a-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    print('Image Converted!!!')


img_dir = str(sys.argv[1])
print(img_dir[:-4])
lat_ = float(sys.argv[2])
lon_ = float(sys.argv[3])
width_ = int(sys.argv[4])
height_ = int(sys.argv[5])

rimg = read_img(img_dir)
bbox_ = calc_bbox(lat_,lon_,width_,height_)
create_tiff(rimg,bbox_)
