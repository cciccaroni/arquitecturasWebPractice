var recorder;


const recordAudio = () => {
  return new Promise(resolve => {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        const start = () => {
          mediaRecorder.start();
        };

        const stop = () => {
          return new Promise(resolve => {
            mediaRecorder.addEventListener("stop", () => {
              const audioBlob = new Blob(audioChunks);
              const audioUrl = URL.createObjectURL(audioBlob);
              const audio = new Audio(audioUrl);
              const play = () => {
                audio.play();
              };

              var fileReader = new FileReader();
              fileReader.readAsArrayBuffer(audioBlob);
              fileReader.onload = function () {
                var audioData = fileReader.result;
                socket.emit('audioMessage', audioData, recipients, $("#conversationId").val(), $("#loggedUserName").val());
              };

              resolve({ audioBlob, audioUrl, play });
            });

            mediaRecorder.stop();
          });
        };

        resolve({ start, stop });
      });
  });
};



function toggleRecording( e ) {
    if (e.classList.contains('recording')) {
        // stop recording
        e.classList.remove('recording');
        recording = false;
        stopRecordingAudio();
    } else {
        // start recording
        e.classList.add('recording');
        recording = true;
        startRecordingAudio();
    }
}



function startRecordingAudio(){
    (async () => {
      recorder = await recordAudio();
      recorder.start();
    })();
}


function stopRecordingAudio(){
    (async () => {
      const audio = await recorder.stop();
    })();
}

