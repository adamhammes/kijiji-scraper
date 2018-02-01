import { Apartment } from './apartment';

import * as L from 'leaflet';

export interface ApartmentMarker {
    apartment: Apartment,
    marker: L.Marker
}

export class MarkerManager {
    private all_markers: Map<number, L.Marker> = new Map();

    private cluster: L.MarkerClusterGroup

    constructor(cluster: L.MarkerClusterGroup, mids: Set<ApartmentMarker>) {
        for (let mid of mids) {
            this.all_markers.set(mid.apartment.id, mid.marker);
        }

        this.cluster = cluster;
    }

    displayAll() {
        const toAdd = []
        for (let [_, marker] of this.all_markers) {
            toAdd.push(marker)
        }

        this.cluster.addLayers(toAdd);
    }

    displayApartments(apartments: Set<Apartment>) {
        this.cluster.clearLayers();

        const toAdd = [];
        for (let apartment of apartments) {
            toAdd.push(this.all_markers.get(apartment.id));
        }
        this.cluster.addLayers(toAdd);
    }
}
