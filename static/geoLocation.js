geoStorage = window.localStorage;

const successCallback = async position => {
    console.log(position);
    console.log(position.coords);
    console.log(position.coords.latitude);
    myLatitude = position.coords.latitude;
    console.log(position.coords.longitude);
    myLongitude = position.coords.longitude;

    localStorage.setItem('latitude', myLatitude);
    localStorage.setItem('longitude', myLongitude);

    console.log(myLatitude);
    console.log(myLongitude);
}

const errorCallback = position => {
    console.error(error);
}

navigator.geolocation.getCurrentPosition(successCallback, errorCallback, {
    enableHighAccuracy: true
})




