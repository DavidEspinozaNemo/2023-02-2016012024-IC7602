let audioContext = new AudioContext()
let audioBuffer
let source
let data

fetch("/get_data")
  .then((response) => response.json())
  .then((jsonData) => {
    data = jsonData
    console.log("====>", data)
    plotGraphs()
  })

function plotGraphs() {
  if (data) {
    console.log("si hay data");
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
  }
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
  fetch("/static/audio/Violin.wav")
    .then((response) => response.arrayBuffer())
    .then((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer))
    .then((decodedData) => {
      source = audioContext.createBufferSource()
      source.buffer = decodedData
      source.connect(audioContext.destination)
      source.start(audioContext.currentTime)
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
