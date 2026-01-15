fetch("/health/activity/today")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("activity");

    if (data.message) {
      container.innerHTML = `<p>${data.message}</p>`;
      return;
    }

    let html = "";

    // CARDIO
    if (data.cardio && data.cardio.length > 0) {
      html += "<h2>Cardio</h2><ul>";
      data.cardio.forEach(c => {
        html += `<li>${c.type} – ${c.duration_minutes} min</li>`;
      });
      html += "</ul>";
    }

    // FUERZA
    if (data.strength && data.strength.length > 0) {
      html += "<h2>Fuerza</h2>";

      data.strength.forEach(group => {
        html += `<h3>${group.group}</h3><ul>`;

        group.exercises.forEach(ex => {
          html += `<li>${ex}</li>`;
        });

        html += "</ul>";
      });
    }

    container.innerHTML = html;
  })
  .catch(err => {
    console.error(err);
    document.getElementById("activity").innerHTML =
      "<p>Error cargando la actividad</p>";
  });
