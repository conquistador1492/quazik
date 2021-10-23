// function initMap() {
//   const bounds = new google.maps.LatLngBounds();
//   const markersArray = [];
//   const map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: 55.53, lng: 9.4 },
//     zoom: 10,
//   });
//   // initialize services
//   const geocoder = new google.maps.Geocoder();
//   const service = new google.maps.DistanceMatrixService();
//   // build request
//   const origin1 = { lat: 55.93, lng: -3.118 };
//   const origin2 = "Greenwich, England";
//   const destinationA = "Stockholm, Sweden";
//   const destinationB = { lat: 50.087, lng: 14.421 };
//   const request = {
//     origins: [origin1, origin2],
//     destinations: [destinationA, destinationB],
//     travelMode: google.maps.TravelMode.DRIVING,
//     unitSystem: google.maps.UnitSystem.METRIC,
//     avoidHighways: false,
//     avoidTolls: false,
//   };
//
//   // put request on page
//   document.getElementById("request").innerText = JSON.stringify(
//     request,
//     null,
//     2
//   );
//   // get distance matrix response
//   service.getDistanceMatrix(request).then((response) => {
//     // put response
//     document.getElementById("response").innerText = JSON.stringify(
//       response,
//       null,
//       2
//     );
//
//     // show on map
//     const originList = response.originAddresses;
//     const destinationList = response.destinationAddresses;
//
//     deleteMarkers(markersArray);
//
//     const showGeocodedAddressOnMap = (asDestination) => {
//       const handler = ({ results }) => {
//         map.fitBounds(bounds.extend(results[0].geometry.location));
//         markersArray.push(
//           new google.maps.Marker({
//             map,
//             position: results[0].geometry.location,
//             label: asDestination ? "D" : "O",
//           })
//         );
//       };
//       return handler;
//     };
//
//     for (let i = 0; i < originList.length; i++) {
//       const results = response.rows[i].elements;
//
//       geocoder
//         .geocode({ address: originList[i] })
//         .then(showGeocodedAddressOnMap(false));
//
//       for (let j = 0; j < results.length; j++) {
//         geocoder
//           .geocode({ address: destinationList[j] })
//           .then(showGeocodedAddressOnMap(true));
//       }
//     }
//   });
// }
//
// function deleteMarkers(markersArray) {
//   for (let i = 0; i < markersArray.length; i++) {
//     markersArray[i].setMap(null);
//   }
//
//   markersArray = [];
// }

const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 0;
let markers = [];

function initMap() {
  // const bangalore = { lat: 12.97, lng: 77.59 };

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
  new google.maps.Marker({
    position: location,
    label: labels[labelIndex++ % labels.length],
    map: map,
  });
}

// function deleteMarker(location, map) {
//   google.maps.Mar
// }