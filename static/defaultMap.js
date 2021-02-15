let default_names = [];
let default_lats = [];
let default_longs = [];
let default_image_urls = [];

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

$('.default_image_url').each(function(index){
    default_image_urls.push($(this).text());
})


console.log([default_lats[0], default_longs[0]]);
console.log(typeof(default_lats[0]))
console.log(default_image_urls[0])

// const defaultMap = L.map('defaultMapId').setView([parseFloat(default_lats[0]), parseFloat(default_longs[0])], 10);

const defaultMap = L.map('defaultMapId').setView([default_lats[0], default_longs[0]], 13);

for (let i = 0; i < default_names.length; i++) {
    L.marker([default_lats[i], default_longs[i]]).addTo(defaultMap).bindTooltip(`<div style="text-align:center; color:grey; font-weight:800; margin: 0.2rem 0 ">${default_names[i]}</div><div><img style="height:6rem; border-radius:0.3rem;" src="${default_image_urls[i]}"/></div>`).openPopup();
}

const default_attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';
const default_tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const default_tiles = L.tileLayer(default_tileUrl, {default_attribution});

default_tiles.addTo(defaultMap);