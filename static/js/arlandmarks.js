function addLandmarks(landmarkData){
    var aScene = $('a-scene');
    // aScene.find('a-camera').remove();
    // aScene.find('a-image').remove();

    // <a-image gps-entity-place="" name="CorePower Yoga" src="../assets/map-marker.png" scale="" material="" geometry=""></a-image>
    landmarkData.features.forEach(landmark => {
        var coordinates = landmark.geometry.coordinates;
        var latitude = coordinates[1];
        var longitude = coordinates[0];
        var gpsEntityPlace = `latitude: ${latitude}; longitude: ${longitude}`
        console.log(gpsEntityPlace);

        var aImage = $(`<a-image gps-entity-place="${gpsEntityPlace}"></a-image>`);
        aImage.attr({
            'name': landmark.properties.name,
            'src': '/static/images/map-marker.png',
            'scale': '',
            'material': '',
            'geometry': ''
        });
        aScene.append(aImage);
    });
}


function loadLandmarks(latitude, longitude){
    fetch(`/api/landmarks?latitude=${latitude}&longitude=${longitude}`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            addLandmarks(data);
            console.log(data);
        });
}

function onGeolocateSuccess(pos) {
    let { latitude, longitude } = pos.coords;
    loadLandmarks(latitude, longitude)
    console.log(latitude, longitude);
}

function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
}

var options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};

navigator.geolocation.getCurrentPosition(onGeolocateSuccess, error, options);