async function init() {
    const path = window.location.pathname;
    if (path.startsWith("/unknown/")) {
        const id = path.split("/")[2];
        renderDetail(id);
    } else {
        renderOverview();
    }
}

window.addEventListener("popstate", init);

function openDetail(id) {
    history.pushState({}, "", `/unknown/${id}`);
    renderDetail(id);
}

function goHome() {
    history.pushState({}, "", `/`);
    renderOverview();
}

function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

function highlightLedger(text) {
    const escaped = escapeHtml(text);
    return escaped
        .replace(/^(\d{4}\/\d{2}\/\d{2})/gm, '<span class="token-date">$1</span>')
        .replace(/(Assets|Income|Expenses|Liabilities|Equity):[A-Za-z0-9:_-]+/g, '<span class="token-account">$&</span>')
        .replace(/(-?\d+[.,]?\d*\s?(EUR|USD|GBP|CHF))/g, '<span class="token-amount">$1</span>');
}

async function renderOverview() {
    const res = await fetch("/api/state");
    const data = await res.json();
    const app = document.getElementById("app");

    const cards = data.unknown.map(t => {
        const preview = t.ledger || "";
        return `
            <div class="tx-card" onclick="openDetail('${t.id}')" role="button" tabindex="0">
                <div class="tx-meta">
                    <span class="tx-id">${escapeHtml(t.id)}</span>
                    <span class="tx-date">${escapeHtml(t.date || "")}</span>
                </div>
                <pre class="ledger-preview">${highlightLedger(preview)}</pre>
            </div>
        `;
    }).join("");

    app.innerHTML = `
        <div class="page">
            <header class="topbar">
                <h1>Unknown Transactions</h1>
                <p>${data.unknown.length} item(s) waiting for review</p>
                <button class="btn tiny" onclick="location.reload()">Refresh</button>
            </header>
            <main class="feed">
                ${cards || '<div class="empty">No unknown transactions.</div>'}
            </main>
        </div>
    `;
    }

async function renderDetail(id) {
    const res = await fetch("/api/state");
    const data = await res.json();
    const tx = data.unknown.find(t => t.id === id);
    const app = document.getElementById("app");

    if (!tx) {
        app.innerHTML = `
            <div class="page">
                <h1>Transaction not found</h1>
                <button class="btn" onclick="goHome()">Back</button>
            </div>
        `;
        return;
    }

    app.innerHTML = `
    <div class="page detail-page">
        <header class="topbar">
            <h1>Transaction ${escapeHtml(id)}</h1>
        </header>

        <section class="detail-panel">
            <label for="dateBox">Date</label>
            <input
                id="dateBox"
                class="text-input"
                type="text"
                value="${escapeHtml(tx.date || "")}"
            />

            <label for="pathBox">Path</label>
            <input
                id="pathBox"
                class="text-input"
                type="text"
                value="${escapeHtml(tx.path || "")}"
            />

            <label for="editBox">Edit ledger entry</label>
            <textarea id="editBox" class="editor">${escapeHtml(tx.ledger || "")}</textarea>

            <div class="actions">
                <button class="btn primary" onclick="saveEdit('${id}')">Save</button>
                <button class="btn danger" onclick="deleteTransaction('${id}')">Delete</button>
                <button class="btn" onclick="goHome()">Back</button>
            </div>
        </section>
    </div>
`;
}
async function saveEdit(id) {
    const ledger = document.getElementById("editBox").value;
    const date = document.getElementById("dateBox").value;
    const path = document.getElementById("pathBox").value;

    const res = await fetch("/api/update-transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, ledger, date, path })
    });

    if (!res.ok) {
        alert("Save failed");
        return;
    }

    goHome();
}

async function deleteTransaction(id) {
    const res = await fetch("/api/update-transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });

    if (!res.ok) {
        alert("Delete failed");
        return;
    }

    goHome();
}

init();
