let latitude = $('#lat').text();
let longitude = $('#long').text();
let myLat = $('#mylat').text();
let myLong = $('#mylong').text();

console.log(latitude);
console.log(longitude);
console.log(myLat);
console.log(myLong);

var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const mymap = L.map('mapid').setView([latitude, longitude], 10);
L.marker([latitude, longitude]).addTo(mymap);
L.marker([myLat, myLong], {icon : greenIcon}).addTo(mymap).bindTooltip('My Location');

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, {attribution});

tiles.addTo(mymap);