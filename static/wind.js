function calculateWind() {
  const runwayHead = document.getElementById("runway-head").value
  const windDir = document.getElementById("wind-dir").value
  const windSpeed = document.getElementById("wind-speed").value
  calculateWindReq(windDir, windSpeed, runwayHead)
  .then(result => {
    if (result === "erro") {
      document.getElementById("label-cross").textContent = "Erro"
      document.getElementById("label-head").textContent = "Erro"
      document.getElementById("runway-number").textContent = " X"
      return
    }

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

    let rwy =  Math.round(runwayHead / 10)
    if (rwy < 10) {
      document.getElementById("runway-number").textContent = "0" + rwy;
    }
    else {
      document.getElementById("runway-number").textContent = rwy;
    }
    

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
      return "erro"
    });
}