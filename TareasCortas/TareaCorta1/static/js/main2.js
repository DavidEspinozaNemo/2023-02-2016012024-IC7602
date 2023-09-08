let audioContext = new AudioContext()
let audioBuffer
let source
let data
let currentIndex = 0
let audioDuration
let timeDomainChart
let frequencyDomainChart
let sampleRate
let startTime
let graphsInitialized = false

fetch("/get_data")
  .then((response) => response.json())
  .then((jsonData) => {
    data = jsonData
    sampleRate = data.audioFrequency
    initializeCharts()
  })

function initializeCharts() {
//   if (!graphsInitialized) {
      // timeDomainChart = new Chart(document.getElementById("timeDomainChart"), {
    new Chart(document.getElementById("timeDomainChart"), {
      type: "line",
      data: {
        labels: Array.from({ length: data.audioData.length }, (_, i) => i),
        datasets: [
          {
            data: data.audioData,
            label: "Time Domain",
            borderColor: "blue",
            fill: false,
          },
        ],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: "Sample Index",
            },
          },
          y: {
            title: {
              display: true,
              text: "Amplitude",
            },
          },
        },
      },
    })
    // frequencyDomainChart = new Chart(
    new Chart(
      document.getElementById("frequencyDomainChart"),
      {
        type: "line",
        data: {
          labels: Array.from(
            { length: data.fourierData.real.length },
            (_, i) => i
          ),
          datasets: [
            {
              data: data.fourierData.real,
              label: "Frequency Domain (Real)",
              borderColor: "red",
              fill: false,
            },
            {
              data: data.fourierData.imag,
              label: "Frequency Domain (Imaginary)",
              borderColor: "green",
              fill: false,
            },
          ],
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: "Frequency Index",
              },
            },
            y: {
              title: {
                display: true,
                text: "Magnitude",
              },
            },
          },
        },
      }
    )
    // graphsInitialized = true
//   }
}

document.getElementById("show-graphs-btn").addEventListener("click", () => {
//   initializeCharts()
})

function playAudio() {
//   initializeCharts()
  console.log("played...")

  fetch("/static/audio/Violin.wav")
    // fetch("/static/audio/rocket.wav")
    .then((response) => response.arrayBuffer())
    .then((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer))
    .then((decodedData) => {
      source = audioContext.createBufferSource()
      source.buffer = decodedData
      audioDuration = decodedData.duration // Almacenamos la duración total aquí
      source.connect(audioContext.destination)
      source.start(audioContext.currentTime)
      startTime = audioContext.currentTime
    //   requestAnimationFrame(updateGraphs) // Llamamos a updateGraphs aquí
    })
}

function pauseAudio() {
  if (source) {
    source.stop()
    source = null
  }
}

function rewindAudio() {
  // Implementación pendiente: Ajustar el offset de inicio al rebobinar
  playAudio()
}

function forwardAudio() {
  // Implementación pendiente: Ajustar el offset de inicio al avanzar
  playAudio()
}

function updateGraphs() {
  if (source) {
    let currentTime = audioContext.currentTime - startTime
    currentIndex = Math.floor(
      (currentTime / audioDuration) * data.audioData.length
    )

    // Asegúrate de que solo estamos agregando nuevos datos, no recreando el array en cada frame
    if (currentIndex > timeDomainChart.data.labels.length) {
      let newLabels = Array.from(
        { length: currentIndex - timeDomainChart.data.labels.length },
        (_, i) => (i + timeDomainChart.data.labels.length) / sampleRate
      )
      timeDomainChart.data.labels.push(...newLabels)
      timeDomainChart.data.datasets[0].data.push(
        ...data.audioData.slice(
          timeDomainChart.data.labels.length,
          currentIndex
        )
      )

      frequencyDomainChart.data.labels.push(...newLabels)
      frequencyDomainChart.data.datasets[0].data.push(
        ...data.fourierData.real.slice(
          frequencyDomainChart.data.labels.length,
          currentIndex
        )
      )
      frequencyDomainChart.data.datasets[1].data.push(
        ...data.fourierData.imag.slice(
          frequencyDomainChart.data.labels.length,
          currentIndex
        )
      )

      timeDomainChart.update()
      frequencyDomainChart.update()
    }

    requestAnimationFrame(updateGraphs)
  }
}
