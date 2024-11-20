// script.js
const video = document.getElementById('video');
const overlay = document.getElementById('overlay');
const startButton = document.getElementById('start-button');
const dashboard = document.getElementById('dashboard');
const faceRecognitionSection = document.getElementById('face-recognition');

// Load face-api models
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
  faceapi.nets.ssdMobilenetv1.loadFromUri('/models')
]).then(startVideo);

// Start webcam feed
function startVideo() {
  navigator.mediaDevices
    .getUserMedia({ video: {} })
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => console.error('Erro ao acessar a webcam:', err));
}

// Face detection
video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.querySelector('.video-container').append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceDescriptors();
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

    if (detections.length > 0) {
      authenticateUser();
    }
  }, 100);
});

// Authenticate user
function authenticateUser() {
  alert('Usuário reconhecido com sucesso!');
  faceRecognitionSection.classList.add('hidden');
  dashboard.classList.remove('hidden');
}