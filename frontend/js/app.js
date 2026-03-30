let wsManager = null;

document.addEventListener("DOMContentLoaded", () => {
    applyTheme(getTheme());
    updateUI();

    const savedKey = localStorage.getItem("saved_private_key");
    if (savedKey) {
        document.getElementById("private-key").value = savedKey;
        document.getElementById("save-private-key").checked = true;
    }
    const savedProxy = localStorage.getItem("saved_proxy");
    if (savedProxy) {
        document.getElementById("proxy").value = savedProxy;
    }

    wsManager = new WSManager();
    wsManager.connect();
    wsManager.on("status", updateStatusUI);
    wsManager.on("logs", appendLogs);
    wsManager.on("error", console.error);

    setupEventListeners();
    setInterval(updatePeriodInfo, 1000);
});

function setupEventListeners() {
    document.getElementById("start-btn").addEventListener("click", async () => {
        const privateKey = document.getElementById("private-key").value.trim();
        const proxy = document.getElementById("proxy").value.trim();
        const signatureType = parseInt(document.getElementById("signature-type").value);
        if (!privateKey) { alert(t("privateKeyPlaceholder")); return; }
        const btn = document.getElementById("start-btn");
        btn.disabled = true;
        btn.querySelector("span").innerHTML = '<span class="loading"></span>';
        const result = await startTrading(privateKey, proxy, signatureType);
        btn.disabled = false;
        btn.querySelector("span").textContent = t("start");
        if (result.status === "error") alert(result.message);
    });

    document.getElementById("stop-btn").addEventListener("click", async () => {
        const btn = document.getElementById("stop-btn");
        btn.disabled = true;
        btn.querySelector("span").innerHTML = '<span class="loading"></span>';
        await stopTrading();
        btn.disabled = false;
        btn.querySelector("span").textContent = t("stop");
    });

    document.getElementById("clear-logs-btn").addEventListener("click", () => {
        document.getElementById("logs-container").innerHTML = "";
    });

    document.getElementById("theme-select").addEventListener("change", (e) => setTheme(e.target.value));
    document.getElementById("language-select").addEventListener("change", (e) => setLanguage(e.target.value));
}

function updateStatusUI(state) {
    if (!state) return;

    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");

    if (state.running) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }

    updateStatusDisplay();

    // 更新地址
    if (state.address) {
        const addr = state.address;
        document.getElementById("address-value").textContent = addr.slice(0, 6) + "..." + addr.slice(-4);
    }

    // 更新余额
    if (state.balance && state.balance.balance_usdc !== undefined) {
        document.getElementById("balance-value").textContent = "$" + state.balance.balance_usdc.toFixed(2);
    }

    // 更新订单
    if (state.orders) {
        const upOrder = state.orders.up_order_id;
        const downOrder = state.orders.down_order_id;
        document.getElementById("yes-order").textContent = upOrder ? upOrder.slice(0, 8) + "..." : "-";
        document.getElementById("no-order").textContent = downOrder ? downOrder.slice(0, 8) + "..." : "-";
        document.getElementById("yes-status").textContent = state.orders.up_filled ? "✓ 已成交" : t("waiting");
        document.getElementById("no-status").textContent = state.orders.down_filled ? "✓ 已成交" : t("waiting");
    }

    // 更新持仓
    updatePositions(state.positions || []);

    // 更新交易历史
    updateHistory(state.trade_history || []);
}

function updatePositions(positions) {
    const tbody = document.getElementById("positions-body");
    if (!positions.length) {
        tbody.innerHTML = `<tr class="empty-row"><td colspan="5">${t("noPositions")}</td></tr>`;
        return;
    }
    tbody.innerHTML = positions.map(p => `
        <tr>
            <td>${p.outcome || "-"}</td>
            <td>${p.side || "-"}</td>
            <td>${p.size || "-"}</td>
            <td>${p.avgPrice || "-"}</td>
            <td>$${parseFloat(p.currentValue || 0).toFixed(2)}</td>
        </tr>
    `).join("");
}

function updateHistory(trades) {
    const tbody = document.getElementById("history-body");
    if (!trades.length) {
        tbody.innerHTML = `<tr class="empty-row"><td colspan="5">${t("noHistory")}</td></tr>`;
        return;
    }
    tbody.innerHTML = trades.slice(0, 10).map(trade => {
        const time = new Date(trade.match_time || trade.timestamp || Date.now()).toLocaleString();
        return `
        <tr>
            <td>${time}</td>
            <td>${trade.market || "-"}</td>
            <td>${trade.side || "-"}</td>
            <td>${trade.price || "-"}</td>
            <td>${trade.size || "-"}</td>
        </tr>`;
    }).join("");
}

function updatePeriodInfo() {
    const now = new Date();
    const timestamp = now.getTime() / 1000;
    const period = Math.floor(timestamp / 300);
    const periodStart = period * 300;
    const periodEnd = periodStart + 300;
    const secondsUntilEnd = Math.floor(periodEnd - timestamp);

    document.getElementById("period-badge").textContent = "#" + period;
    document.getElementById("seconds-remaining").textContent = secondsUntilEnd;
    document.getElementById("period-start").textContent = new Date(periodStart * 1000).toLocaleTimeString();
    document.getElementById("period-end").textContent = new Date(periodEnd * 1000).toLocaleTimeString();
}

function appendLogs(logs) {
    const container = document.getElementById("logs-container");
    logs.forEach(log => {
        const entry = document.createElement("div");
        entry.className = "log-entry";
        const time = new Date(log.timestamp);
        const timeStr = time.toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        entry.innerHTML = `
            <span class="log-time">${timeStr}</span>
            <span class="log-level ${log.level}">${log.level}</span>
            <span class="log-message">${escapeHtml(log.message)}</span>
        `;
        container.appendChild(entry);
    });
    container.scrollTop = container.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

window.tradingState = { running: false };