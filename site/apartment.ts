declare function require(path: string): any;

const apartment_json = require('../example_values.json');

interface Apartment {
  id: string,
  address: string,
  url: string,
  headline: string,
  description: string,
  date: string,
  price: number,
  num_rooms: number,
  is_furnished: boolean,
  allows_animals: boolean,
  latitude: number,
  longitude: number
};

const apartments: Array<Apartment> = Array.from(Object.values(apartment_json));

export default apartments;
