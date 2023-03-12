const button = document.getElementById("myButton");

button.addEventListener("click", () => {
  const title = "Mon titre";
  const body = "Mon contenu";
  
  fetch("http://localhost:5000/create", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ title, body }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data) {
        console.log(data);
        title = "";
        body = "";
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.log(error);
    });
});
