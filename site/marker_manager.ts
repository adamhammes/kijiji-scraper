import { Apartment } from './apartment';

import * as L from 'leaflet';
import 'drmonty-leaflet-awesome-markers/css/leaflet.awesome-markers.css';
import 'drmonty-leaflet-awesome-markers';
import { genPopupContent } from './popup';

enum MarkerStatus {
    Normal,
    Starred,
    Ignored
}

const normalIcon = L.AwesomeMarkers.icon({
    prefix: 'fa',
    icon: 'star',
    markerColor: 'blue'
});

const starredIcon = L.AwesomeMarkers.icon({
    prefix: 'fa',
    icon: 'bookmark',
    markerColor: 'green'
});

const ignoredIcon = L.AwesomeMarkers.icon({
    prefix: 'fa',
    icon: 'star',
    markerColor: 'red'
});

export class MarkerManager {
    private allMarkers: Map<number, L.Marker> = new Map();

    private markerStatus: Map<number, MarkerStatus> = new Map();

    private cluster: L.MarkerClusterGroup

    constructor(cluster: L.MarkerClusterGroup, apartments: Set<Apartment>) {
        this.cluster = cluster;

        for (const apartment of apartments) {
            this.markerStatus.set(apartment.id, MarkerStatus.Starred);
            const marker = this.createMarker(apartment);
            this.allMarkers.set(apartment.id, marker);
        }
    }

    private createMarker(apartment: Apartment): L.Marker {
        const status = this.markerStatus.get(apartment.id);
        const marker = L.marker(
            [apartment.latitude, apartment.longitude],
            { icon: this.statusIcon(status) }
        );

        const popupContent = genPopupContent(apartment);
        const popup = L.popup({
            maxHeight: 250
        }).setContent(popupContent);

        marker.bindPopup(popup);

        return marker;
    }

    private statusIcon(stats: MarkerStatus) {
        switch (stats) {
            case MarkerStatus.Ignored: return ignoredIcon;
            case MarkerStatus.Normal: return normalIcon;
            case MarkerStatus.Starred: return starredIcon;
            default: alert('Problem in statusIcon');
        }
    }

    displayAll() {
        const toAdd = []
        for (let [_, marker] of this.allMarkers) {
            toAdd.push(marker)
        }

        this.cluster.addLayers(toAdd);
    }

    displayApartments(apartments: Set<Apartment>) {
        this.cluster.clearLayers();

        const toAdd = [];
        for (let apartment of apartments) {
            toAdd.push(this.allMarkers.get(apartment.id));
        }
        this.cluster.addLayers(toAdd);
    }
}
