# import libraries
import folium
import pandas as pd

#https://python-graph-gallery.com/312-add-markers-on-folium-map/
def create_map(concerts_data):
    lat = []
    lon = []
    city = []
    name = []
    for concert in concerts_data:
        lat.append(int(concert['location']['lat']))
        lon.append(int(concert['location']['lng']))
        city.append(str(concert['location']['city']))
        name.append((str(concert['displayName'])))
    # Make a data frame with dots to show on the map
    data = pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'city': city,
        'name': name
    })
    #data

    # Make an empty map
    m = folium.Map(location=[20, 0], tiles="cartodbdark_matter", zoom_start=2)

    # I can add marker one by one on the map
    for i in range(0, len(data)):
        if data.iloc[i]['name'] != 'null':
            popup = folium.Popup(data.iloc[i]['city']+" "+data.iloc[i]['name'], parse_html=True)
            folium.Marker([data.iloc[i]['lat'], data.iloc[i]['lon']], popup=popup).add_to(m)
        else:
            folium.Marker([data.iloc[i]['lat'], data.iloc[i]['lon']]).add_to(m)

    # Save it as html
    html_string = m.get_root().render()
    return html_string
