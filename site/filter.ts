import { MarkerManager } from "./marker_manager";
import { Apartment } from "./apartment";

interface Filterable {
    (apartment: Apartment, formData: FormData): boolean
}

export class Filter {
    filters: [Filterable] = [
        priceFilter,
        sizeFilter,
        furnishedFilter,
        animalFilter
    ];

    marker_manager: MarkerManager
    all_apartments: Set<Apartment>
    form: HTMLFormElement

    constructor(apartments: Set<Apartment>, marker_manager: MarkerManager) {
        this.marker_manager = marker_manager;
        this.all_apartments = apartments;

        this.form = document.querySelector('#sidebar form');
        
        this.form.onchange = this.onFormChange.bind(this);
        this.form.onsubmit = (e) => e.preventDefault();
    }

    onFormChange(e: any) {
        console.log("here");
        e.preventDefault();
        const formData = new FormData(this.form);

        const matching_apartments = new Set();
        for (let apartment of this.all_apartments) {
            let pass = true;
            for (let filter of this.filters) {
                pass = pass && filter(apartment, formData);
            }

            if (pass) {
                matching_apartments.add(apartment);
            }
        }

        this.marker_manager.displayApartments(matching_apartments);
    }
}

const priceFilter: Filterable = (apartment, formData) => {
    const max_input_value = formData.get('maxPrice').toString();
    const max_price = Number.parseFloat(max_input_value) || Number.MAX_VALUE;

    const min_input_value = formData.get('minPrice').toString();
    const min_price = Number.parseFloat(min_input_value) || Number.MIN_VALUE;


    const realPrice = apartment.price / 100;
    return min_price <= realPrice && realPrice <= max_price;
}

const furnishedFilter: Filterable = (apartment, formData) => {
    const name = formData.get('meuble').toString();

    switch (name) {
        case "peuimporte": return true;
        case "oui": return apartment.is_furnished === true;
        case "non": return apartment.is_furnished === false;
        default: alert("problem in furnishedFilter");
    }
}

const animalFilter: Filterable = (apartment, formData) => {
    const name = formData.get('animaux').toString();

    switch (name) {
        case "peuimporte": return true;
        case "oui": return apartment.allows_animals === true;
        case "non": return apartment.allows_animals === false;
        default: alert("problem in animalFilter");
    }
}

const sizeFilter: Filterable = (apartment, formData) => {
    const sizes = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5];

    for (let size of sizes) {
        const as_string = size.toString();
        const size_is_on = formData.get(as_string) === 'on';
        
        if (size_is_on && apartment.num_rooms == size) {
            return true;
        }

        if (size_is_on && size == 6.5 && apartment.num_rooms > size) {
            return true;
        }
    }

    return false;
}
