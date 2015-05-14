from libgoods import curv_grid, data_files_dir
reload(curv_grid)
import numpy as np
import os

f = os.path.join(data_files_dir,'t000.nc')
bbox = [65,-175,75,-145] #Geographic domain [South Lat, West Lon, North Lat, East Lon]
out_dir = data_files_dir #Where to write files (default is libgoods/data_files )



var_map = { 'time':'time',
            'lon': 'lon',
            'lat': 'lat',
            'u': 'uocn',
            'v': 'vocn',
            } 
            
acnfs = curv_grid.cgrid(f)
acnfs.get_dimensions(var_map)

#meshgrid lon/lat for curvilinear grid
acnfs.data['lon'],acnfs.data['lat'] = np.meshgrid(acnfs.data['lon'],acnfs.data['lat'])

#Determine geographic subset indices and get data
acnfs.subset(bbox) #south lat, west lon, north lat, east lon
acnfs.get_data(var_map,yindex=acnfs.y,xindex=acnfs.x,zindex=0,is3d=False,extra_2dvars=['hi','aice','uvel','vvel'])     

#make mask
mask = (acnfs.data['u'] == acnfs.atts['u']['missing_value']).choose(1,0)
acnfs.grid['mask'] = mask

#rename ice vars
rename_dict = {'hi':'ice_thickness','aice':'ice_fraction','uvel':'ice_u','vvel':'ice_v'}
for key, val in rename_dict.iteritems():
    acnfs.data[val] = acnfs.data[key]
    acnfs.atts[val] = acnfs.atts[key]

acnfs.write_nc(os.path.join(out_dir,'acnfs_example.nc'),is3d=False,extra_2dvars=rename_dict.values())
  