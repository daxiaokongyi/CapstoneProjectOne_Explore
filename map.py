import folium

# Create map object
m = folium.Map(location=[37.7338, -122.4467],zoom_start=12)

# Global tooltip
tooltip = 'Click For More Info'

# Create markers
folium.Marker([37.733795, -122.446747], popup='<strong>Location One</strong>', tooltip=tooltip).add_to(m)

# Generate map
m.save('map.html')