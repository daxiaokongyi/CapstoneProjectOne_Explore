let latitude = $('#lat').text();
let longitude = $('#long').text();
let myLat = $('#mylat').text();
let myLong = $('#mylong').text();

console.log(latitude);
console.log(longitude);
console.log(myLat);
console.log(myLong);

// let redMarker = L.AwesomeMarkers.icon({icon: 'coffee', markerColor: 'red'});

const mymap = L.map('mapid').setView([latitude, longitude],13);
let item = L.marker([latitude, longitude]).addTo(mymap);
let myPlace = L.marker([myLat, myLong]).addTo(mymap);
// let myPlace = L.marker([myLat, myLong], {icon : redMarker}).addTo(mymap);

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, {attribution});

tiles.addTo(mymap);