from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
from matplotlib import cm, colors

fig = plt.figure()
ax = fig.add_subplot(111)

map = Basemap(llcrnrlon=80.,llcrnrlat=12.5,urcrnrlon=140.,urcrnrlat=52.5,resolution='i',projection='laea',lat_0=35.,
        lon_0=110.)

#map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='#ddaa66') #lake_color='aqua'
#map.drawcoastlines()

map.readshapefile('./china_provinces00','cnprovinces', drawbounds = True)

patches = []
for info, shape in zip(map.cnprovinces_info, map.cnprovinces):
    # if info['EPROV'] == 'Shanghai':
    print info
    patches.append( Polygon(np.array(shape), True) )

print count
colors = np.zeros(33,float)
#norm=colors.Normalize(vmin = np.min(colors), vmax = np.max(colors))
print colors


colors[1] = .34
colors[7] = .70
colors[8] = .20
colors[15] = .13
colors[26] = .48
colors[32] = .90

ax.add_collection(PatchCollection(patches, facecolors=cm.RdYlBu(colors), cmap=cm.RdYlBu, edgecolor='k', linewidth=1., zorder=2))

plt.show()
