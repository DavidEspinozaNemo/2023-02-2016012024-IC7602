let audioContext = new AudioContext()
let audioBuffer
let source
let data
let currentSampleIndex = 0
const samplesPerFrame = 1000 // ajustar según sea necesario
let chartInstance
let frequencyChartInstance
let intervalId
let decodedData
let isPlaying = false
let isFilePathSet = false

/**
 * Actualiza los gráficos en cada intervalo de tiempo
 */
const updateGraphs = () => {
  if (currentSampleIndex < data.audioData.length - samplesPerFrame) {
    plotGraphs(false)
    currentSampleIndex += samplesPerFrame
  } else {
    clearInterval(intervalId)
  }
}

//todo
// fetch("/get_data")
//   .then((response) => response.json())
//   .then((jsonData) => {
//     data = jsonData
//     plotGraphs()
//   })

/**
 * Representa gráficamente los datos en el dominio del tiempo y la frecuencia
 * @param {boolean} initial - Determina si es la primera vez que se están ploteando los datos
 */
const plotGraphs = (initial = true) => {
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

/**
 * Resetea el zoom de ambos gráficos (dominio de tiempo y frecuencia) a su estado inicial.
 */
const resetZoom = () => {
  chartInstance.resetZoom()
  frequencyChartInstance.resetZoom()
}

/**
 * Carga un archivo de audio desde una ruta específica, decodifica los datos de audio
 * y los almacena en una variable para su uso posterior.
 */
const loadAudio = () => {
  fetch("/static/audio/Violin.wav")
    .then((response) => response.arrayBuffer())
    .then((arrayBuffer) => audioContext.decodeAudioData(arrayBuffer))
    .then((data) => {
      decodedData = data
    })
}

/**
 * Inicia la reproducción del audio desde el índice de muestra actual.
 * Si el audio aún no se ha cargado, se muestra un mensaje de error en la consola.
 */
const playAudio = () => {
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

/**
 * Pausa la reproducción del audio y limpia el intervalo de actualización de los gráficos.
 */
const pauseAudio = () => {
  if (source) {
    source.stop()
    source = null
    clearInterval(intervalId)
  }
}

/**
 * Retrocede el audio por una cantidad especificada de muestras y luego reanuda la reproducción.
 */
const rewindAudio = () => {
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

/**
 * Avanza el audio por una cantidad especificada de muestras y luego reanuda la reproducción.
 */
const forwardAudio = () => {
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

/**
 * Conmuta entre el estado de reproducción y pausa del audio, y actualiza el texto del botón de reproducción/pausa de acuerdo.
 */
const togglePlayPause = () => {
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

/**
 * Restablece el audio a su estado inicial y limpia los gráficos.
 */
const resetAudio = () => {
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

// async function sendFilePathToServer() {
const sendFilePathToServer = async () => {
  const filePathInput = document.getElementById("filePathInput")
  const filePath = filePathInput.value

  if (!filePath) {
    console.error("No file path provided")
    return
  }

  try {
    const response = await fetch("/set_file_path", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ filePath }),
    })
    console.log(response)
    console.log("File path sent to the server")
    isFilePathSet = true

    if (response.ok) {
      fetch("/get_data")
        .then((response) => response.json())
        .then((jsonData) => {
          data = jsonData
          plotGraphs()
        })
    }
  } catch (error) {
    console.error("Error sending file path:", error)
  }
}

loadAudio()
