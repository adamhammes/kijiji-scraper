import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import './main.css';

import * as L from 'leaflet';
import 'leaflet.markercluster';

import apartments from './apartment';

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

const apartment_markers = apartments.filter(apartment => {
	return apartment.latitude != null || apartment.latitude != null;
}).map(apartment => {
	const marker = L.marker([apartment.latitude, apartment.longitude]);

	const title = apartment.headline;
	const link = apartment.url;
	const popupText = `<h3><a target="_blank" href="${link}">${title}</a></h2>${apartment.description}`;

	const popup = L.popup({
		maxHeight: 250
	}).setContent(popupText);

	marker.bindPopup(popup);
	return marker;	
});

apartment_cluster.addLayers(apartment_markers);
map.addLayer(apartment_cluster);