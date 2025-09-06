const ws = new WebSocket("ws://localhost:8000/ws");
const gameImg = document.getElementById("game");
const actionDiv = document.getElementById("action");
const canvas = document.getElementById("spikes");
const ctx = canvas.getContext("2d");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  gameImg.src = "data:image/jpeg;base64," + data.frame;
  actionDiv.innerText = "Action: " + data.action;

  ctx.fillStyle = "black";
  ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle = "lime";
  data.spikes.forEach((val,i)=>{
    ctx.fillRect(i*10, 200-val*5, 8, val*5);
  });
};
