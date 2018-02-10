import { Apartment } from './apartment';
import { MarkerStatus } from './markers/marker_manager';

export class Persister {
  private markerStatuses: Map<number, MarkerStatus>;

  constructor(apartments: Set<Apartment>) {
    let persisted: Map<number, MarkerStatus>;
    try {
      persisted = new Map(
        JSON.parse(localStorage.getItem('favoritedApartments'))
      );
    } catch {
      persisted = new Map();
    }

    this.markerStatuses = new Map();
    for (let ap of apartments) {
      if (persisted.has(ap.id)) {
        this.markerStatuses.set(ap.id, persisted.get(ap.id));
      } else {
        this.markerStatuses.set(ap.id, MarkerStatus.Default);
      }
    }
  }

  markerStatus(ap: Apartment): MarkerStatus {
    return this.markerStatuses.get(ap.id);
  }

  persistStatuses(): void {
    const apArray = [];

    for (let entry of this.markerStatuses) {
      apArray.push(entry);
    }

    localStorage.setItem('favoritedApartments', JSON.stringify(apArray));
  }

  setStatus(ap: Apartment, status: MarkerStatus): void {
    this.markerStatuses.set(ap.id, status);
    this.persistStatuses();
  }
}
