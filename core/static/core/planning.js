(function () {
  const dateInput = document.getElementById("dateInput");
  const resetBtn = document.getElementById("resetBtn");
  const head = document.getElementById("planningHead");
  const body = document.getElementById("planningBody");
  const table = document.getElementById("planningTable");

  const agents = JSON.parse(
    document.getElementById("agents-data")?.textContent || "[]"
  );

  const weekday = ["dim", "lun", "mar", "mer", "jeu", "ven", "sam"];

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function toISODate(d) {
    return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;
  }

  function getMonthDays(year, monthIndex) {
    const first = new Date(year, monthIndex, 1);
    const days = [];
    const d = new Date(first);

    while (d.getMonth() === monthIndex) {
      days.push(new Date(d));
      d.setDate(d.getDate() + 1);
    }
    return days;
  }

  function renderTableFromDate(isoDate) {
    if (!isoDate) return;

    const selected = new Date(isoDate + "T00:00:00");
    const year = selected.getFullYear();
    const monthIndex = selected.getMonth();
    const days = getMonthDays(year, monthIndex);

    // ===== THEAD =====
    head.innerHTML = "";
    const trh = document.createElement("tr");

    const thQualif = document.createElement("th");
    thQualif.textContent = "Qualification";
    thQualif.className = "planning__sticky planning__sticky--qualif";
    trh.appendChild(thQualif);

    const thNom = document.createElement("th");
    thNom.textContent = "Nom";
    thNom.className = "planning__sticky planning__sticky--nom";
    trh.appendChild(thNom);

    days.forEach((d) => {
      const th = document.createElement("th");
      th.innerHTML = `${weekday[d.getDay()]}<br>${d.getDate()}`;
      trh.appendChild(th);
    });

    head.appendChild(trh);

    // ===== TBODY =====
    body.innerHTML = "";

    agents.forEach((a) => {
      const tr = document.createElement("tr");

      const tdQ = document.createElement("td");
      tdQ.className = "planning__sticky planning__sticky--qualif";
      tdQ.textContent = a.qualification ?? "";
      tr.appendChild(tdQ);

      const tdN = document.createElement("td");
      tdN.className = "planning__sticky planning__sticky--nom";
      tdN.textContent = a.nom ?? "";
      tr.appendChild(tdN);

      days.forEach((d) => {
        const td = document.createElement("td");
        td.className = "planning__cell";
        td.dataset.agentId = a.id;
        td.dataset.agentName = a.nom ?? "";
        td.dataset.date = toISODate(d);
        td.textContent = "";
        tr.appendChild(td);
      });

      body.appendChild(tr);
    });
  }

  // ===== Modal logic =====
  const modal = document.getElementById("planningModal");
  const form = document.getElementById("planningForm");
  const pfAgent = document.getElementById("pfAgent");
  const pfDate = document.getElementById("pfDate");
  const pfValue = document.getElementById("pfValue");

  let activeCell = null;

  function openModal({ agentName, date, value }) {
    pfAgent.value = agentName || "";
    pfDate.value = date || "";
    pfValue.value = value || "";
    modal.setAttribute("aria-hidden", "false");
    pfValue.focus();
  }

  function closeModal() {
    modal.setAttribute("aria-hidden", "true");
    activeCell = null;
  }

  function onTableClick(e) {
    const cell = e.target.closest("td.planning__cell");
    if (!cell) return;

    activeCell = cell;
    openModal({
      agentName: cell.dataset.agentName,
      date: cell.dataset.date,
      value: cell.textContent.trim(),
    });
  }

  // fermeture (boutons + backdrop)
  modal.addEventListener("click", (e) => {
    if (e.target?.dataset?.close) closeModal();
  });

  // ESC pour fermer
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.getAttribute("aria-hidden") === "false") {
      closeModal();
    }
  });

  // submit => met à jour la cellule (front)
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!activeCell) return;

    activeCell.textContent = pfValue.value.trim();
    closeModal();
  });

  function init() {
    const today = new Date();
    dateInput.value = toISODate(today);

    renderTableFromDate(dateInput.value);

    dateInput.addEventListener("change", () => {
      renderTableFromDate(dateInput.value);
    });

    resetBtn.addEventListener("click", () => {
      dateInput.value = toISODate(new Date());
      renderTableFromDate(dateInput.value);
    });

    // ✅ indispensable : click sur la table
    table.addEventListener("click", onTableClick);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
