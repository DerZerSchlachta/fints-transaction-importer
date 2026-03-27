async function loadTransactions() {
    const res = await fetch("/api/unknown-transactions");
    const data = await res.json();

    const container = document.getElementById("transactions");
    container.innerHTML = "";

    data.forEach(tx => {
        const div = document.createElement("div");
        div.className = "entry";

        div.innerHTML = `
            <div><strong>ID:</strong> ${tx.id}</div>

            <label>Date:</label>
            <input type="text" value="${tx.date}" id="date-${tx.id}">

            <label>Path:</label>
            <input type="text" value="${tx.path}" id="path-${tx.id}">

            <label>Ledger:</label>
            <textarea id="ledger-${tx.id}">${tx.ledger}</textarea>

            <button onclick="saveTransaction('${tx.id}')">Save</button>
        `;

        container.appendChild(div);
    });
}


async function saveTransaction(id) {
    const updatedTx = {
        id: id,
        date: document.getElementById(`date-${id}`).value,
        path: document.getElementById(`path-${id}`).value,
        ledger: document.getElementById(`ledger-${id}`).value
    };

    const res = await fetch("/api/update-transaction", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatedTx)
    });

    const data = await res.json();
    console.log("Saved:", data);

    // Reload list after saving
    loadTransactions();
}


// initial load
loadTransactions();