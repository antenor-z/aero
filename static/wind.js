function calculateWind() {
    const runwayHead = document.getElementById("runway-head").value
    const windDir = document.getElementById("wind-dir").value
    const windSpeed = document.getElementById("wind-speed").value
    calculateWindReq(windDir, windSpeed, runwayHead)
    .then(result => {
      console.log(result)
      document.getElementById("w").getElementById("angle").textContent = result.angle
      document.getElementById("w").getElementById("cross").textContent = result.cross
      document.getElementById("w").getElementById("head").textContent = result.head
    });
  }
  function calculateWindReq(wind_dir, wind_speed, runway_head) {
    const apiUrl = `/windcalc/?wind_dir=${wind_dir}&wind_speed=${wind_speed}&runway_head=${runway_head}`

    return fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        return data
      })
      .catch(error => {
        console.error('Error fetching data:', error)
        return null
      });
  }