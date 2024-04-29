function feetToNM(feet) {
    return parseFloat(feet) / 6076
  }
  function minToHour(min) {
    return parseFloat(min) / 60
  }
  function hourToMin(hour) {
    return parseFloat(hour) * 60
  }

  function calcular() {
    let currentAltitude = parseFloat(document.getElementById("curent-altitude").value)
    let desiredAltitude = parseFloat(document.getElementById("desired-altitude").value)
    let descentRate = parseFloat(document.getElementById("descent-rate").value)
    let speed = parseFloat(document.getElementById("speed").value)

    let isDegrees = document.getElementById("graus").checked

    let requiredDistance;
    if (isDegrees) {
      requiredDistance = feetToNM(currentAltitude - desiredAltitude) / Math.tan((descentRate * Math.PI) / 180)
      if (descentRate >= 4)
        document.getElementById("triangle").getElementById("remark").textContent = "Razão alta"
      else
        document.getElementById("triangle").getElementById("remark").textContent = ""
    } else {
      requiredDistance = minToHour((currentAltitude - desiredAltitude) / descentRate) * speed
      if (descentRate >= 3500)
        document.getElementById("triangle").getElementById("remark").textContent = "Razão alta"
      else
        document.getElementById("triangle").getElementById("remark").textContent = ""
    }

    let requiredTime = Math.round(hourToMin(requiredDistance / speed))

    if (!Number.isNaN(requiredDistance)) {
      requiredDistance = Math.round(requiredDistance)
      document.getElementById("triangle").getElementById("current-alt").textContent = `${currentAltitude}ft`
      document.getElementById("triangle").getElementById("desired-alt").textContent = `${desiredAltitude}ft`
      document.getElementById("triangle").getElementById("required-dist").textContent = `${requiredDistance}NM`
      document.getElementById("triangle").getElementById("required-time").textContent = `Tempo: ${requiredTime} min`
    }
    else
    {
      document.getElementById("req").innerHTML = `<span class="req-dist">Não foi possível calcular</span>`
    }
    
  }