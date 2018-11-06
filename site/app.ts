import "./main.scss";

import "leaflet";
import "leaflet.markercluster";

declare const L: any;

import { Apartment } from "./apartment";
import { MarkerManager } from "./markers/marker_manager";
// import { Filter } from "./filter";
import { Persister } from "./persister";

const minZoom = 9;
const defaultZoom = minZoom + 2;
let map: any;

function fetchApartments() {
  const [city, ad_type] = window.location.pathname.split("/").filter(Boolean);
  const jsonUrl = `/${city}-${ad_type}.json`;

  fetch(jsonUrl).then(response => response.json().then(loadApartments));
}

function loadApartments(data: any) {
  const location = {
    lat: data.city.latitude,
    lng: data.city.longitude
  };
  map.setView(location, defaultZoom);

  const apartment_cluster = L.markerClusterGroup({
    disableClusteringAtZoom: 15,
    spiderfyOnMaxZoom: false
  });

  map.addLayer(apartment_cluster);
  const apartments: Apartment[] = data.offers;

  const apartment_set = new Set(apartments);

  const persister = new Persister(apartment_set);
  const marker_manager = new MarkerManager(
    apartment_cluster,
    apartment_set,
    persister
  );
  marker_manager.displayAll();

  // const filter = new Filter(apartment_set, marker_manager);
  // filter.filter();
}

function main() {
  map = L.map("mapContainer");
  const accessToken =
    "pk.eyJ1IjoiYWRhbWhhbW1lcyIsImEiOiJjamQxczNrajQyd25kMndvNWR6cGdqYWl2In0.30k-mIhdJr0otiiSv8mQ-w";
  const attribution =
    'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://createivecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery @ <a href="http://mapbox.com">Mapbox</a>';
  L.tileLayer(
    "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
    {
      attribution,
      minZoom,
      id: "mapbox.streets",
      accessToken
    }
  ).addTo(map);

  fetchApartments();
}

window.addEventListener("load", main);
