const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 0;
let markers = [];

function initMap() {
  const bangalore = { lat: 55.75, lng: 37.61 };

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: bangalore,
  });

  // This event listener calls addMarker() when the map is clicked.
  google.maps.event.addListener(map, "click", (event) => {
    addMarker(event.latLng, map);
  });

  // google.maps.event.addListener(map, "rightclick", (event) => {
  //   deleteMarker(event.latLng, map);
  // });

  // Add a marker at the center of the map.
  // addMarker(bangalore, map);
}

// Adds a marker to the map.
function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
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
  // document.getElementById("find-route-button").style.cursor = "auto";
}

// function deleteMarker(location, map) {
//   google.maps.Mar
// }