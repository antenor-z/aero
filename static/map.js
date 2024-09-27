const map = L.map('map').setView([-17, -52], 4.2)
      
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map)

locations.forEach(location => {
    const marker = L.marker([location.latitude, location.longitude]).addTo(map)
    
    var icon = L.icon({
        iconUrl: '/static/3p/images/marker-icon.png',
        shadowUrl: '/static/3p/images/marker-icon.png',
    
        iconSize:     [20, 20],
        shadowSize:   [0, 0],
        iconAnchor:   [10, 10],
        shadowAnchor: [0, 0],
        popupAnchor:  [5, -20]
    });

    marker.setIcon(icon)
    marker.on('mouseover', function () {
    this.openPopup()
    })

    marker.on('mouseout', function () {
    this.closePopup()
    })

    marker.bindPopup(`<b>${location.name}</b> (${location.city})`, {closeButton: false}).on('click', () => {
    window.location.href = location.url + "?mapa=1"
    })
})