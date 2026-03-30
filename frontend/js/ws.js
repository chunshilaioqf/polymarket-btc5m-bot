class WSManager {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.listeners = { status: [], logs: [], error: [] };
    }

    connect() {
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log("WebSocket connected");
            this.reconnectAttempts = 0;
            this.updateConnectionStatus(true);
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (e) {
                console.error("Failed to parse:", e);
            }
        };

        this.ws.onclose = () => {
            console.log("WebSocket disconnected");
            this.updateConnectionStatus(false);
            this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            this.listeners.error.forEach(cb => cb(error));
        };
    }

    handleMessage(data) {
        switch (data.type) {
            case "status":
                window.tradingState = data.data;
                this.listeners.status.forEach(cb => cb(data.data));
                break;
            case "logs":
                this.listeners.logs.forEach(cb => cb(data.data));
                break;
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }

    updateConnectionStatus(connected) {
        const status = document.getElementById("connection-status");
        const text = document.getElementById("connection-text");
        const wsStatus = document.getElementById("ws-status");
        if (connected) {
            status.className = "connection-status connected";
            text.textContent = t("connected");
            wsStatus.textContent = "✓";
            wsStatus.style.color = "var(--success)";
        } else {
            status.className = "connection-status";
            text.textContent = t("disconnected");
            wsStatus.textContent = "✗";
            wsStatus.style.color = "var(--error)";
        }
    }

    on(event, callback) {
        if (this.listeners[event]) this.listeners[event].push(callback);
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    close() { if (this.ws) this.ws.close(); }
}

async function startTrading(privateKey, proxy, signatureType) {
    try {
        const response = await fetch("/api/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ private_key: privateKey, proxy: proxy, signature_type: signatureType })
        });
        const result = await response.json();
        if (result.status === "success" && document.getElementById("save-private-key").checked) {
            localStorage.setItem("saved_private_key", privateKey);
            if (proxy) localStorage.setItem("saved_proxy", proxy);
        }
        return result;
    } catch (error) { return { status: "error", message: error.message }; }
}

async function stopTrading() {
    try {
        const response = await fetch("/api/stop", { method: "POST" });
        localStorage.removeItem("saved_private_key");
        return await response.json();
    } catch (error) { return { status: "error", message: error.message }; }
}

async function getStatus() {
    try {
        const response = await fetch("/api/status");
        const result = await response.json();
        window.tradingState = result;
        return result;
    } catch (error) { return { running: false }; }
}

async function getLogs(limit = 100) {
    try { return await (await fetch(`/api/logs?limit=${limit}`)).json(); }
    catch (error) { return { logs: [] }; }
}