import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
from shapely.ops import nearest_points
from shapely.geometry import Point, MultiPoint, LineString, Polygon
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import contextily as ctx


# Random colors have been assigned
color = ['#008fd5', '#fc4f30', '#fe7f2d', '#ffee32']


def scale_bar(ax, length='None', location=(0.5, 0.05), linewidth=5,):
    """ This function will brink back a scale_bar

        Args:
            ax is the axes to draw the scale_bar .
            length is the length of the scale_bar in km.
            location is center of the scale_bar in axis coordinates.
            (0.5 controls the East West position of the plot and 0.05 controls North South of the plot)
            linewidth is the thickness of the scale_bar.

    """
    #Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    #Make tmc horizontally centred on the middle of the map,
    #vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    #Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    #Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]
    #Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 700, sbx + length * 700]
    #Plot the scale_bar
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='black', linewidth=linewidth)
    #Plot the scale_bar label
    ax.text(sbx, sby, str(length) + ' km', transform=tmc,
            horizontalalignment='center', verticalalignment='bottom', fontsize=12, )


def capitalize_name(name):
    """ This function will capitalize the initial letter of the values

        Args:
            name is the name of the column
            return the name from attribute table column with method
            title in order to capitalize the first letter of the value
    """
    # The return will bring back from the attribute table the column 'name'
    return name.title()


def upper_name(name):
    """ This function will upper case the values

         Args:
            name is the name of the column
            return the name from attribute table column with method
            upper in order to upper case the value

    """
    # The return will bring back from the attribute table the column 'name'
    return name.upper()


def lower_name(name):
    """ This function will lower case the values

        Args:
            name is the name of the column
            return the name from attribute table column with method
            title in order to lower the elements
    """
    # The return will bring back from the attribute table the column 'name'
    return name.lower()


def generate_legend(labels, color, alpha=1):
    """ This function will generate colored patches on the legend label

        Args:
            label will add the labels
            color will add the colors
            alpha controls the transparency
            handles [] is a condition of an empty list
            zip will define iterable arguments from two or more iterables
            patches will generate face color and edge color patches
            handles will generate an appropriate entry
            return will return handles

    """
    handles = []
    for c, l in zip(color, labels):
        patches = mpatches.Patch(label=l, color=c)
        handles.append(patches)
    return handles


def unique_name(name):
    """ This function will find the unique names on the list

    Args:
        name is the column of the values
        return the unique values of the 'name' column in attribute table

    """
    unique = []
    for i in name:
        if name in unique:
            continue
        else:
            unique.append(name)
    return unique


def province_chania():
    """ This function will find the unique name of the provinces layer and will return
          the percentage of each state

    Methods:
        overlay will return the new overlap shapes
        iterrows will iterate the index of each row in panda series
        return will return the percentage of each state

    """
    chania = gpd.overlay(provinces[provinces['name'] == 'Chania'], states,
                             how='intersection')  # intersects the provinces 'Chania' with states
    for i, row in chania.iterrows():
        chania.loc[i, 'Pc'] = row['area_km2_2'] / row['area_km2_1'] * 100
    return chania


def province_rethymno():
    """ This function will find the unique name of the provinces layer and will return
          the percentage of each state

    Methods:
        overlay will return the new overlap shapes
        iterrows will iterate the index of each row in panda series
        return will return the percentage of each state

      """
    rethymno = gpd.overlay(provinces[provinces['name'] == 'Rethymno'], states,
                             how='intersection')  # intersects the provinces 'Rethymno' with states
    for i, row in rethymno.iterrows():
        rethymno.loc[i, 'Pc'] = row['area_km2_2'] / row['area_km2_1'] * 100
    return rethymno


def province_iraklion():
    """ This function will find the unique name of the provinces layer and will return
              the percentage of each state

        Methods:
            overlay will return the new overlap shapes
            iterrows will iterate the index of each row in panda series
            return will return the percentage of each state

      """
    iralkion = gpd.overlay(provinces[provinces['name'] == 'Iraklion'], states,
                             how='intersection')  # intersects the provinces 'Iralkion' with states
    for i, row in iralkion.iterrows():
        iralkion.loc[i, 'Pc'] = row['area_km2_2'] / row['area_km2_1'] * 100
    return iralkion


def province_lasithi():
    """ This function will find the unique name of the provinces layer and will return
          the percentage of each state

    Methods:
        overlay will return the new overlap shapes
        iterrows will iterate the index of each row in panda series
        return will return the percentage of each state

      """
    lasithi = gpd.overlay(provinces[provinces['name'] == 'Lasithi'], states,
                             how='intersection')  # intersects the provinces 'Lasithi' with states
    for i, row in lasithi.iterrows():
        lasithi.loc[i, 'Pc'] = row['area_km2_2'] / row['area_km2_1'] * 100
    return lasithi


def nearest_values(row, other_gdf, point_column='geometry', value_column="geometry"):
    """This function will find the nearest point and will return the value.

        Args:
            row will check each row
            other_gdf refers to other shapefiles points, polygons
            point_column will return the geometry
            values_column will return the referred value 'name', 'geometry'
            return will return the nearest value
    """
    # Create an union of the other GeoDataFrame's geometries:
    other_points = other_gdf["geometry"].unary_union
    # Find the nearest points
    nearest_geoms = nearest_points(row[point_column], other_points)
    # Get corresponding values from the other GeoDataFrames
    nearest_data = other_gdf.loc[other_gdf["geometry"] == nearest_geoms[1]]
    # Get the values of the column
    nearest_value = nearest_data[value_column].values[0]
    return nearest_value


# Reading the Vector shapefiles with Geopandas GeoDataFrame.
provinces = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\provinces\provinces.shp')
states = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\states\states.shp')
outline = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\outline\outline.shp')
cities = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\cities\cities.shp')
airports = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\airports\airports.shp')
rivers = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\rivers\rivers.shp')
roads = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\roads\roads.shp')
refuges = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\Final_Assignment_EGM722\data\refuges\refuges.shp')


# Transform each shapefile to correct epsg. For Greece coordinate reference system the CRS is 'epsg=32635'
provinces = provinces.to_crs(epsg=32635)
states = states.to_crs(epsg=32635)
outline = outline.to_crs(epsg=32635)
cities = cities.to_crs(epsg=32635)
airports = airports.to_crs(epsg=32635)
rivers = rivers.to_crs(epsg=32635)
roads = roads.to_crs(epsg=32635)
refuges = refuges.to_crs(epsg=32635)


# Provinces polygons layer
provinces = provinces.drop(columns=['gid', 'parent', 'esye_id', 'name_gr', 'center', 'shape_leng', 'shape_area']) # Drop method will drop off the no needed columns
provinces['area_km2'] = provinces.area / 1000000  # Provinces adding a new column and bring back Square Kilometres
provinces.rename(columns={'name_eng': 'name', 'pop': 'population'}, inplace=True)  # Rename column the columns
provinces = provinces[['name', 'area_km2', 'population', 'geometry']]  # Add the columns in order
provinces['population'] = provinces.population / 1000   # Add the population column
provinces = provinces.replace({'N. IRAKLIOU': 'Iraklion',  # Replace method will replace the rows of 'name' column
                               'N. CHANION': 'Chania',
                               'N. LASITHIOU': 'Lasithi',
                               'N. RETHYMNOU': 'Rethymno',
                               })
provinces_percentage = provinces['name'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
#print(provinces_percentage)
#print(provinces.describe())
#print(provinces.count())
#print(provinces)


# Calculate the the max area, min area and the mean of provinces layer
max_area = provinces['area_km2'].max()
min_area = provinces['area_km2'].min()
mean_area = provinces['area_km2'].mean()
#print(provinces[provinces['area_km2'] > 10])
#print("Max area: {0} km2".format(max_area))
#print("Min area: {0} km2".format(min_area))
#print("Mean area: {0} km2".format(mean_area))
#print("Sum area: {0} km2".format(provinces['area_km2'].sum()))


# Filters applying in order to print the attribute table with all the names of provinces except the 'rethymno' and 'chania'
filt = (provinces['name'] == 'Rethymno') | (provinces['name'] == 'Chania')
provinces_filt = provinces.loc[~ filt, 'name']
#print(provinces_filt)


# States polygons layer
states = states.drop(columns=['KWD_YPES']) # The drop method will remove declared columns from the attribute table
states['area_km2'] = states.area / 1000000 # The area method will append a new column 'area_km2' in meters and divided it by 1000000 will bring back km2
states.rename(columns={'NAME': 'name'}, inplace=True) # Rename method to change the elements designation
states = states[['name', 'area_km2', 'geometry']]
#print(states.describe())
#print(states)
#states.plot(cmap="hsv")
#plt.show()


# Cities points layer,
cities = cities.drop(columns=['fid', 'ONOMA']) # Using the drop method to remove columns as they containing information in Greek language.
cities.rename(columns={'NAME': 'name'},  inplace=True) # Set the capital NAME to lower case
cities = cities.replace({'Hrakleio': 'Iraklion', # Using the replace method to replace the names
                         'Agios Nikolaos': 'Agios nikolaos',
                         'Rethimno': 'Rethymno',
                         'Hania': 'Chania'})
# If the above method do not worked you can uncomment the following to bring the same results,
# Else just leave them under the comment
#cities.loc[0, 'name'] = 'Iraklion'
#cities.loc[1, 'name'] = 'agios nikolaos'
#cities.loc[2, 'name'] = 'rethymno'
#cities.loc[3, 'name'] = 'chania'
#print(cities)


# Airports points shapefile layer
airports = airports.drop(columns='Id') # Drop method to remove columns
airports.rename(columns={'Name': 'name'},  inplace=True) # Rename the columns
airports = airports.replace({'Heraklion Airport': # Replace the values of the rows
                             'Iraklion Airport'})
airports_upper = airports['name'].apply(capitalize_name) # Capitalize function
airports_sum = airports.name.apply(unique_name) # Unique function
filt = airports['name'].str.contains('Sitia', na=False) # Str.contains will return if only the arguments are True
#print(airports.loc[filt, 'name'])
#print(airports_upper)


# The nearest airport per city point layer
unary_union = cities.unary_union
airports["nearest_cities"] = airports.apply(nearest_values, other_gdf=cities, point_column="geometry",
                                                            value_column="name", axis=1)

#print(airports)

# The total airports included per province polygon layer and the nearest city
airports = gpd.GeoDataFrame(airports, geometry=gpd.points_from_xy(airports.geometry.x, airports.geometry.y))
airports.crs = ('epsg:32635')
airports_per_pro = gpd.sjoin(airports, provinces, op='within')
airports_per_pro.rename(columns={'name_left': 'airports_name', 'name_right': 'provinces_name'},  inplace=True)
#print(airports_per_pro)


# Refuges polygons layer and drop method to remove declared columns
refuges = refuges.drop(columns=['fid', 'OBJECTID', 'KODE', 'FEK', 'AREA_',
                                'PREFECTURE', 'DESCRIPTIO', 'CREATED_BY',
                                'CREATED_DA', 'UPDATED_BY', 'UPDATED_BY', 'ID'])
# Rename method to change the elements designation
refuges = refuges.rename(columns={'NAME': 'name',
                                 'PERIMETER': 'perimeter',
                                 'HECTARES': 'hectares',
                                 'UPDATED': 'update',
                                 'SHAPE_AREA': 'shape_area',
                                 'SHAPE_LEN': 'shape_lenght'})
# Adding the area column
refuges['area_km2'] = refuges.area / 1000000
# Join the refuges with function province_chania()
join_refuges = gpd.sjoin(refuges, province_chania())
# Rename the columns
join_refuges.rename(columns={'name': 'refuges_name',
                     'name_1': 'province_chania',
                      'name_2': 'states_name'}, inplace=True)
# Run the loop to return the percentage only for the refuges layer included in province_chania
for i, row in join_refuges.iterrows():
    join_refuges.loc[i, 'refuges_Pc'] = row['area_km2'] / row['area_km2_2'] * 100
#print(join_refuges)
#print(refuges)


# Rivers line layer
rivers = rivers.drop(columns=['fid', 'objectid', 'eu_cd', 'name', 'altname2',
                              'altname3', 'region_cd', 'system', 'ins_when',
                              'ins_by', 'basin_cd', 'status_yr', 'modified',
                              'artificial', 'alt_cat', 'geol_cat', 'size_cat',
                              'ms_cd', 'geology', 'lat', 'lon', 'size_', 'energy',
                              'av_width', 'av_depth', 'av_slope', 'riv_morph', 'discharge',
                              'val_morph', 'solids', 'acid_neut', 'substratum', 'chloride',
                              'a_temp_rge', 'av_a_temp', 'ppt', 'dist_sourc', 'cont'])
# Rename the columns
rivers = rivers.rename(columns={'altname1': 'name', 'shape_Leng': 'shape_length'})
# For rivers looping the table and add the 'length'
for i, row in rivers.iterrows():
    rivers.loc[i, 'length'] = row['geometry'].length / 1000
# Re-order the columns
rivers = rivers[['name', 'length', 'shape_length', 'geometry']]
# Applying the function upper_name
rivers_lower = rivers['name'].apply(upper_name)
#print(rivers)
#print(rivers_lower)


# Roads line layer
# For roads looping the table in order to add the length of the roads in metres as the crs is in metres
for i, row in roads.iterrows():
    roads.loc[i, 'length'] = row['geometry'].length
# Classification of columns and determination of order of each column
roads = roads[['type', 'length', 'geometry']]
# The normalize=True setting the total percentage of each road in the area
# The total values of the column 'type' to observe the different roads type of total roads of each category
roads_percentages = roads['type'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
#print(roads_percentages)

# Checking for total values
roads_type = roads['type'].value_counts()
#print(roads_type)

# Calculate the total length in Kilometres for each category
roads_sum = roads.groupby(['type'])['length'].sum() / 1000
#print(roads_sum)

# Join the province polygon layer with roads multi-linestring
join_pro_roa = gpd.sjoin(provinces, roads, how='inner', op='intersects')
#print(join_pro_roa)

# Groupby process will split and combine the groups of data given
provinces_roads_total = join_pro_roa.groupby(['name', 'type'])['length'].sum() / 1000
#print(provinces_roads_total)


# Checking the roads layer being in same crs with provinces layer
if provinces.crs == roads.crs:
    print('The provinces and the Roads got the same CRS:', provinces.crs, roads.crs)
else:
    print('Not the same CRS')


# Join method and count the total percentage of each states in province
provinces_sum = provinces.groupby(['name', 'population'])['area_km2'].sum() # groupby  will split and group the data
join_pro_sta = gpd.sjoin(states, provinces,  how='left', op='intersects') # join will transfer the attribute table from provinces to states
for i, row in join_pro_sta.iterrows():
    join_pro_sta.loc[i, 'Pc'] = row['area_km2_left'] / row['area_km2_right'] * 100
#print(join_pro_sta) # You will notice double series in the first three rows the name 'agios vasilios' assigned up 3 times. The results occurred by overlapping


# Spatial Geo-processes
# The functions will return the individual states included in the province layer and the percentage of each individual state
# Uncomment below on Buffer the plt.show() to observe the 7 different figures
#(province_chania()).plot(cmap='hsv', edgecolor='black', linewidth=2)
#(province_rethymno()).plot(cmap='hsv', edgecolor='blue', linewidth=2)
#(province_iraklion()).plot(cmap='hsv', edgecolor='green', linewidth=2)
#(province_lasithi()).plot(cmap='hsv', edgecolor='yellow', linewidth=2)
#print(province_chania())
#print(province_rethymno())
#print(province_iraklion())
#print(province_lasithi())


# Union and Centroid
# Union method will unite the two layers and dissolve will return one layer by a common column
#union = gpd.overlay(provinces, states, how='union')
#union['common'] = 1
#dissolve = union.dissolve(by='common')
#centroid = union['geometry'].centroid
#fig1, ax1 = plt.subplots()
#centroid.plot(ax=ax1, color='none', edgecolor='purple')
#dissolve.plot(ax=ax1, color='none', edgecolor='cyan')
#union.plot(color='none', edgecolor='orange')


# Buffer
#buffer = rivers['geometry'].buffer(distance=800) # buffing the river linestring for 800 metres
#buffer.plot(edgecolor='k', color='blue')
#plt.show()


# For projected layers CRS added universal transverse mercator UTM coordinate system at 35
CRS = ccrs.UTM(35)
fig, ax, = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection=CRS))
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[26.5, 26, 25.5, 25, 24.5, 24, 23.5, 23],
                         ylocs=[34, 34.5, 35, 35.5, 36])
gridlines.right_labels = False
gridlines.bottom_labels = False


# Plotting the individual shapefiles and overlapping the plots ax=ax
outline.plot(ax=ax, edgecolor='black', color='none', alpha=1)
provinces.plot(ax=ax, edgecolor='black', color=color, alpha=1)
cities.plot(ax=ax, edgecolor='black', markersize=100, color='magenta')
refuges.plot(ax=ax, color='g')
rivers.plot(ax=ax, color='b', alpha=1)


# The title of the map
plt.title('This is the map of Crete', fontsize=16)


# Checking the unique names and the len of the provinces attribute
num_provinces = len(provinces.name.apply(unique_name))
#print('Number of unique features: {}'.format(num_provinces))


# Creating a list with unique names of the provinces
provinces_names = provinces.name.unique()
#print('{}'.format(provinces_names))


# Creating handles and trigger the function generate_legend to bring the m.pathces labels into the map
provinces_handles = generate_legend(provinces.name, color, alpha=1)
refuges_handle = generate_legend(refuges.name, color='g', alpha=1)


# Define the column geometry x and y axis for cities shapefile points
y_cities = cities.geometry.y
x_cities = cities.geometry.x


# Creating a plot on the map for the points calling the x and y axis from attribute layer
cities_handles = ax.plot(x_cities, y_cities, color='magenta',
                                            label='Cities',
                                            marker='o',
                                            linestyle='None',
                                            markersize=8)

rivers_handle = ax.plot([], color='b', linewidth=2, label='Rivers')


# Adding the name of cities on the map pulling the names from column 'name'
for x_cities, y_cities, name in zip(
    cities.geometry.x, cities.geometry.y, cities.name):
        ax.annotate(name, xy=(x_cities, y_cities),  backgroundcolor="None", fontsize=12, horizontalalignment='center',
                                                    verticalalignment='bottom', ha="center",
                                                    xytext=(85, 35), textcoords='offset points',
                                                    bbox=dict(boxstyle="round4,pad=.5", fc="0.9"),
                                                    arrowprops=dict(arrowstyle="->",
                                                    connectionstyle="angle,angleA=0,angleB=80,rad=20")
                                                    )


# Calling the function 'capitalize_name' to update the lower case letter to initial capital letters while looping the name attirbute in province_names
get_names = [capitalize_name(name) for name in provinces_names]


# Creating the handles
handles = provinces_handles + refuges_handle + cities_handles + rivers_handle


# Getting the labels for the legend
labels = get_names + ['Refuges', 'Cities', 'Rivers']


# Adding the legend on the map
plt.legend(handles, labels, title='Legend',
                            title_fontsize=12,
                            fontsize=10,
                            loc='upper right')

# Calling a style 'bmh' for better visualisation
plt.style.use('bmh')


# More styles are available below
#print(plt.style.available)


# Scale bar
scale_bar(ax, 20)


# In order to observe the base map you need to install the "contextily" package below. Please make a note DO NOT ADD THE QUOTATION MARKS ON CMD COMMAND
# 1) Option, Open the cmd on windows or linux or mac and type "conda install contextily" or "conda install -c conda-forge contextily" and if not installed because the Current channel are not available go to option 2
# 2) Option, If the above doesnt work you can type "conda config --append channels conda-forge" and after the channel install again type "conda install contextily" and if not work go to option 3
# 3) Option, type the following on cmd "pip3 install contextily==1.0rc2" and hopefully you have install the contextily package now
# The watercolor added as main basemap as Crete is an island but 4 more basemaps added if you want to observe different basemaps
# Just commend the Watercolor and uncomment the next basemap
# Uncomment the following code
#ctx.add_basemap(ax=ax, crs='epsg:32635',  source=ctx.providers.Stamen.Watercolor
                #source=ctx.providers.OpenTopoMap
                #source=ctx.providers.Stamen.TerrainBackground
                #source=ctx.providers.CartoDB.Voyager
                #source=ctx.providers.OpenStreetMap.Mapnik )


# Uncomment the plt.show to observe the final map of Crete
#plt.show()


#Uncomment the following line of code in order to save the image to your local folder same with your py
#fig.savefig('map.png', bbox_inches='tight', dpi=300)