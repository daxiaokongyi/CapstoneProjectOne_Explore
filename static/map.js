// let latitude = business['coordinates']['latitude'];
// let longitude = business['coordinates']['longitude'];

const mymap = L.map('mapid').setView([51.505, -0.09],13);
// const mymap = L.map('mapid').setView([latitude, longitude],13);

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, {attribution});

tiles.addTo(mymap);

const api_url = 'https://api.wheretheiss.at/v1/satellites/25544';

async function getIss() {
    const response = await fetch(api_url);
    const data = await response.json();
    const {latitude, longitude} = data;

    console.log(latitude);
    console.log(longitude);
    L.marker([latitude, longitude]).addTo(mymap);

    // L.marker([51.505, -0.09]).addTo(mymap);
}

getIss();