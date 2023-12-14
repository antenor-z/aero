function searchAirports() {
    var query = document.getElementById('searchInput').value.toLowerCase()

    var airports = document.getElementsByClassName('airport')

    let resultFound = false

    for (var i = 0; i < airports.length; i++) {
        var airport = airports[i]

        var city = airport.querySelector('.box-airport-name').textContent.toLowerCase()
        var icao = airport.querySelector('.box-value').textContent.split(' ● ')[0].toLowerCase()
        var airportName = airport.querySelector('.box-value').textContent.split(' ● ')[1].toLowerCase()

        if (city.includes(query) || icao.includes(query) || airportName.includes(query)) {
            airport.style.display = 'block'
            resultFound = true
        } else {
            airport.style.display = 'none'
        }

        var noResultMessage = document.getElementById('noResultMessage')
        if (resultFound) {
            noResultMessage.style.display = 'none'
        } else {
            noResultMessage.style.display = 'block'
        }
    }
}