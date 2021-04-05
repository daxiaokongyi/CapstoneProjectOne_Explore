// let geoStorage = window.localStorage;
let userLatitude;
let userLongitude;
let userCityObject;
let userCity;

const successCallback = async position => {
    try {
        console.log(position);
        // console.log(position.coords);
        console.log(position.coords.latitude);
        console.log(position.coords.longitude);

        userLatitude = position.coords.latitude;
        userLongitude = position.coords.longitude;
        userCityObject = await axios.get(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${userLatitude}&longitude=${userLongitude}&localityLanguage=en`);

        // console.log(userCityObject.data.city);

        userCity = userCityObject.data.city;
        console.log(userCity);

        if (userCity) {
            document.getElementById('city').innerText = userCity;
        } else {
            document.getElementById('city').innerText = "Your City";
        }


        localStorage.setItem('latitude', userLatitude);
        localStorage.setItem('longitude', userLongitude);
        localStorage.setItem('city', userCity);
        
        console.log(localStorage.getItem('latitude'));
        console.log(localStorage.getItem('longitude'));
        console.log(localStorage.getItem('city'));

        let payload = {"latitude": userLatitude, "longitude": userLongitude, "city": userCity};
        console.log(payload);
        await axios.post('/api/location', payload);
    } catch (error) {
        console.log(error);
    }

}

const errorCallback = error => {
    console.error(error);
}

navigator.geolocation.getCurrentPosition(successCallback, errorCallback, {
    enableHighAccuracy: true
})






