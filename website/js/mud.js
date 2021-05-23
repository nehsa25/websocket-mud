var socket;

$(document).ready(function () {
  var host = "208.52.52.157";
  var port = 81;
  var full_address = "ws://" + host + ":" + port + "/"

  $("#formdiv").hide();

  // Focus on the command bar
  $("#command").focus();

  var input = document.getElementById("command");
  input.addEventListener("keyup", function(event) {
      if (event.keyCode === 13) {
          event.preventDefault();
          document.getElementById("submit_btn").click();
      }
  });

  console.log("Setting up websocket connection at " + full_address)
  // configure_websocket(host, port);
  socket = new WebSocket(full_address);

  //Connection opened
  socket.addEventListener('open', function(event) {
    console.log("Connected to server");
  });

  //Listen to messages
  socket.addEventListener('message', function(event) {    
    var data = JSON.parse(event.data);

    // get the previous html and trim as necessary
    msg = trimHtml();

    // process the command
    msg = processCommand(data, msg)

    // unescape
    unescape(msg);
      
    // set the new HTML
    //$("#messages").html(msg);
    document.getElementById('messages').innerHTML = msg;
    
    // place us at bottom of div
    scrollSmoothToBottom("messages_wrapper");
  });
});

function processCommand(data, msg) {
  switch (data.type) {        
    case 'request_hostname':
      console.log("Inside request_hostname switch");
      names = ['Crossen', 'Bink', 'Ashen', 'Renkath', 'Kelsek', 'Ash', 'Jay', 'Bob', 'Fred', 'Mike', 'James', 'Jones', 'Tim']
      var name = names[Math.floor(Math.random() * names.length)];
      var resp = '{"type": "hostname_answer", "host": "' + name + '"}';
      console.log("Server is requesting our name, sending back: " + resp);      
      socket.send(resp);
      break;
    case 'event': // check if there's an event # breeze, silence, rain
      if (data.message != "") {
        msg += "<br><span style=\"color: yellow;\">" + data.message + "</span>";
      }
      break;
    case 'info': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: darksalmon;\">" + data.message + "</span>";
      }
      break;
      case 'command': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">" + data.message + "</span>";
      }
      break;
    case 'you_attack': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: #98FB98;\">" + data.message + "</span>";
      }
      break;
    case 'error': // check if there's an info event      
      if (data.message != "") {
        msg += "<br><span style=\"color: red;\">" + data.message + "</span>";
      }
      break;
    case 'attack': // check if there's an attack event
      if (data.message != "") {
        attack_txt = data.message.split('! ')
        msg += "<br><span style=\"color: red;\">" + attack_txt[0] + "!</span><br><span style=\"font-size: 1rem; vertical-align: super; color: #cccccc;\">" + attack_txt[1] + "</span>";
      }
      break;
    case 'health': // check if there's an health event
      if (data.message != "") {

        hitpoints = parseInt(data.message.split('/')[0]);
        max_hitpoints = parseInt(data.message.split('/')[1]);
        
        if (hitpoints / max_hitpoints >= .75) {
          color = 'green';
        } else if (hitpoints / max_hitpoints >= .25) {
          color = '#FF7034;'; // burnt orange
        } else {
          color = 'red';
        }

        var health_msg = "Health: <span style=\"color: " + color + ";\">" + hitpoints + "</span> / " + max_hitpoints;
        $('#health').html(health_msg);
      }
      break;
    case 'room': // check if there's a room name
      if (data.name != "") {
        msg += "<br><span style=\"color: green; text-weight: bold;\">" + data.name + "</span>";
      }

      // check if there's a room descrption
      if (data.description != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">" + data.description + "</span>";
      }

      // check for people
      if (data.people != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">People: </span><span style=\"color: antiquewhite;\">" + data.people + "</span>";
      }

      // check for monsters
      if (data.monsters != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">Monsters: </span><span style=\"color: red;\">" + data.monsters + "</span>";
      }

      // check for items
      if (data.items != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">You see </span><span style=\"color: green;\">" + data.items + "</span>";
      }

      // check for available exits
      if (data.exits != "") {
        msg += "<br><span style=\"color: #F9F5EC;\">Available exits: </span><span style=\"color: green;\">" + data.exits + "</span>";
      }
      break;
    case 'get_clients':
      console.log("Inside get_clients switch");
      $("#users_connected").text(data.value + " users connected.");
      break;
    default:
      console.error("unsupported event", JSON.stringify(event));
      break;
    }

    return msg;
}

function trimHtml() {
  msg = $("#messages").html() + "";
  lines = msg.split('<br>');
  if (lines.length > 100) {
    msg = lines.slice(Math.max(lines.length - 100, 0)).join('<br>')
  }
  
  return msg;
}

function scrollSmoothToBottom(id) {
  var div = document.getElementById(id);
  $('#' + id).animate({
     scrollTop: div.scrollHeight - div.clientHeight
  }, 50);
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
    
    // clear command
    $("#command").val("");
  } else {
    console.log("Websocket is closed..");
  }  
}
