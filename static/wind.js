function calculateWind() {
  const runwayHead = document.getElementById("runway-head").value
  const windDir = document.getElementById("wind-dir").value
  const windSpeed = document.getElementById("wind-speed").value
  calculateWindReq(windDir, windSpeed, runwayHead)
  .then(result => {
    console.log(result)

    let head = result.head * 10
    let cross = result.cross * 10
    let speed = windSpeed * 10

    document.getElementById("vector-head").setAttribute("height", Math.abs(head))
    if (head < 0)
    {
      document.getElementById("vector-head").setAttribute('transform', 'rotate(' + 180 + ' 0 0)')
      document.getElementById("label-head").textContent = `vento de cauda ${Math.abs(result.head)} nós`
    }
    else 
    {
      document.getElementById("vector-head").setAttribute('transform', 'rotate(' + 0 + ' 0 0)')
      document.getElementById("label-head").textContent = `vento de proa ${Math.abs(result.head)} nós`
    }
  

    document.getElementById("vector-cross").setAttribute("height", Math.abs(cross))
    if (cross < 0)
    {
      document.getElementById("vector-cross").setAttribute('transform', 'rotate(' + 270 + ' 0 0)')
      document.getElementById("label-cross").textContent = `vindo pela esquerda com ${Math.abs(result.cross)} nós`
    }
    else
    {
      document.getElementById("vector-cross").setAttribute('transform', 'rotate(' + 90 + ' 0 0)')
      document.getElementById("label-cross").textContent = `vindo pela direita com ${Math.abs(result.cross)} nós`
    }

    document.getElementById("vector").setAttribute('transform', 'rotate(' + result.angle + ' 0 0)')
    document.getElementById("vector").setAttribute("height", Math.abs(speed))

    document.getElementById("runway-number").textContent = Math.round(runwayHead / 10)
    

  })
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