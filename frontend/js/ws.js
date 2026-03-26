// WebSocket 管理
class WSManager {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.listeners = {
            status: [],
            logs: [],
            error: []
        };
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
                console.error("Failed to parse WebSocket message:", e);
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
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            setTimeout(() => this.connect(), this.reconnectDelay);
        }
    }
    
    updateConnectionStatus(connected) {
        const indicator = document.getElementById("connection-indicator");
        const text = document.getElementById("connection-text");
        
        if (connected) {
            indicator.className = "status-indicator running";
            text.textContent = t("connected");
        } else {
            indicator.className = "status-indicator stopped";
            text.textContent = t("disconnected");
        }
    }
    
    on(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event].push(callback);
        }
    }
    
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
    
    close() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// API 函数
async function startTrading(privateKey) {
    try {
        const response = await fetch("/api/start", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ private_key: privateKey })
        });
        
        const result = await response.json();
        
        if (result.status === "success") {
            // 保存私钥到 localStorage（可选）
            if (document.getElementById("save-private-key").checked) {
                localStorage.setItem("saved_private_key", privateKey);
            }
        }
        
        return result;
    } catch (error) {
        console.error("Start trading error:", error);
        return { status: "error", message: error.message };
    }
}

async function stopTrading() {
    try {
        const response = await fetch("/api/stop", {
            method: "POST"
        });
        
        const result = await response.json();
        
        // 清除保存的私钥
        localStorage.removeItem("saved_private_key");
        
        return result;
    } catch (error) {
        console.error("Stop trading error:", error);
        return { status: "error", message: error.message };
    }
}

async function getStatus() {
    try {
        const response = await fetch("/api/status");
        const result = await response.json();
        window.tradingState = result;
        return result;
    } catch (error) {
        console.error("Get status error:", error);
        return { running: false };
    }
}

async function getLogs(limit = 100) {
    try {
        const response = await fetch(`/api/logs?limit=${limit}`);
        return await response.json();
    } catch (error) {
        console.error("Get logs error:", error);
        return { logs: [] };
    }
}
