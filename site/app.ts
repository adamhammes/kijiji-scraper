import './main.scss';

import 'leaflet';
import 'leaflet.markercluster';

declare const L: any;

import apartments from './apartment';
import { MarkerManager } from './markers/marker_manager';
import { Filter } from './filter';
import { Persister } from './persister';

const quebecLocation = {
  lat: 46.82,
  lng: -71.3
};

const minZoom = 9;
const defaultZoom = minZoom + 2;

const map = L.map('mapContainer').setView(quebecLocation, defaultZoom);

const accessToken =
  'pk.eyJ1IjoiYWRhbWhhbW1lcyIsImEiOiJjamQxczNrajQyd25kMndvNWR6cGdqYWl2In0.30k-mIhdJr0otiiSv8mQ-w';
const attribution =
  'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://createivecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery @ <a href="http://mapbox.com">Mapbox</a>';
L.tileLayer(
  'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
  {
    attribution,
    minZoom,
    id: 'mapbox.streets',
    accessToken
  }
).addTo(map);

const apartment_cluster = L.markerClusterGroup({
  disableClusteringAtZoom: 15,
  spiderfyOnMaxZoom: false
});
map.addLayer(apartment_cluster);

const apartment_set = new Set();
for (let [_, apartment] of apartments) {
  apartment_set.add(apartment);
}

const persister = new Persister(apartment_set);
const marker_manager = new MarkerManager(
  apartment_cluster,
  apartment_set,
  persister
);
marker_manager.displayAll();

const filter = new Filter(apartment_set, marker_manager);
filter.filter();
