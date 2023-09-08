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
  if (!graphsInitialized) {
    timeDomainChart = new Chart(document.getElementById("timeDomainChart"), {
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
    frequencyDomainChart = new Chart(
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
    graphsInitialized = true
  }
}

document.getElementById("show-graphs-btn").addEventListener("click", () => {
  initializeCharts()
  // plotGraphs()
})

function plotGraphs() {
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

  new Chart(document.getElementById("frequencyDomainChart"), {
    type: "line",
    data: {
      labels: Array.from({ length: data.fourierData.real.length }, (_, i) => i),
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
  })
}

function playAudio() {
  initializeCharts()
console.log("played...");

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
      requestAnimationFrame(updateGraphs) // Llamamos a updateGraphs aquí
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
    let currentTime = audioContext.currentTime - startTime // Calculamos el tiempo transcurrido
    let currentIndex = Math.floor(
      (currentTime / audioDuration) * data.audioData.length
    )

    timeDomainChart.data.labels = Array.from(
      { length: currentIndex },
      (_, i) => i / sampleRate
    )
    timeDomainChart.data.datasets[0].data = data.audioData.slice(
      0,
      currentIndex
    )

    frequencyDomainChart.data.labels = Array.from(
      { length: currentIndex },
      (_, i) => i / sampleRate
    )
    frequencyDomainChart.data.datasets[0].data = data.fourierData.real.slice(
      0,
      currentIndex
    )
    frequencyDomainChart.data.datasets[1].data = data.fourierData.imag.slice(
      0,
      currentIndex
    )

    timeDomainChart.update()
    frequencyDomainChart.update()

    requestAnimationFrame(updateGraphs)
  }
}

// function updateGraphs() {
//   if (source) {
//     let currentTime = audioContext.currentTime
//     currentIndex = Math.floor(
//       (currentTime / audioDuration) * data.audioData.length
//     )

//     timeDomainChart.data.labels = Array.from(
//       { length: currentIndex },
//       (_, i) => i / sampleRate
//     )
//     timeDomainChart.data.datasets[0].data = data.audioData.slice(
//       0,
//       currentIndex
//     )

//     frequencyDomainChart.data.labels = Array.from(
//       { length: currentIndex },
//       (_, i) => i / sampleRate
//     )
//     frequencyDomainChart.data.datasets[0].data = data.fourierData.real.slice(
//       0,
//       currentIndex
//     )
//     frequencyDomainChart.data.datasets[1].data = data.fourierData.imag.slice(
//       0,
//       currentIndex
//     )

//     timeDomainChart.update()
//     frequencyDomainChart.update()

//     requestAnimationFrame(updateGraphs)
//   }
// }

// function updateGraphs() {
//   if (source) {
//     let currentTime = audioContext.currentTime
//     currentIndex = Math.floor(
//       (currentTime / audioDuration) * data.audioData.length
//     )

//     let sliceSize = 100 // Ajusta este valor para encontrar el mejor rendimiento
//     let startIndex = Math.max(0, currentIndex - sliceSize)

//     timeDomainChart.data.labels = timeDomainChart.data.labels.slice(
//       startIndex,
//       currentIndex
//     )
//     timeDomainChart.data.datasets[0].data = data.audioData.slice(
//       startIndex,
//       currentIndex
//     )

//     frequencyDomainChart.data.labels = frequencyDomainChart.data.labels.slice(
//       startIndex,
//       currentIndex
//     )
//     frequencyDomainChart.data.datasets[0].data = data.fourierData.real.slice(
//       startIndex,
//       currentIndex
//     )
//     frequencyDomainChart.data.datasets[1].data = data.fourierData.imag.slice(
//       startIndex,
//       currentIndex
//     )

//     timeDomainChart.update({ duration: 0 }) // desactivar animaciones puede ayudar
//     frequencyDomainChart.update({ duration: 0 })

//     requestAnimationFrame(updateGraphs)
//   }
// }
