function messageHandler(message) {
    // Get the snackbar DIV
    var x = document.getElementById("toaster");
  
    var ele = document.createElement('div')
    const ele_id = `toast${Math.random()}`
    ele.id = ele_id
    ele.innerHTML = message

    ele.className = "show";

    x.appendChild(ele)
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(() => {
        ele.className = ele.className.replace("show", "");
        ele.remove()
    }, 5000);
}

const roomName = 'lobby';
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    messageHandler(data.message);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// setInterval(() => {
//     chatSocket.send(JSON.stringify({
//         'message': `Message: ${Math.random()}`
//     }));
// }, 2000);
