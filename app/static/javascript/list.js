$(document).ready(() => {
  $("[user]").click(function() {
      location.href = "chat/" + $(this).attr("user_id");
  });

  $("[group]").click(function() {
      location.href = "chat/group/" + $(this).attr("group_id");
  });

  $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  })
});



function initializeSocket(){
    socket = io.connect('https://' + location.host + '/chat');

    socket.on('connect', function() {
        socket.emit('joined');
    });

    socket.on('uiTextMessage', function(data) {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update text
          $("#" + elementId + " [last_received]").text(data.msg);

          //update unread count
          updateUnreadCount(elementId);
          updateFrom(elementId, data.group_id);

          //hide audio and image
          $("#" + elementId + " [image]").attr("src", "");
          $("#" + elementId + " img").hide();
          $("#" + elementId + " audio").hide();
          console.log(data);
    });

    socket.on('uiAudioMessage', function(data) {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update audio
          $("#" + elementId + " audio").show();
          $("#" + elementId + " [audio_source]").attr("src", data.audioPath);
          var audio = document.getElementById(elementId + '_audio')
          audio.load();

          updateUnreadCount(elementId)
          updateFrom(elementId, data.group_id);

          //hide image and text
          $("#" + elementId + " [last_received]").text("");
          $("#" + elementId + " [image]").attr("src", "");
          $("#" + elementId + " img").hide();
          console.log(data);
    });

    socket.on('uiImageMessage', data => {
          var elementId;
          if(data.group_id){
            elementId = "group_" + data.group_id;
          }
          else{
            elementId = "user_" + data.user_id;
          }

          //update image
          $("#" + elementId + " img").attr("src", data.imagePath);
          $("#" + elementId + " img").show();

          updateUnreadCount(elementId);
          updateFrom(elementId, data.group_id);

          //hide text and audio
          $("#" + elementId + " audio").hide();
          $("#" + elementId + " [last_received]").text("");
          console.log(data);
    });
}

function updateUnreadCount(elementId){
    var unread = $("#" + elementId + " [unread_count]").attr("unread_count");
    $("#" + elementId + " [unread_count]").attr("unread_count", parseInt(unread) + 1);
    $("#" + elementId + " [unread_count]").text(parseInt(unread) + 1);
}

function updateFrom(elementId, groupId){
    if(groupId){
        $("#" + elementId + " [last_received_from]").text(data.from + ": ");
    }
}


function getFromText(data){
    var fromText = data.from;
    if(data.group != null){
        fromText = data.from + ' del grupo *' + data.group + '*';
    }
    return fromText;
}
