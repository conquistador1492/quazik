const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 0;
let markers = [];

function initMap() {
  const moscow = { lat: 55.75, lng: 37.61 };

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: moscow,
  });

  google.maps.event.addListener(map, "click", (event) => {
    addMarker(event.latLng, map);
  });
}

function addMarker(location, map) {
  markers.push(new google.maps.Marker({
    position: location,
    label: labels[labelIndex % labels.length],
    map: map,
  }));

    $('<input />').attr('type', 'hidden')
        .attr('name', labels[labelIndex % labels.length])
        .attr('value', location.lat().toString() + ',' + location.lng().toString())
        .appendTo('#find-route-form');

    labelIndex++;
}
