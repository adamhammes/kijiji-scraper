import { Apartment } from './apartment'

export const genPopupContent = (ap: Apartment) => {
    return `
    <h3>
      <a target="_blank" href=${ap.url}>${ap.headline}</a>
    </h3>
    <p><b>
      ${numRoomsToString(ap.num_rooms)} 
    | ${priceToString(ap.price)}
    </b></p>
    <p>${ap.description}</p>
`;
}

/// Converts a price (in cents) into a price formatted Canadian-style.
/// Example:
///     priceToString(62000); // '620,00 $'
const priceToString = (raw_price: number) => {
    const dollars = Math.floor(raw_price / 100);
    const cents = raw_price % 100;
    const padded_cents = cents.toString().padEnd(2, '0');

    return `${dollars},${padded_cents} $`;
}

/// Examples:
///     numRoomsToString(4.5); // '4 1/2'
///     numRoomToString(2);    // '2'
const numRoomsToString = (raw_rooms: number) => {
    const integral = Math.floor(raw_rooms);
    const fractional = raw_rooms - integral === 0 ? '' : ' 1/2'

    return `${integral}${fractional}`;
}
