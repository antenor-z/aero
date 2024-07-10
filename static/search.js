function searchAirports() {
    var query = document.getElementById('searchInput').value.toLowerCase()

    var airports = document.getElementsByClassName('airport')

    var visibleCount = 0
    for (var i = 0; i < airports.length; i++) {
        var airport = airports[i]

        var city = airport.querySelector('.box-airport-name').textContent.toLowerCase()
        var icao = airport.querySelector('.box-value').textContent.split(' ● ')[0].toLowerCase()
        var airportName = airport.querySelector('.box-value').textContent.split(' ● ')[1].toLowerCase()

        if (city.includes(query) || icao.includes(query) || airportName.includes(query)) {
            airport.style.display = 'block'
            visibleCount += 1
        } else {
            airport.style.display = 'none'
        }
    }

    var noResultMessage = document.getElementById('noResultMessage')
    if (visibleCount > 0) {
        noResultMessage.style.display = 'none'
    } else {
        noResultMessage.style.display = 'block'
    }

    var enterMessage = document.getElementById('enterMessage')
    if (visibleCount === 1) {
        enterMessage.style.display = 'block'
    } else {
        enterMessage.style.display = 'none'
    }
}

document.getElementById('searchInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        var airports = document.getElementsByClassName('airport')
        var visibleAirports = [];

        for (var i = 0; i < airports.length; i++) {
            if (airports[i].style.display !== 'none') {
                visibleAirports.push(airports[i])
            }
        }

        if (visibleAirports.length === 1) {
            var icaoCode = visibleAirports[0].querySelector('.box-value').textContent.split(' ● ')[0]
            window.location.href = '/info/' + icaoCode
        }
    }
})