// let geoStorage = window.localStorage;
let userLatitude;
let userLongitude;

const successCallback = async position => {
    // console.log(position);
    // console.log(position.coords);
    console.log(position.coords.latitude);
    console.log(position.coords.longitude);

    userLatitude = position.coords.latitude;
    userLongitude = position.coords.longitude;

    localStorage.setItem('latitude', userLatitude);
    localStorage.setItem('longitude', userLongitude);
    
    console.log(localStorage.getItem('latitude'));
    console.log(localStorage.getItem('longitude'));

    let payload = {"latitude": userLatitude, "longitude": userLongitude};
    console.log(payload);
    await axios.post('/api/location', payload);
}

const errorCallback = error => {
    console.error(error);
}

navigator.geolocation.getCurrentPosition(successCallback, errorCallback, {
    enableHighAccuracy: true
})






