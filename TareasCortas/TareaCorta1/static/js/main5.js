let audioContext = new AudioContext()
let audioBuffer
let source
let data
let currentSampleIndex = 0
const samplesPerFrame = 1000 // ajusta según sea necesario
let chartInstance
let frequencyChartInstance
let intervalId
let decodedData
let isPlaying = false

function updateGraphs() {
  if (currentSampleIndex < data.audioData.length - samplesPerFrame) {
    plotGraphs(false)
    currentSampleIndex += samplesPerFrame
  } else {
    clearInterval(intervalId)
  }
}

fetch("/get_data")
  .then((response) => response.json())
  .then((jsonData) => {
    data = jsonData
    console.log("====>", data)
    plotGraphs()
  })

function plotGraphs(initial = true) {
  if (!data) {
    console.error("Data is not loaded yet.")
    return
  }

  if (initial) {
    chartInstance = new Chart(document.getElementById("timeDomainChart"), {
      type: "line",
      data: {
        labels: Array.from({ length: samplesPerFrame }, (_, i) => i),
        datasets: [
          {
            data: [],
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
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: "xy",
            },
            zoom: {
              wheel: {
                enabled: true,
              },
              pinch: {
                enabled: true,
              },
              mode: "xy",
              drag: {
                enabled: true,
              },
            },
          },
        },
      },
    })

    frequencyChartInstance = new Chart(
      document.getElementById("frequencyDomainChart"),
      {
        type: "line",
        data: {
          labels: Array.from({ length: samplesPerFrame }, (_, i) => i),
          datasets: [
            {
              data: [],
              label: "Frequency Domain (Real)",
              borderColor: "red",
              fill: false,
            },
            {
              data: [],
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
          plugins: {
            zoom: {
              pan: {
                enabled: true,
                mode: "xy",
              },
              zoom: {
                wheel: {
                  enabled: true,
                },
                pinch: {
                  enabled: true,
                },
                mode: "xy",
                drag: {
                  enabled: true,
                },
              },
            },
          },
        },
      }
    )
  } else {
    if (!chartInstance || !frequencyChartInstance) {
      console.error(
        "Chart instance or frequencyChartInstance is not created yet."
      )
      return
    }

    const newAudioData = data.audioData.slice(
      currentSampleIndex,
      currentSampleIndex + samplesPerFrame
    )
    chartInstance.data.labels = Array.from(
      { length: newAudioData.length },
      (_, i) => i + currentSampleIndex
    )
    chartInstance.data.datasets[0].data = newAudioData
    chartInstance.update()

    const newFourierRealData = data.fourierData.real.slice(
      currentSampleIndex,
      currentSampleIndex + samplesPerFrame
    )
    const newFourierImagData = data.fourierData.imag.slice(
      currentSampleIndex,
      currentSampleIndex + samplesPerFrame
    )
    frequencyChartInstance.data.labels = Array.from(
      { length: newFourierRealData.length },
      (_, i) => i + currentSampleIndex
    )
    frequencyChartInstance.data.datasets[0].data = newFourierRealData
    frequencyChartInstance.data.datasets[1].data = newFourierImagData
    frequencyChartInstance.update()

    currentSampleIndex += samplesPerFrame
  }
}

function resetZoom() {
  chartInstance.resetZoom()
  frequencyChartInstance.resetZoom()
}

function loadAudio() {
  fetch("/static/audio/Violin.wav")
    .then((response) => response.arrayBuffer())
    .then((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer))
    .then((data) => {
      decodedData = data
    })
}

function playAudio() {
  if (!decodedData) {
    console.error("Audio data has not been loaded yet.")
    return
  }

  source = audioContext.createBufferSource()
  source.buffer = decodedData
  source.connect(audioContext.destination)
  source.start(
    audioContext.currentTime,
    (currentSampleIndex / data.audioData.length) * decodedData.duration
  )

  source.onended = () => {
    clearInterval(intervalId)
    isPlaying = false
    document.getElementById("playPauseButton").innerText = "Play"
  }
  intervalId = setInterval(updateGraphs, 100) // ajusta según sea necesario
}

function pauseAudio() {
  if (source) {
    source.stop()
    source = null
    clearInterval(intervalId)
  }
}

function rewindAudio() {
  if (source) {
    source.stop()
    source = null
    clearInterval(intervalId)
  }

  if (currentSampleIndex >= samplesPerFrame) {
    currentSampleIndex -= samplesPerFrame // ajusta según sea necesario
    playAudio()
  }
}

function forwardAudio() {
  if (source) {
    source.stop()
    source = null
    clearInterval(intervalId)
  }
  if (currentSampleIndex < data.audioData.length - samplesPerFrame) {
    currentSampleIndex += samplesPerFrame // ajusta según sea necesario
    playAudio()
  }
}

function togglePlayPause() {
  if (isPlaying) {
    pauseAudio()
    console.log("playing... so pause")
  } else {
    playAudio()
    console.log("pause... so play")
  }
  isPlaying = !isPlaying
  document.getElementById("playPauseButton").innerText = isPlaying
    ? "Pause"
    : "Play"
}

function resetAudio() {
  if (source) {
    source.stop()
    source = null
  }

  currentSampleIndex = 0
  clearInterval(intervalId)

  // Limpia los datos de los gráficos
  chartInstance.data.datasets[0].data = []
  chartInstance.update()

  frequencyChartInstance.data.datasets[0].data = []
  frequencyChartInstance.data.datasets[1].data = []
  frequencyChartInstance.update()
}

loadAudio()
