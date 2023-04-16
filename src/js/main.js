var ws = new WebSocket("ws://localhost:8000/ws");

function clearData(){
    const form = document.getElementById("loginPrompt");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      // Reset the form
      form.reset();
    });
}