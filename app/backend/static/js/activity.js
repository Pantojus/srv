fetch("/health/activity/today")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("activity");

    if (data.message) {
      container.innerHTML = `<p>${data.message}</p>`;
      return;
    }

    let html = "";

    if (data.strength && data.strength.length > 0) {
      html += "<h2>Fuerza</h2>";

      data.strength.forEach(group => {
        html += `<h3>${group.group}</h3><ul class="exercise-list">`;

        group.exercises.forEach(ex => {
          html += `
            <li>
              <span
                class="exercise-item"
                data-exercise-id="${ex.id}">
                ${ex.name}
              </span>
            </li>
          `;
        });

        html += "</ul>";
      });
    }

    container.innerHTML = html;
    attachExerciseClickHandlers();
  })
  .catch(err => {
    console.error(err);
    document.getElementById("activity").innerHTML =
      "<p>Error cargando la actividad</p>";
  });


// =======================================================
// CLICK EN EJERCICIO
// =======================================================

function attachExerciseClickHandlers() {
  document.querySelectorAll(".exercise-item").forEach(item => {
    item.addEventListener("click", () => {
      const exerciseId = item.dataset.exerciseId;
      const parentLi = item.closest("li");
      const next = parentLi.nextElementSibling;

      if (next && next.classList.contains("exercise-detail")) {
        next.remove();
        return;
      }

      document
        .querySelectorAll(".exercise-detail")
        .forEach(el => el.remove());

      const detailDiv = document.createElement("div");
      detailDiv.className = "exercise-detail";
      detailDiv.innerHTML = "<p>Cargando...</p>";
      parentLi.after(detailDiv);

      fetch(`/health/api/exercise/${exerciseId}`)
        .then(res => res.json())
        .then(data => {
          detailDiv.innerHTML = renderExerciseDetail(data);
          requestAnimationFrame(() => {
            detailDiv.classList.add("open");
          });
        })
        .catch(err => {
          console.error(err);
          detailDiv.innerHTML =
            "<p>Error cargando el detalle del ejercicio</p>";
        });
    });
  });
}


// =======================================================
// RENDER DESPLEGABLE
// =======================================================

function renderExerciseDetail(data) {
  return `
    <div class="exercise-box">
      <div class="exercise-box-header">
        <button class="close-btn"
          onclick="this.closest('.exercise-detail').remove()">✕</button>
      </div>

      <h4>Series de calentamiento</h4>
      ${renderWarmupSet(data.warmup_sets)}

      <h4>Series efectivas</h4>
      ${renderEffectiveSets(data.effective_sets)}

      <div class="exercise-actions">
        <button class="save-btn" disabled>Guardar</button>
      </div>
    </div>
  `;
}


// =======================================================
// CALENTAMIENTO (1 serie)
// =======================================================

function renderWarmupSet(warmupSets) {
  const reps = warmupSets[0]?.reps ?? "";
  const weight = warmupSets[0]?.weight ?? "";

  return `
    <table class="sets-table">
      <tr>
        <th>Serie</th>
        <th>Reps</th>
        <th>Peso (kg)</th>
      </tr>
      <tr>
        <td>1</td>
        <td><input type="number" min="1" step="1" value="${reps}"></td>
        <td><input type="number" min="0" step="0.5" value="${weight}"></td>
      </tr>
    </table>
  `;
}


// =======================================================
// SERIES EFECTIVAS
// =======================================================

function renderEffectiveSets(sets) {
  let rows = "";

  if (!sets || sets.length === 0) {
    rows += renderEffectiveRow(1);
  } else {
    sets.forEach((s, i) => {
      rows += renderEffectiveRow(i + 1, s.reps, s.weight);
    });
  }

  return `
    <table class="sets-table effective-sets">
      <tr>
        <th>Serie</th>
        <th>Reps</th>
        <th>Peso (kg)</th>
        <th></th>
      </tr>
      ${rows}
    </table>

    <button class="add-set-btn"
      onclick="addEffectiveSet(this)">
      ➕ Añadir serie
    </button>
  `;
}

function renderEffectiveRow(order, reps = "", weight = "") {
  return `
    <tr>
      <td>${order}</td>
      <td><input type="number" min="1" step="1" value="${reps}"></td>
      <td><input type="number" min="0" step="0.5" value="${weight}"></td>
      <td>
        <button class="remove-set-btn"
          onclick="removeEffectiveSet(this)">➖</button>
      </td>
    </tr>
  `;
}

function addEffectiveSet(button) {
  const table = button.previousElementSibling;
  const rowCount = table.querySelectorAll("tr").length - 1;
  table.insertAdjacentHTML(
    "beforeend",
    renderEffectiveRow(rowCount + 1)
  );
}

function removeEffectiveSet(button) {
  const table = button.closest("table");
  const rows = table.querySelectorAll("tr");

  if (rows.length <= 2) return; // cabecera + 1 fila mínima

  button.closest("tr").remove();

  // Reordenar numeración
  table.querySelectorAll("tr").forEach((row, i) => {
    if (i === 0) return;
    row.children[0].textContent = i;
  });
}
