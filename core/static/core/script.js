/* =========================
   Base + Design tokens
========================= */
:root{
  --bg: #0b1220;
  --panel: rgba(255,255,255,0.06);
  --card: rgba(255,255,255,0.08);
  --stroke: rgba(255,255,255,0.12);
  --stroke-2: rgba(255,255,255,0.18);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.70);
  --shadow: 0 10px 30px rgba(0,0,0,0.35);
  --radius: 16px;
  --radius-sm: 12px;

  --focus: rgba(255,255,255,0.25);

  /* Catégories */
  --en:   #9e9e9e;
  --cr:   #1b5e20;
  --ch:   #4caf50;
  --rr:   #0d47a1;
  --rh:   #2196f3;
  --prer: #ff9800;
  --pror: #f9a825;
  --proh: #ffeb3b;
}

* { box-sizing: border-box; }
html, body { height: 100%; }

body{
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Apple Color Emoji", "Segoe UI Emoji";
  color: var(--text);
  background:
    radial-gradient(1200px 700px at 10% 10%, rgba(33,150,243,0.22), transparent 60%),
    radial-gradient(900px 600px at 90% 20%, rgba(255,152,0,0.18), transparent 55%),
    radial-gradient(900px 600px at 40% 90%, rgba(76,175,80,0.16), transparent 55%),
    var(--bg);
}

/* =========================
   Header
========================= */
.app-header{
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(12px);
  background: rgba(11,18,32,0.65);
  border-bottom: 1px solid var(--stroke);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.app-title{
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-title__logo{
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: rgba(255,255,255,0.10);
  border: 1px solid var(--stroke);
  box-shadow: var(--shadow);
}

.app-header h1{
  margin: 0;
  font-size: 18px;
  line-height: 1.1;
}
.app-header p{
  margin: 2px 0 0;
  color: var(--muted);
  font-size: 12px;
}

/* =========================
   Controls
========================= */
.controls{
  display: flex;
  align-items: end;
  gap: 10px;
  flex-wrap: wrap;
}
.control{
  display: grid;
  gap: 6px;
}
.control span{
  font-size: 12px;
  color: var(--muted);
}
input[type="date"]{
  background: rgba(255,255,255,0.08);
  border: 1px solid var(--stroke);
  color: var(--text);
  padding: 10px 12px;
  border-radius: 12px;
  outline: none;
}
input[type="date"]:focus{
  border-color: var(--stroke-2);
  box-shadow: 0 0 0 4px var(--focus);
}

/* =========================
   Buttons
========================= */
.btn{
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,0.10);
  color: var(--text);
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 650;
  letter-spacing: 0.2px;
  transition: transform .08s ease, background .15s ease, border-color .15s ease;
}
.btn:hover{ background: rgba(255,255,255,0.14); border-color: var(--stroke-2); }
.btn:active{ transform: translateY(1px); }
.btn:focus{ outline: none; box-shadow: 0 0 0 4px var(--focus); }

.btn--ghost{
  background: rgba(255,255,255,0.06);
}

/* =========================
   Layout
========================= */
.layout{
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 16px;
  padding: 16px;
  align-items: start;
}

@media (max-width: 980px){
  .layout{ grid-template-columns: 1fr; }
}

/* =========================
   Panel + Zones
========================= */
.panel{
  border: 1px solid var(--stroke);
  background: var(--panel);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.panel__head{
  padding: 14px 14px 10px;
  border-bottom: 1px solid var(--stroke);
}
.panel__head h2{
  margin: 0;
  font-size: 15px;
}
.muted{ color: var(--muted); font-size: 12px; margin: 4px 0 0; }

.zones{
  padding: 12px;
  display: grid;
  gap: 10px;
}

.zone{
  border: 1px solid var(--stroke);
  border-radius: 14px;
  overflow: hidden;
  background: rgba(0,0,0,0.10);
}
.zone__header{
  padding: 10px 12px;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.3px;
  border-bottom: 1px solid var(--stroke);
  background: rgba(255,255,255,0.04);
}
.zone__body{
  min-height: 44px;
  padding: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

/* =========================
   People pills
========================= */
.person-btn{
  border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.10);
  color: var(--text);
  padding: 7px 10px;
  border-radius: 999px;
  cursor: grab;
  font-weight: 700;
  font-size: 12px;
  user-select: none;
  transition: transform .08s ease, filter .15s ease, background .15s ease;
}
.person-btn:hover{ background: rgba(255,255,255,0.14); }
.person-btn:active{ cursor: grabbing; transform: translateY(1px); }
.person-btn:focus{ outline: none; box-shadow: 0 0 0 4px var(--focus); }

.person-btn.en   { background: color-mix(in srgb, var(--en) 35%, rgba(255,255,255,0.10)); }
.person-btn.cr   { background: color-mix(in srgb, var(--cr) 40%, rgba(255,255,255,0.10)); }
.person-btn.ch   { background: color-mix(in srgb, var(--ch) 40%, rgba(255,255,255,0.10)); }
.person-btn.rr   { background: color-mix(in srgb, var(--rr) 40%, rgba(255,255,255,0.10)); }
.person-btn.rh   { background: color-mix(in srgb, var(--rh) 40%, rgba(255,255,255,0.10)); }
.person-btn.prer { background: color-mix(in srgb, var(--prer) 45%, rgba(255,255,255,0.10)); }
.person-btn.pror { background: color-mix(in srgb, var(--pror) 45%, rgba(255,255,255,0.10)); color: #121212; }
.person-btn.proh { background: color-mix(in srgb, var(--proh) 60%, rgba(255,255,255,0.10)); color: #121212; }

/* =========================
   Dropzone feedback
========================= */
.dropzone{
  transition: box-shadow .15s ease, background .15s ease;
  border-radius: 12px;
}
.dropzone.drag-over{
  box-shadow: 0 0 0 4px rgba(255,255,255,0.14) inset, 0 0 0 2px rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.06);
}

/* =========================
   Content / Table
========================= */
.content{
  display: grid;
  gap: 12px;
}

.card{
  border: 1px solid var(--stroke);
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.card__head{
  padding: 14px 14px 10px;
  border-bottom: 1px solid var(--stroke);
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 10px;
}
.card__head h2{ margin: 0; font-size: 15px; }

.table-wrap{
  overflow: auto;
  max-height: calc(100vh - 190px);
}

table{
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 860px;
  font-size: 12px;
}

thead th{
  position: sticky;
  top: 0;
  background: rgba(11,18,32,0.92);
  border-bottom: 1px solid var(--stroke);
  z-index: 2;
}

th, td{
  padding: 10px 8px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  text-align: center;
  vertical-align: middle;
}

tbody tr:hover td{
  background: rgba(255,255,255,0.04);
}

td[contenteditable="true"]{
  outline: none;
  border-radius: 10px;
}
td[contenteditable="true"]:focus{
  box-shadow: 0 0 0 4px var(--focus);
}

select, input[type="time"]{
  width: 100%;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.06);
  color: var(--text);
  padding: 8px;
  outline: none;
}
select:focus, input[type="time"]:focus{
  box-shadow: 0 0 0 4px var(--focus);
  border-color: rgba(255,255,255,0.20);
}

/* Flux colors (fond cellule) */
.flux-OM { background: rgba(158,158,158,0.35); }
.flux-OMBIO { background: rgba(109,143,106,0.35); }
.flux-EMB { background: rgba(251,192,45,0.30); }
.flux-DV { background: rgba(123,30,60,0.35); }
.flux-SACORANGE { background: rgba(255,152,0,0.35); }
.flux-PRECOLLECTE { background: rgba(33,150,243,0.30); }
.flux-PROPRETEPAV { background: rgba(13,71,161,0.35); }
.flux-LAVAGEBOM { background: rgba(142,36,170,0.35); }
.flux-VERRE { background: rgba(207,216,220,0.28); color: rgba(255,255,255,0.92); }

.footer{
  padding: 0 4px 12px;
}


/* styles.css (ajouts / remplacements DnD) */

.person-btn.is-dragging{
  opacity: 0.55;
  transform: scale(0.98);
  filter: saturate(0.85);
}

.dropzone{
  transition: box-shadow .15s ease, background .15s ease, outline-color .15s ease;
  border-radius: 12px;
}

.dropzone.drag-over{
  box-shadow: 0 0 0 4px rgba(255,255,255,0.14) inset, 0 0 0 2px rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.06);
}

.dnd-placeholder{
  display: inline-block;
  width: 54px;
  height: 28px;
  border-radius: 999px;
  border: 1px dashed rgba(255,255,255,0.22);
  background: rgba(255,255,255,0.04);
}