from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np
from matplotlib import cm, colors
import sys
from netCDF4 import Dataset
import itertools

# Read in the shapefile

fig = plt.figure()
ax = fig.add_subplot(111)

map = Basemap(llcrnrlon=-180.,llcrnrlat=-90.,urcrnrlon=180.,urcrnrlat=90,resolution='i',projection='cyl',lat_0=0.,lon_0=0.)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='#ddaa66', lake_color='aqua') #lake_color='aqua'
#map.drawcoastlines()

map.readshapefile('./world_regions_2008/world_regions_2008','world_regions', drawbounds = True)

plt.show()

sys.exit()

paths = []
rgnm = []
rgid = []

for info, shape in zip(map.world_regions_info, map.world_regions):
    paths.append( Path(shape) )
    rgid.append( info['ObjectID'] + 1 )
    rgnm.append( info['REGION'] )


# Read in coordinates
ncfile = '../bcim/1990_embcm_month_4albedo.nc'

fh = Dataset(ncfile, 'r')

lats = fh.variables['lat'][:]
lons = fh.variables['lon'][:]

fh.close()

nlat = len(lats)
nlon = len(lons)

world_region_map = [[0 for x in range(nlon)] for x in range(nlat)]

for path, ilat, ilon in itertools.product(paths,range(nlat),range(nlon)):

    index = paths.index(path)
    pronm = rgnm[index]

    if ( ilat == 0 and ilon == 0 ):
        print index
        print pronm
        print rgid[index]
 
    lat = lats[ilat]
    lon = lons[ilon]
    if ( lon > 180 ):
        lon = lon - 360

    if path.contains_point((lon,lat)):  #shapefile writes in (lon,lat)
       world_region_map[ilat][ilon] = rgid[index]

### Write data to ncfile
ncfile = Dataset('world_regions_2008_'+str(nlat)+'x'+str(nlon)+'.nc','w',format='NETCDF4')

ncfile.createDimension('lat',nlat)
ncfile.createDimension('lon',nlon)

lat_dim = ncfile.createVariable('lat',np.float32,('lat',))
lon_dim = ncfile.createVariable('lon',np.float32,('lon',))

lat_dim.units = 'degrees_N'
lon_dim.units = 'degrees_E'

mask = ncfile.createVariable('mask',np.int32,('lat','lon'))

#Create description for the ncfile
description = ''
id = 0
for pronm in rgnm:
    if ( id != rgid[rgnm.index(pronm)] ):
        id += 1
        description += pronm + ': ' + str(id) + ',  '

mask.description = description

print description

lat_dim[:] = lats
lon_dim[:] = lons

mask[:] = world_region_map

ncfile.close()
