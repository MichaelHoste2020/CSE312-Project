function clearData(){
    const form = document.getElementById("loginPrompt");
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      // Reset the form
      form.reset();
    });
}