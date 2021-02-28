let currentLat = localStorage.getItem('latitude');
let currentLong = localStorage.getItem('longitude');

console.log(currentLat, currentLong);
async function currentLocation() {
    // evt.preventDefault();
    let payload = {"latitude": currentLat, "longitude": currentLong};
    let res = await axios.post('/api/location', payload);
    // let res = await axios.post('/', payload);

    let data = res.data;
    // console.log(data);
}

currentLocation();

