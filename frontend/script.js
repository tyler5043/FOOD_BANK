const API = "http://127.0.0.1:8000";

// ── Cached data ──────────────────────────────────────────────────────────────
let allInventory = [];
let familyCount  = 0;
let visitorCount = 0;

// ── Helpers ──────────────────────────────────────────────────────────────────

function setApiStatus(ok) {
  const el = document.getElementById("apiStatus");
  el.textContent = ok ? "⬤ API Connected" : "⬤ API Offline";
  el.className   = "api-status " + (ok ? "ok" : "err");
}

function statusTag(status = "") {
  const s = status.toLowerCase();
  if (s.includes("ok") || s.includes("good"))    return `<span class="tag tag-ok">${status}</span>`;
  if (s.includes("low"))                          return `<span class="tag tag-low">${status}</span>`;
  if (s.includes("crit") || s.includes("empty")) return `<span class="tag tag-critical">${status}</span>`;
  return `<span class="tag tag-default">${status}</span>`;
}

function daysTag(days) {
  if (days <= 3)  return `<span class="tag tag-critical">${days}d</span>`;
  if (days <= 7)  return `<span class="tag tag-low">${days}d</span>`;
  return `<span class="tag tag-ok">${days}d</span>`;
}

// ── Page Navigation ───────────────────────────────────────────────────────────

function showPage(page) {
  document.querySelectorAll(".page").forEach(p => p.classList.add("hidden"));
  document.getElementById(page).classList.remove("hidden");

  // Highlight active nav item
  document.querySelectorAll(".nav-links li").forEach(li => li.classList.remove("active"));
  const navEl = document.getElementById("nav-" + page);
  if (navEl) navEl.classList.add("active");

  // Lazy-load heavy sections
  if (page === "predictions") loadPredictions();
  if (page === "inventory")   renderInventory(allInventory);
  if (page === "banks")       loadBanks();
}

// ── Summary Metrics ───────────────────────────────────────────────────────────

async function loadSummary() {
  try {
    const res  = await fetch(API + "/summary");
    const data = await res.json();

    document.getElementById("banks").innerText    = data.banks.toLocaleString();
    document.getElementById("expiring").innerText = data.expiring.toLocaleString();
    document.getElementById("quantity").innerText = data.quantity.toLocaleString();
    document.getElementById("people").innerText   = data.people_served.toLocaleString();

    // Remove skeleton shimmer
    ["banks","expiring","quantity","people"].forEach(id => {
      const card = document.getElementById("card-" + id);
      if (card) card.classList.remove("skeleton");
    });

    setApiStatus(true);
  } catch (err) {
    console.error("Summary error:", err);
    setApiStatus(false);
  }
}

// ── Alerts Table ──────────────────────────────────────────────────────────────

async function loadAlerts() {
  try {
    const res  = await fetch(API + "/expiring");
    const data = await res.json();

    const badge = document.getElementById("alertBadge");
    if (badge) badge.textContent = data.length + " items";

    const tbody = document.querySelector("#alerts tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:var(--muted)">No items expiring this week 🎉</td></tr>`;
      return;
    }

    data.forEach(item => {
      const tr = tbody.insertRow();
      tr.insertCell(0).innerText   = item.bank_name;
      tr.insertCell(1).innerText   = item.item_name;
      tr.cells[2].innerHTML        = daysTag(item.days_left);
      tr.insertCell(2); // placeholder — overwritten next line
      tr.cells[2].innerHTML = daysTag(item.days_left);
    });
  } catch (err) {
    console.error("Alerts error:", err);
  }
}

// ── Banks List ────────────────────────────────────────────────────────────────

async function loadBanks() {
  try {
    const res   = await fetch(API + "/banks");
    const data  = await res.json();
    const grid  = document.getElementById("banksList");
    const sel   = document.getElementById("bankSelect");

    if (grid) {
      grid.innerHTML = "";
      data.forEach(b => {
        const div = document.createElement("div");
        div.className   = "bank-card";
        div.textContent = "🏪 " + b.name;
        grid.appendChild(div);
      });
    }

    // Populate check-in select (only if still empty)
    if (sel && sel.options.length <= 1) {
      sel.innerHTML = `<option value="">— Select a food bank —</option>`;
      data.forEach(b => {
        const opt       = document.createElement("option");
        opt.value       = b.name;
        opt.textContent = b.name;
        sel.appendChild(opt);
      });
    }
  } catch (err) {
    console.error("Banks error:", err);
  }
}

// ── Inventory ─────────────────────────────────────────────────────────────────

async function loadInventory() {
  try {
    const res    = await fetch(API + "/inventory");
    allInventory = await res.json();
  } catch (err) {
    console.error("Inventory load error:", err);
  }
}

function renderInventory(data) {
  const tbody = document.querySelector("#inventoryTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--muted)">No results found.</td></tr>`;
    return;
  }

  data.forEach(r => {
    const tr = tbody.insertRow();
    tr.insertCell(0).innerText = r.bank_name  || "—";
    tr.insertCell(1).innerText = r.item_name  || "—";
    tr.insertCell(2).innerText = (r.quantity  || 0).toLocaleString();
    tr.cells[3].innerHTML      = daysTag(r.days_left || 99);
    tr.insertCell(3); // placeholder
    tr.cells[3].innerHTML = daysTag(r.days_left || 99);
    tr.cells[4].innerHTML = statusTag(r.supply_status || "");
    tr.insertCell(4); // placeholder
    tr.cells[4].innerHTML = statusTag(r.supply_status || "");
  });
}

function filterInventory() {
  const q = document.getElementById("inventorySearch").value.toLowerCase();
  const filtered = allInventory.filter(r =>
    (r.bank_name  || "").toLowerCase().includes(q) ||
    (r.item_name  || "").toLowerCase().includes(q)
  );
  renderInventory(filtered);
}

// ── Check-In ──────────────────────────────────────────────────────────────────

function checkin() {
  const bank = document.getElementById("bankSelect").value;
  const size = parseInt(document.getElementById("familySize").value) || 0;

  if (!bank) { alert("Please select a food bank."); return; }
  if (size < 1) { alert("Please enter a valid family size."); return; }

  familyCount  += 1;
  visitorCount += size;

  document.getElementById("familyCount").innerText  = familyCount;
  document.getElementById("visitorCount").innerText = visitorCount;

  // Visual feedback
  const btn = document.querySelector("#checkin .btn-primary");
  btn.textContent = "✔ Checked In!";
  btn.style.background = "#22c55e";
  setTimeout(() => {
    btn.textContent      = "✅ Check In Family";
    btn.style.background = "";
  }, 1600);
}

// ── Network Search ────────────────────────────────────────────────────────────

async function searchItem() {
  const q = document.getElementById("itemSearch").value.toLowerCase().trim();
  if (!q) return;

  // Use cached inventory if available, else fetch
  const data = allInventory.length ? allInventory : await (await fetch(API + "/inventory")).json();

  const results = data.filter(x =>
    (x.item_name || "").toLowerCase().includes(q)
  );

  const tbody = document.querySelector("#networkTable tbody");
  tbody.innerHTML = "";

  if (results.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--muted)">No matches for "${q}"</td></tr>`;
    return;
  }

  results.forEach(r => {
    const tr = tbody.insertRow();
    tr.insertCell(0).innerText = r.bank_name  || "—";
    tr.insertCell(1).innerText = r.item_name  || "—";
    tr.insertCell(2).innerText = (r.quantity  || 0).toLocaleString();
    tr.cells[3].innerHTML      = statusTag(r.supply_status || "");
    tr.insertCell(3); // placeholder
    tr.cells[3].innerHTML = statusTag(r.supply_status || "");
  });
}

// Allow pressing Enter in search
document.addEventListener("DOMContentLoaded", () => {
  const inp = document.getElementById("itemSearch");
  if (inp) inp.addEventListener("keydown", e => { if (e.key === "Enter") searchItem(); });
  const inv = document.getElementById("inventorySearch");
  if (inv) inv.addEventListener("input", filterInventory);
});

// ── Predictions Chart ─────────────────────────────────────────────────────────

async function loadPredictions() {
  const chartDiv = document.getElementById("chart");
  if (!chartDiv || chartDiv.dataset.loaded) return;

  try {
    const res  = await fetch(API + "/predictions");
    const data = await res.json();

    const banks    = data.map(d => d.bank_name);
    const supply   = data.map(d => d.total_quantity);
    const demand   = data.map(d => d.total_demand);

    Plotly.newPlot("chart", [
      {
        name: "Supply (Qty)",
        x: banks, y: supply,
        type: "bar",
        marker: { color: "#0e7c6e" }
      },
      {
        name: "Daily Demand",
        x: banks, y: demand,
        type: "bar",
        marker: { color: "#f59e0b" }
      }
    ], {
      barmode: "group",
      font: { family: "DM Sans, sans-serif", color: "#1a2740" },
      plot_bgcolor:  "transparent",
      paper_bgcolor: "transparent",
      legend: { orientation: "h", y: -0.25 },
      margin: { t: 20, b: 80, l: 60, r: 20 },
      xaxis: { tickangle: -30 },
      yaxis: { title: "Units" }
    }, { responsive: true, displayModeBar: false });

    chartDiv.dataset.loaded = "true";
  } catch (err) {
    console.error("Predictions error:", err);
    document.getElementById("chart").innerHTML =
      `<p style="color:var(--muted);text-align:center;padding:40px">Could not load predictions — is the API running?</p>`;
  }
}

// ── Boot ──────────────────────────────────────────────────────────────────────

window.onload = async function () {
  await Promise.all([
    loadSummary(),
    loadAlerts(),
    loadInventory(),
    loadBanks(),
  ]);
};