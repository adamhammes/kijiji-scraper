import { Apartment } from "../apartment";
import { MarkerManager, MarkerStatus } from "./marker_manager";

interface ElementMaker {
  (ap: Apartment, manager: MarkerManager): HTMLElement;
}

export const genPopupContent = (manager: MarkerManager, ap: Apartment) => {
  const parts: ElementMaker[] = [title, status, byline, description];

  const container = document.createElement("div");

  for (const part of parts) {
    container.appendChild(part(ap, manager));
  }

  return container;
};

const description: ElementMaker = ap => {
  const p = document.createElement("p");
  p.innerHTML = ap.description;
  return p;
};

const byline: ElementMaker = ap => {
  const num_rooms = numRoomsToString(ap.num_rooms);
  const price = priceToString(ap.price);

  const bold = document.createElement("b");
  bold.innerText = `${num_rooms} | ${price}`;

  const p = document.createElement("p");
  p.appendChild(bold);

  if (typeof ap.is_furnished !== 'undefined') {
    const title = ap.is_furnished ? 'Meublé': 'Non-meublé';
    const elem = _makeIcon('home', title, !ap.is_furnished);

    p.insertAdjacentHTML('beforeend', ' | ' + elem);
  }

  if (typeof ap.allows_animals !== 'undefined') {
    const title = ap.allows_animals ? 'Animaux acceptés': 'Animaux non-acceptés';
    const elem = _makeIcon('paw', title, !ap.allows_animals);

    p.insertAdjacentHTML('beforeend', ' | ' + elem);
  }

  return p;
};

const _makeIcon = (icon: string, title: string, xout: boolean) => {
  const iconSize = xout ? ' fa-stack-1x' : ''; 
  const iconHTML = `<i title="${title}" class="fas fa-${icon}${iconSize}"/>`;
  const banHTML = '<i class="fa fa-ban fa-stack-2x"/>';

  if (xout) {
    return `<span class="fa-stack">${iconHTML}${banHTML}</span>`;
  } else {
    return iconHTML;
  }
};

const title: ElementMaker = ap => {
  const anchor = document.createElement("a");
  anchor.setAttribute("target", "_blank");
  anchor.setAttribute("href", ap.url);
  anchor.innerText = ap.headline;

  const h3 = document.createElement("h3");
  h3.appendChild(anchor);
  return h3;
};

const status: ElementMaker = (ap, manager) => {
  const favorite = document.createElement("button");
  favorite.innerHTML = '<i class="fas fa-star"></i> Favori';
  favorite.onclick = manager.statusClick.bind(
    manager,
    ap,
    MarkerStatus.Favorited
  );

  const seen = document.createElement("button");
  seen.innerHTML = '<i class="fas fa-check"></i> Marquer comme vu';
  seen.onclick = manager.statusClick.bind(manager, ap, MarkerStatus.Seen);

  const statusContainer = document.createElement("div");
  statusContainer.appendChild(favorite);
  statusContainer.appendChild(seen);

  return statusContainer;
};

/// Converts a price (in cents) into a price formatted Canadian-style.
/// Example:
///     priceToString(62000); // '620,00 $'
const priceToString = (raw_price: number) => {
  const dollars = Math.floor(raw_price / 100);
  const cents = raw_price % 100;
  const padded_cents = cents.toString().padEnd(2, "0");

  return `${dollars},${padded_cents} $`;
};

/// Examples:
///     numRoomsToString(4.5); // '4 1/2'
///     numRoomToString(2);    // '2'
const numRoomsToString = (raw_rooms: number) => {
  const integral = Math.floor(raw_rooms);
  const fractional = raw_rooms - integral === 0 ? "" : " 1/2";

  return `${integral}${fractional}`;
};
