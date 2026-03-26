// 主应用逻辑
let wsManager = null;

// 初始化
document.addEventListener("DOMContentLoaded", () => {
    // 初始化主题
    applyTheme(getTheme());
    
    // 初始化语言
    updateUI();
    
    // 恢复保存的私钥
    const savedKey = localStorage.getItem("saved_private_key");
    if (savedKey) {
        document.getElementById("private-key").value = savedKey;
        document.getElementById("save-private-key").checked = true;
    }
    
    // 初始化 WebSocket
    wsManager = new WSManager();
    wsManager.connect();
    
    // 监听状态更新
    wsManager.on("status", updateStatusUI);
    
    // 监听日志更新
    wsManager.on("logs", appendLogs);
    
    // 监听错误
    wsManager.on("error", (error) => {
        console.error("WebSocket error:", error);
    });
    
    // 设置按钮事件
    setupEventListeners();
    
    // 定期更新状态
    setInterval(async () => {
        if (wsManager && wsManager.ws && wsManager.ws.readyState !== WebSocket.OPEN) {
            await getStatus();
            updateStatusUI(window.tradingState);
        }
    }, 5000);
});

// 设置事件监听
function setupEventListeners() {
    // 开始交易按钮
    document.getElementById("start-btn").addEventListener("click", async () => {
        const privateKey = document.getElementById("private-key").value.trim();
        
        if (!privateKey) {
            alert(t("privateKeyPlaceholder"));
            return;
        }
        
        const btn = document.getElementById("start-btn");
        btn.disabled = true;
        btn.innerHTML = '<span class="loading"></span>';
        
        const result = await startTrading(privateKey);
        
        btn.disabled = false;
        btn.textContent = t("start");
        
        if (result.status === "error") {
            alert(t("startError") + ": " + result.message);
        }
    });
    
    // 停止交易按钮
    document.getElementById("stop-btn").addEventListener("click", async () => {
        const btn = document.getElementById("stop-btn");
        btn.disabled = true;
        btn.innerHTML = '<span class="loading"></span>';
        
        const result = await stopTrading();
        
        btn.disabled = false;
        btn.textContent = t("stop");
        
        if (result.status === "error") {
            alert(t("stopError") + ": " + result.message);
        }
    });
    
    // 清空日志按钮
    document.getElementById("clear-logs-btn").addEventListener("click", () => {
        document.getElementById("logs-container").innerHTML = "";
    });
    
    // 主题选择
    document.getElementById("theme-select").addEventListener("change", (e) => {
        setTheme(e.target.value);
    });
    
    // 语言选择
    document.getElementById("language-select").addEventListener("change", (e) => {
        setLanguage(e.target.value);
    });
    
    // 周期信息更新
    setInterval(updatePeriodInfo, 1000);
}

// 更新状态 UI
function updateStatusUI(state) {
    if (!state) return;
    
    // 更新运行状态
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    
    if (state.running) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
    
    // 更新状态指示器
    updateStatusDisplay();
    
    // 更新订单信息
    if (state.orders) {
        document.getElementById("yes-order").textContent = state.orders.yes_order_id || "-";
        document.getElementById("no-order").textContent = state.orders.no_order_id || "-";
        document.getElementById("yes-filled").textContent = state.orders.yes_filled ? "✓" : "-";
        document.getElementById("no-filled").textContent = state.orders.no_filled ? "✓" : "-";
    }
    
    // 更新市场信息
    if (state.market) {
        document.getElementById("market-name").textContent = state.market.question || "-";
    }
}

// 更新周期信息
function updatePeriodInfo() {
    const now = new Date();
    const timestamp = now.getTime() / 1000;
    const period = Math.floor(timestamp / 300);
    const periodStart = period * 300;
    const periodEnd = periodStart + 300;
    const secondsUntilEnd = Math.floor(periodEnd - timestamp);
    
    document.getElementById("current-period").textContent = period;
    document.getElementById("period-start").textContent = new Date(periodStart * 1000).toLocaleString();
    document.getElementById("period-end").textContent = new Date(periodEnd * 1000).toLocaleString();
    document.getElementById("seconds-remaining").textContent = secondsUntilEnd + " " + t("seconds");
}

// 追加日志
function appendLogs(logs) {
    const container = document.getElementById("logs-container");
    
    logs.forEach(log => {
        const entry = document.createElement("div");
        entry.className = "log-entry";
        
        const time = new Date(log.timestamp).toLocaleTimeString();
        const level = log.level;
        const message = log.message;
        
        entry.innerHTML = `
            <span class="log-time">${time}</span>
            <span class="log-level ${level}">${level}</span>
            <span class="log-message">${escapeHtml(message)}</span>
        `;
        
        container.appendChild(entry);
    });
    
    // 自动滚动到底部
    container.scrollTop = container.scrollHeight;
}

// 转义 HTML
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// 公开全局函数供 i18n.js 使用
window.tradingState = { running: false };