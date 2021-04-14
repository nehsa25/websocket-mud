var socket;

$(document).ready(function () {
  var host = "127.0.0.1";
  var port = 1234;
  var full_address = "ws://" + host + ":" + port + "/"

  // Focus on the command bar
  $("#command").focus();

  var input = document.getElementById("command");
  input.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
          event.preventDefault();
          document.getElementById("submit_btn").click();
      }
  });

  console.log("Setting up websockect connection at " + full_address)
  // configure_websocket(host, port);
  socket = new WebSocket(full_address);

  //Connection opened
  socket.addEventListener('open', function(event) {
    console.log("Connected to server");
  });

  //Listen to messages
  socket.addEventListener('message', function(event) {    
    var data = JSON.parse(event.data);
    switch (data.type) {        
    case 'request_hostname':
      console.log("Inside request_hostname switch");
      var resp = '{"type": "hostname_answer", "host": "' + "webclient_" + new Date().getTime() + '"}'
      console.log("Server is requesting our name, sending back: " + resp);      
      socket.send(resp);
      break;
    case 'room':
      console.log("Inside room switch");
      msg = $("#messages").html() + "";

      // check if there's any response text
      if (data.top_response != "") {
        msg += "<span style=\"color: darksalmon; font-style: italic; font-weight: bold;\">" + data.top_response + "</span><br>";
      }

      // there will always be a room name + description
      msg += "<br><span style=\"color: yellow;\">[" + data.name + "]</span>";
      msg += "<br><span style=\"color: antiquewhite;\">" + data.description + "</span>";

      // check for monsters
      if (data.monsters != "") {
        msg += "<br><span style=\"color: antiquewhite;\">Monsters: </span><span style=\"color: red;\">" + data.monsters + "</span>";
      }

      // check for items
      if (data.items != "") {
        msg += "<br><span style=\"color: antiquewhite;\">You see </span><span style=\"color: green;\">" + data.items + "</span>";
      }

      // check for available exits
      if (data.exits != "") {
        msg += "<br><span style=\"color: antiquewhite;\">Available exits: </span><span style=\"color: green;\">" + data.exits + "</span><br><br>";
      }

      // check if there's any response text
      if (data.bottom_response != "") {
        msg += "<span style=\"color: darksalmon; font-style: italic; font-weight: bold;\">" + data.bottom_response + "</span><br>";
      }
      unescape(msg);
      
      $("#messages").html(msg);
      
      // place us at bottom of div
      scrollSmoothToBottom("messages");

      // clear command
      $("#command").val("");
      break
    case 'get_clients':
      console.log("Inside get_clients switch");
      $("#users_connected").text(data.value + " users connected.");
    default:
      console.error("unsupported event", JSON.stringify(event));
    }
  });
});

function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $('#' + id).animate({
     scrollTop: div.scrollHeight - div.clientHeight
  }, 250);
}

function resetfocus() {
  $("#command").focus();
}

function isOpen(ws) { return ws.readyState === ws.OPEN }

function send_command() {
  var cmd = $('#command').val();
  
  if (isOpen(socket)) {
    var full_cmd = {
      "type": "cmd", 
      "cmd": cmd
    };
    console.log("Sending: " + cmd);
    console.log(full_cmd);
    socket.send(JSON.stringify(full_cmd));
  } else {
    console.log("Websocket is closed..");
  }  
}
