declare function require(path: string): any;
const apartment_json = require('apartment_values!');

export interface Apartment {
  id: number;
  address: string;
  url: string;
  headline: string;
  description: string;
  date: string;
  price: number;
  num_rooms: number;
  is_furnished: boolean;
  allows_animals: boolean;
  latitude: number;
  longitude: number;
}

const apartments: Map<number, Apartment> = new Map();

for (let key in Object.keys(apartment_json)) {
  const apartment: Apartment = apartment_json[key];

  if (apartment.latitude != null && apartment.longitude != null) {
    apartments.set(apartment.id, apartment);
  }
}

export default apartments;
