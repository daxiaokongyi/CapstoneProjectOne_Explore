let default_names = [];
let default_lats = [];
let default_longs = [];

$('.default_name').each(function(index){
    default_names.push($(this).text());
})
console.log(default_names);

$('.default_lat').each(function(index){
    default_lats.push($(this).text());
})
console.log(default_lats);

$('.default_long').each(function(index){
    default_longs.push($(this).text());
})
console.log([default_lats[0], default_longs[0]]);
console.log(typeof(default_lats[0]))

// const defaultMap = L.map('defaultMapId').setView([parseFloat(default_lats[0]), parseFloat(default_longs[0])], 10);

const defaultMap = L.map('defaultMapId').setView([default_lats[0], default_longs[0]], 10);

for (let i = 0; i < 5; i++) {
    L.marker([default_lats[i], default_longs[i]]).addTo(defaultMap).bindTooltip(default_names[i]);
}

const default_attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const default_tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const default_tiles = L.tileLayer(default_tileUrl, {default_attribution});

default_tiles.addTo(defaultMap);