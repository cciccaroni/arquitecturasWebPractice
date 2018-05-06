$(document).ready(() => {
  $("[user]").click(function() {
      location.href = "chat/" + this.id;
  });

  $("[group]").click(function() {
      location.href = "chat/group/" + this.id;
  });



  $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  })
});


/* previously
  let socket;
  let conversation = []
  $(document).ready(() => {
      socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
      socket.on('connect', () => {
          socket.emit('joined', {});
      });

      socket.on('message', data => {
          var userId = data.from.id;
          $("#" + userId + " [last_received]").text(data.msg);
          var unread = $("#" + userId + " [unread_count]").attr("unread_count");
          $("#" + userId + " [unread_count]").attr("unread_count", parseInt(unread) + 1);
          $("#" + userId + " [unread_count]").text(parseInt(unread) + 1);
          $("#" + userId + " [image]").attr("src", "");
          $("#" + userId + " [image]").hide()
          console.log(data)
      });

      socket.on('image', data => {
          var arrayBuffer = data.msg;
          var bytes = new Uint8Array(arrayBuffer);
          var userId = data.from.id;
          $("#" + userId + " [image]").attr("src", 'data:image/png;base64,'+encode(bytes));
          var unread = $("#" + userId + " [unread_count]").attr("unread_count");
          $("#" + userId + " [unread_count]").attr("unread_count", parseInt(unread) + 1);
          $("#" + userId + " [unread_count]").text(parseInt(unread) + 1);
            $("#" + userId + " [last_received]").text("");
      });

      socket.on('status', data => {
          console.log(data.msg)
          if (data.msg.status !== 'ENTERED') return;
          if ($(`#${data.msg.id}`) !== undefined) return;
          let newUser = `list-group-item list-group-item-action" id={{actual_user.id}} data-toggle="list" `
                      + `href='#_${data.msg.id} role="tab" aria-controls=${data.msg.name}>${data.msg.name}</a>`
          $('.list-group-item-action').last().append(newUser)
      });

      $("[user]").click(function() {
          //location.href = "chat/" + this.id;
          conversation = [this.id];
          $("#conversation").text(this.id)
      });

      $("#send").click(() => {
          msg = $("#msg").val()
          if (msg !== '')
            socket.emit('textMessage', msg, conversation);
      });

      $("#logout").click(() => {
          console.log('log out')
          socket.emit('left', {}, () => {
              socket.disconnect();
              window.location.href = "{{ url_for('auth.signin') }}";
          });
      });

      $('#myTabs a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
      })

      $("#file").on("change", function (e) {
          var file = $(this)[0].files[0];
          var fileReader = new FileReader();
          if (file) {
              fileReader.readAsArrayBuffer(file);
              fileReader.onload = function () {
                  var imageData = fileReader.result;
                  socket.emit('imageMessage', imageData, conversation);
              };
          }
      });

      function encode (input) {
          var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
          var output = "";
          var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
          var i = 0;

          while (i < input.length) {
              chr1 = input[i++];
              chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
              chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

              enc1 = chr1 >> 2;
              enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
              enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
              enc4 = chr3 & 63;

              if (isNaN(chr2)) {
                  enc3 = enc4 = 64;
              } else if (isNaN(chr3)) {
                  enc4 = 64;
              }
              output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                        keyStr.charAt(enc3) + keyStr.charAt(enc4);
          }
          return output;
      }

  });
*/