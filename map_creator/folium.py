# import libraries
import folium
import pandas as pd

#https://python-graph-gallery.com/312-add-markers-on-folium-map/
def create_map(concerts_data):
    lat=[]
    lon=[]
    for concert in concerts_data:
        lat.append(int(concert['location']['lat']))
        lon.append(int(concert['location']['lng']))
    # Make a data frame with dots to show on the map
    data = pd.DataFrame({
        'lat': lat,
        'lon': lon,
        #'name': ['Buenos Aires', 'Paris', 'melbourne', 'St Petersbourg', 'Abidjan', 'Montreal', 'Nairobi', 'Salvador']
    })
    #data

    # Make an empty map
    m = folium.Map(location=[20, 0], tiles="Mapbox Control Room", zoom_start=2)

    # I can add marker one by one on the map
    for i in range(0, len(data)):
        folium.Marker([data.iloc[i]['lat'], data.iloc[i]['lon']]).add_to(m)

    # Save it as html
    m.save('templates/map.html')
    html_string = m.get_root().render()
    return html_string
