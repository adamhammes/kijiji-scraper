import { Apartment } from '../apartment';
import { Persister } from '../persister';

import * as L from 'leaflet';

declare function require(path: string): any;
const blueIcon = require('./icons/marker-icon-blue.png');
const yellowIcon = require('./icons/marker-icon-yellow.png');
const greyIcon = require('./icons/marker-icon-grey.png');
const shadowIcon = require('./icons/marker-shadow.png');

import { genPopupContent } from './popup';

export enum MarkerStatus {
    Default,
    Favorited,
    Seen
}

export class MarkerManager {
    private persister: Persister;
    private allMarkers: Map<number, L.Marker> = new Map();
    private markerStatus: Map<number, MarkerStatus> = new Map();

    private cluster: L.MarkerClusterGroup

    constructor(cluster: L.MarkerClusterGroup, apartments: Set<Apartment>, persister: Persister) {
        this.cluster = cluster;
        this.persister = persister

        for (const apartment of apartments) {
            this.markerStatus.set(apartment.id, this.persister.markerStatus(apartment));
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

        const popupContent = genPopupContent(this, apartment);
        const popup = L.popup({
            maxHeight: 250
        }).setContent(popupContent);

        marker.bindPopup(popup);

        return marker;
    }

    private statusIcon(stats: MarkerStatus): L.Icon {
        let icon;

        switch (stats) {
            case MarkerStatus.Default: icon = blueIcon; break;
            case MarkerStatus.Favorited: icon = yellowIcon; break;
            case MarkerStatus.Seen: icon = greyIcon; break;
            default: alert('unreachable in MarkerManager.statusIcon');
        }

        return new L.Icon({
            iconUrl: icon,
            shadowUrl: shadowIcon,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
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

    getStatus(apartment: Apartment) {
        return this.markerStatus.get(apartment.id);
    }

    statusClick(apartment: Apartment, status: MarkerStatus) {
        const currentStatus = this.getStatus(apartment);

        let newStatus;
        if (currentStatus == status) {
            newStatus = MarkerStatus.Default;
        } else {
            newStatus = status;
        }

        this.markerStatus.set(apartment.id, newStatus);
        this.persister.setStatus(apartment, newStatus);

        const marker = this.allMarkers.get(apartment.id)
        marker.setIcon(this.statusIcon(this.markerStatus.get(apartment.id)));
    }
}
