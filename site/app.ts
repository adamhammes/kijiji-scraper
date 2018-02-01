import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import './main.css';

import * as L from 'leaflet';
import 'leaflet.markercluster';

import apartments from './apartment';
import { genPopupContent } from './popup';
import { ApartmentMarker, MarkerManager } from './marker_manager';
import { Filter } from './filter';

const quebecLocation = {
	lat: 46.82,
	lng: -71.3,
};

const minZoom = 9;
const defaultZoom = minZoom + 2

const map = L.map('mapContainer').setView(quebecLocation, defaultZoom);

const accessToken = 'pk.eyJ1IjoiYWRhbWhhbW1lcyIsImEiOiJjamQxczNrajQyd25kMndvNWR6cGdqYWl2In0.30k-mIhdJr0otiiSv8mQ-w';

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Todo',
	minZoom: minZoom,
	id: 'mapbox.streets',
	accessToken: accessToken
}).addTo(map);

const apartment_cluster = L.markerClusterGroup({
	disableClusteringAtZoom: 15,
	spiderfyOnMaxZoom: false
});
map.addLayer(apartment_cluster);

const mids: Set<ApartmentMarker> = new Set();
for (let [_, apartment] of apartments) {
	const marker = L.marker([apartment.latitude, apartment.longitude]);

	const popupContent = genPopupContent(apartment);
	const popup = L.popup({
		maxHeight: 250
	}).setContent(popupContent);

	marker.bindPopup(popup);

	mids.add({ apartment, marker });
}

const marker_manager = new MarkerManager(apartment_cluster, mids);
marker_manager.displayAll();


const apartment_set = new Set();
for (let [_, apartment] of apartments) {
	apartment_set.add(apartment);
}

const filter = new Filter(apartment_set, marker_manager);
