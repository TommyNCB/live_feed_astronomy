// JavaScript code for real-time video streaming
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

// Initialize Socket.io
const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

// Get user media (camera)
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        remoteVideo.srcObject = stream;
        localVideo.srcObject = stream;
        // Emit the stream to the server
        socket.emit('join', { room: 'default' });
    })
    .catch(error => console.error('Error accessing camera:', error));

// Receive and display remote video
socket.on('stream', data => {
    localVideo.srcObject = data.stream;
});
