console.log("✅ vehicules.js chargé")

(function () {
  "use strict";

  // -------- CSRF --------
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  const csrfToken = getCookie('csrftoken');

  const table = document.getElementById('vehicules-table');
  const toast = document.getElementById('toast');
  const btnSave = document.getElementById('btn-save');

  if (!table) return;

  // -------- helpers --------
  function snapshotRow(tr) {
    return {
      type: tr.querySelector('.type-input').value,
      archive: tr.querySelector('.archive-input').checked
    };
  }

  function setToast(msg, ok = true) {
    toast.textContent = msg;
    toast.className = 'toast ' + (ok ? 'ok' : 'err');
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 2500);
  }

  // -------- état initial --------
  const initial = new Map();
  [...table.querySelectorAll('tbody tr')].forEach(tr => {
    initial.set(tr.dataset.pk, snapshotRow(tr));
  });

  function markIfModified(tr) {
    const pk = tr.dataset.pk;
    const now = snapshotRow(tr);
    const before = initial.get(pk);
    const modified = !before || now.type !== before.type || now.archive !== before.archive;
    tr.classList.toggle('modified', modified);
  }

  table.addEventListener('input', e => {
    const tr = e.target.closest('tr');
    if (tr) markIfModified(tr);
  });

  table.addEventListener('change', e => {
    const tr = e.target.closest('tr');
    if (tr) markIfModified(tr);
  });

  // -------- sélection ligne --------
  table.addEventListener('click', e => {
    const tr = e.target.closest('tr');
    if (!tr) return;
    [...table.querySelectorAll('tbody tr')].forEach(r => r.style.outline = '');
    tr.style.outline = '2px solid #7aa7ff';
  });

  // -------- sauvegarde --------
  async function saveAll() {
    const rows = [...table.querySelectorAll('tbody tr')];
    const changed = rows.filter(tr => tr.classList.contains('modified'));

    if (changed.length === 0) {
      setToast("Aucune modification à enregistrer.");
      return;
    }

    const items = changed.map(tr => ({
      vehicule: tr.dataset.pk,
      type: tr.querySelector('.type-input').value.trim(),
      archive: tr.querySelector('.archive-input').checked
    }));

    const res = await fetch(window.VEHICULES_SAVE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({ items })
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      setToast(data.error || "Erreur lors de l'enregistrement.", false);
      return;
    }

    changed.forEach(tr => {
      initial.set(tr.dataset.pk, snapshotRow(tr));
      tr.classList.remove('modified');
    });

    setToast(`Enregistré : ${data.updated} ligne(s).`);
  }

  // -------- suppression --------
  async function deleteRow(tr) {
    const pk = tr.dataset.pk;
    if (!confirm(`Supprimer le véhicule "${pk}" ?`)) return;

    const url = window.VEHICULE_DELETE_URL.replace("___PK___", encodeURIComponent(pk));
    const res = await fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken }
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      setToast("Erreur lors de la suppression.", false);
      return;
    }

    initial.delete(pk);
    tr.remove();
    setToast("Véhicule supprimé.");
  }

  btnSave.addEventListener('click', saveAll);

  table.addEventListener('click', e => {
    if (e.target.classList.contains('btn-delete')) {
      deleteRow(e.target.closest('tr'));
    }
  });

})();
