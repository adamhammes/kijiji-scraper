import * as L from "leaflet";
import * as apartment_json from "../example_values.json";

const apartments = Array.from(Object.values(apartment_json));
console.log(apartments);

const quebecLocation = {
	lat: 46.82,
	lng: -71.3,
};

const minZoom = 11;

const map = L.map('mapId').setView(quebecLocation, minZoom);

const accessToken = 'pk.eyJ1IjoiYWRhbWhhbW1lcyIsImEiOiJjamQxczNrajQyd25kMndvNWR6cGdqYWl2In0.30k-mIhdJr0otiiSv8mQ-w';

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Todo',
	minZoom: minZoom,
	id: 'mapbox.streets',
	accessToken: accessToken
}).addTo(map);

apartments.forEach(apartment => {
	const marker = L.marker([apartment.latitude, apartment.longitude]).addTo(map);
	marker.bindPopup(apartment.description);
})
// for (let i = 0; i < 2000; i++) {
// }
