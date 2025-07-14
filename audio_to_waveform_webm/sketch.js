let audio;
let fft;
let fileInput;
let isPlaying = false;
let recordButton;
let mediaRecorder;
let recordedChunks = [];
let recording = false;
let visualizing = false;
let canvas;

function setup() {
  canvas = createCanvas(640, 360);
  background(30);
  textAlign(CENTER, CENTER);
  fill(200);
  textSize(18);
  text('Upload MP3 to visualize and export as .webm', width/2, height/2);

  fileInput = createFileInput(handleFile);
  fileInput.position(10, height + 10);

  recordButton = createButton('Start Recording');
  recordButton.position(fileInput.x + fileInput.width + 10, height + 10);
  recordButton.mousePressed(toggleRecording);

  fft = new p5.FFT(0.8, 64);
}

function draw() {
  if (visualizing) {
    background(30);
    let spectrum = fft.analyze();

    let w = width / spectrum.length;
    for (let i = 0; i < spectrum.length; i++) {
      let amp = spectrum[i];
      let y = map(amp, 0, 255, height, 0);
      fill(100 + i*2, 200, 255 - i*2);
      rect(i * w, y, w - 2, height - y);
    }
  }
}

function handleFile(file) {
  if (audio) {
    audio.stop();
    audio.disconnect();
  }
  if (file.type === 'audio') {
    audio = loadSound(file.data, audioLoaded, audioLoadError);
  }
}

function audioLoaded() {
  audio.play();
  fft.setInput(audio);
  isPlaying = true;
  visualizing = true;
}

function audioLoadError(e) {
  alert('Error loading audio file!');
}

function toggleRecording() {
  if (!recording) {
    // Start recording canvas to .webm
    recordedChunks = [];
    let stream = document.querySelector('canvas').captureStream(30);
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });

    mediaRecorder.ondataavailable = function(e) {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = function() {
      let blob = new Blob(recordedChunks, {type: 'video/webm'});
      let url = URL.createObjectURL(blob);
      let a = document.createElement('a');
      a.href = url;
      a.download = 'waveform_bars.webm';
      a.click();
      URL.revokeObjectURL(url);
    };

    mediaRecorder.start();
    recordButton.html('Stop Recording');
    recording = true;
  } else {
    // Stop recording
    mediaRecorder.stop();
    recordButton.html('Start Recording');
    recording = false;
  }
}