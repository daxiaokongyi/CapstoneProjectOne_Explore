let currentLat = localStorage.getItem('latitude');
let currentLong = localStorage.getItem('longitude');
const axios = require('axios');

// console.log(currentLat, currentLong);
async function currentLocation() {
    let payload = {latitude: currentLat, longitude: currentLong};
    let res = await axios.post('/api/location', payload);
    let data = res.data;
    console.log(data);
}

currentLocation();

