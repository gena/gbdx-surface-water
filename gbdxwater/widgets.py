from ipywidgets import interact
from IPython.display import Image, display
from IPython.html.widgets import interact

#Now let's make some HTML to style our intended mapbox output
from IPython.display import HTML

style = """
<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.css' rel='stylesheet' />

<style> #map {
  position: relative;
  min-width: 830px;
  min-height: 650px;
  overflow:visible;
}
</style>

"""

HTML(style)

code = """
<div id='map'></div>
<script type="text/Javascript">
    function selectFeature(feature) {
        var kernel = IPython.notebook.kernel;
        kernel.execute("selection = '" + JSON.stringify(feature) + "'");
        selectedFeature = feature
    }

    //Load required javascript libraries
    require.config({
      paths: {
          mapboxgl: 'https://api.tiles.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl',
          bootstrap: 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min',
          jquery: 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'
      }
    });

    IPython.OutputArea.auto_scroll_threshold = 9999;

    require(['mapboxgl', 'bootstrap', 'jquery'], function(mapboxgl, bootstrap, jquery){
        $ = jquery


        mapboxgl.accessToken = 'pk.eyJ1IjoiZ2VubmFkaXkiLCJhIjoiMm9WN3VWQSJ9.b9s_EXvxcqiAbaf5GzrEnA';
        mapboxgl.config.API_URL = 'https://api.mapbox.com';

        let map = new mapboxgl.Map({
            container: 'map', // container id
            //style: 'mapbox://styles/mapbox/dark-v8', //stylesheet location
            style: 'mapbox://styles/gennadiy/cjjbudokv2t6c2snpqmv7rlg6',
            center: [2, 35], // starting position
            zoom: 1 // starting zoom 
        });

        // add controls
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');
        map.addControl(new mapboxgl.GeolocateControl());
        // map.addControl(new mapboxgl.AttributionControl({compact: true}))
        map.addControl(new mapboxgl.ScaleControl());
        map.addControl(new mapboxgl.FullscreenControl());

        let overlay = document.getElementById('map-overlay');

        let hoveredFeature = null;
        let selectedFeature = null

        let source = 'composite'
        let sourceLayer = 'HydroLAKES_polys_v10'
        let layer = 'hydrolakes-polys-v10'

        let sourceOSM = 'composite'
        let dataHoverOSM = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [0, 0]
                    ]
                }
            }]
        };

        let sourceLayerOSM = 'water'
        let layerOSM = 'water'

        let mapBounds = map.getBounds()
        map.on('zoom', function() {
            // console.log()
        })

        map.on('load', function() {

            map.addLayer({
                "id": "waterbodies-highlighted",
                "type": "fill",
                "source": source,
                "source-layer": sourceLayer,
                "paint": {
                    "fill-outline-color": "#484896",
                    "fill-color": "#6e599f",
                    "fill-opacity": 0.75
                },
                "filter": ["in", "Hylak_id", ""]
            }, 'hydrolakes-points-v10'); // Place polygon under these labels.

            map.addLayer({
                "id": "waterbodies-selected",
                "type": "fill",
                "source": source,
                "source-layer": sourceLayer,
                "paint": {
                    "fill-outline-color": "#484896",
                    "fill-color": "#ffff00",
                    "fill-opacity": 0.75
                },
                "filter": ["in", "Hylak_id", ""]
            }, 'hydrolakes-points-v10'); // Place polygon under these labels.

            map.on("mousemove", layer, function(e) {
                map.getCanvas().style.cursor = 'pointer';

                if (e.features.length > 0) {
                    // Single out the first found feature.
                    var feature = e.features[0];

                    // Add features that share the same county name to the highlighted layer.
                    map.setFilter('waterbodies-highlighted', ['in', 'Hylak_id', feature.properties.Hylak_id]);

                    hoveredFeature = feature
                }
            });

            // Reset the state-fills-hover layer's filter when the mouse leaves the layer.
            map.on("mouseleave", layer, function() {
                map.getCanvas().style.cursor = '';
                map.setFilter('waterbodies-highlighted', ['in', 'Hylak_id', '']);

                hoveredFeature = null
            });

            map.on("click", layer, function(e) {
                if (hoveredFeature) {
                    map.setFilter('waterbodies-selected', ['in', 'Hylak_id', hoveredFeature.properties.Hylak_id]);
                    selectFeature(hoveredFeature)
                } else {
                    map.setFilter('waterbodies-selected', ['in', 'Hylak_id', null]);
                    selectFeature(null)
                }

            })
        });
    });

</script>
"""

def show_waterbodies_map():
    HTML(code)