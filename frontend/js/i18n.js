// 多语言支持
const translations = {
    en: {
        title: "Polymarket BTC 5m Bot",
        settings: "Settings",
        privateKey: "Private Key",
        privateKeyPlaceholder: "Enter your private key (0x...)",
        privateKeyHint: "Private key is stored in memory only during trading",
        theme: "Theme",
        themeSystem: "System",
        themeLight: "Light",
        themeDark: "Dark",
        language: "Language",
        start: "Start Trading",
        stop: "Stop Trading",
        clearLogs: "Clear Logs",
        status: "Status",
        running: "Running",
        stopped: "Stopped",
        currentPeriod: "Current Period",
        periodStart: "Period Start",
        periodEnd: "Period End",
        secondsRemaining: "Seconds Remaining",
        yesOrder: "Yes Order",
        noOrder: "No Order",
        yesFilled: "Yes Filled",
        noFilled: "No Filled",
        market: "Market",
        logs: "Logs",
        noLogs: "No logs yet",
        connectionStatus: "Connection",
        connected: "Connected",
        disconnected: "Disconnected",
        config: "Trading Config",
        tradingPair: "Trading Pair",
        price: "Price",
        quantity: "Quantity",
        cancelWindow: "Cancel Window",
        startError: "Failed to start trading",
        stopError: "Failed to stop trading",
        seconds: "seconds"
    },
    ja: {
        title: "Polymarket BTC 5m Bot",
        settings: "設定",
        privateKey: "秘密鍵",
        privateKeyPlaceholder: "秘密鍵を入力 (0x...)",
        privateKeyHint: "秘密鍵は取引中のみメモリに保存されます",
        theme: "テーマ",
        themeSystem: "システム",
        themeLight: "ライト",
        themeDark: "ダーク",
        language: "言語",
        start: "取引開始",
        stop: "取引停止",
        clearLogs: "ログをクリア",
        status: "ステータス",
        running: "実行中",
        stopped: "停止",
        currentPeriod: "現在期間",
        periodStart: "期間開始",
        periodEnd: "期間終了",
        secondsRemaining: "残り時間",
        yesOrder: "Yes注文",
        noOrder: "No注文",
        yesFilled: "Yes約定",
        noFilled: "No約定",
        market: "マーケット",
        logs: "ログ",
        noLogs: "ログがありません",
        connectionStatus: "接続",
        connected: "接続済み",
        disconnected: "切断",
        config: "取引設定",
        tradingPair: "取引ペア",
        price: "価格",
        quantity: "数量",
        cancelWindow: "キャンセル期間",
        startError: "取引開始に失敗しました",
        stopError: "取引停止に失敗しました",
        seconds: "秒"
    },
    "zh-CN": {
        title: "Polymarket BTC 5m 交易机器人",
        settings: "设置",
        privateKey: "私钥",
        privateKeyPlaceholder: "输入您的私钥 (0x...)",
        privateKeyHint: "私钥仅在交易期间存储在内存中",
        theme: "主题",
        themeSystem: "跟随系统",
        themeLight: "浅色",
        themeDark: "深色",
        language: "语言",
        start: "开始交易",
        stop: "停止交易",
        clearLogs: "清空日志",
        status: "状态",
        running: "运行中",
        stopped: "已停止",
        currentPeriod: "当前周期",
        periodStart: "周期开始",
        periodEnd: "周期结束",
        secondsRemaining: "剩余秒数",
        yesOrder: "Yes 订单",
        noOrder: "No 订单",
        yesFilled: "Yes 已成交",
        noFilled: "No 已成交",
        market: "市场",
        logs: "日志",
        noLogs: "暂无日志",
        connectionStatus: "连接状态",
        connected: "已连接",
        disconnected: "已断开",
        config: "交易配置",
        tradingPair: "交易对",
        price: "价格",
        quantity: "数量",
        cancelWindow: "取消窗口期",
        startError: "启动交易失败",
        stopError: "停止交易失败",
        seconds: "秒"
    },
    ko: {
        title: "Polymarket BTC 5m 봇",
        settings: "설정",
        privateKey: "개인 키",
        privateKeyPlaceholder: "개인 키 입력 (0x...)",
        privateKeyHint: "개인 키는 거래 중에만 메모리에 저장됩니다",
        theme: "테마",
        themeSystem: "시스템",
        themeLight: "라이트",
        themeDark: "다크",
        language: "언어",
        start: "거래 시작",
        stop: "거래 중지",
        clearLogs: "로그 지우기",
        status: "상태",
        running: "실행 중",
        stopped: "중지됨",
        currentPeriod: "현재 기간",
        periodStart: "기간 시작",
        periodEnd: "기간 종료",
        secondsRemaining: "남은 시간",
        yesOrder: "Yes 주문",
        noOrder: "No 주문",
        yesFilled: "Yes 체결",
        noFilled: "No 체결",
        market: "시장",
        logs: "로그",
        noLogs: "로그 없음",
        connectionStatus: "연결",
        connected: "연결됨",
        disconnected: "연결 끊김",
        config: "거래 설정",
        tradingPair: "거래 쌍",
        price: "가격",
        quantity: "수량",
        cancelWindow: "취소 기간",
        startError: "거래 시작 실패",
        stopError: "거래 중지 실패",
        seconds: "초"
    },
    de: {
        title: "Polymarket BTC 5m Bot",
        settings: "Einstellungen",
        privateKey: "Privater Schlüssel",
        privateKeyPlaceholder: "Privaten Schlüssel eingeben (0x...)",
        privateKeyHint: "Privater Schlüssel wird nur während des Handels im Speicher gespeichert",
        theme: "Design",
        themeSystem: "System",
        themeLight: "Hell",
        themeDark: "Dunkel",
        language: "Sprache",
        start: "Handel starten",
        stop: "Handel stoppen",
        clearLogs: "Logs löschen",
        status: "Status",
        running: "Läuft",
        stopped: "Gestoppt",
        currentPeriod: "Aktuelle Periode",
        periodStart: "Periodenstart",
        periodEnd: "Periodenende",
        secondsRemaining: "Verbleibende Sekunden",
        yesOrder: "Yes Order",
        noOrder: "No Order",
        yesFilled: "Yes ausgeführt",
        noFilled: "No ausgeführt",
        market: "Markt",
        logs: "Logs",
        noLogs: "Noch keine Logs",
        connectionStatus: "Verbindung",
        connected: "Verbunden",
        disconnected: "Getrennt",
        config: "Handelskonfiguration",
        tradingPair: "Handelspaar",
        price: "Preis",
        quantity: "Menge",
        cancelWindow: "Cancel-Fenster",
        startError: "Handel konnte nicht gestartet werden",
        stopError: "Handel konnte nicht gestoppt werden",
        seconds: "Sekunden"
    },
    fr: {
        title: "Bot Polymarket BTC 5m",
        settings: "Paramètres",
        privateKey: "Clé privée",
        privateKeyPlaceholder: "Entrez votre clé privée (0x...)",
        privateKeyHint: "La clé privée n'est stockée en mémoire que pendant le trading",
        theme: "Thème",
        themeSystem: "Système",
        themeLight: "Clair",
        themeDark: "Sombre",
        language: "Langue",
        start: "Démarrer le trading",
        stop: "Arrêter le trading",
        clearLogs: "Effacer les logs",
        status: "Statut",
        running: "En cours",
        stopped: "Arrêté",
        currentPeriod: "Période actuelle",
        periodStart: "Début de période",
        periodEnd: "Fin de période",
        secondsRemaining: "Secondes restantes",
        yesOrder: "Ordre Yes",
        noOrder: "Ordre No",
        yesFilled: "Yes exécuté",
        noFilled: "No exécuté",
        market: "Marché",
        logs: "Logs",
        noLogs: "Pas encore de logs",
        connectionStatus: "Connexion",
        connected: "Connecté",
        disconnected: "Déconnecté",
        config: "Configuration de trading",
        tradingPair: "Paire de trading",
        price: "Prix",
        quantity: "Quantité",
        cancelWindow: "Fenêtre d'annulation",
        startError: "Échec du démarrage du trading",
        stopError: "Échec de l'arrêt du trading",
        seconds: "secondes"
    },
    es: {
        title: "Bot Polymarket BTC 5m",
        settings: "Configuración",
        privateKey: "Clave privada",
        privateKeyPlaceholder: "Ingresa tu clave privada (0x...)",
        privateKeyHint: "La clave privada solo se almacena en memoria durante el trading",
        theme: "Tema",
        themeSystem: "Sistema",
        themeLight: "Claro",
        themeDark: "Oscuro",
        language: "Idioma",
        start: "Iniciar trading",
        stop: "Detener trading",
        clearLogs: "Limpiar logs",
        status: "Estado",
        running: "Ejecutando",
        stopped: "Detenido",
        currentPeriod: "Período actual",
        periodStart: "Inicio del período",
        periodEnd: "Fin del período",
        secondsRemaining: "Segundos restantes",
        yesOrder: "Orden Yes",
        noOrder: "Orden No",
        yesFilled: "Yes ejecutado",
        noFilled: "No ejecutado",
        market: "Mercado",
        logs: "Logs",
        noLogs: "Sin logs aún",
        connectionStatus: "Conexión",
        connected: "Conectado",
        disconnected: "Desconectado",
        config: "Configuración de trading",
        tradingPair: "Par de trading",
        price: "Precio",
        quantity: "Cantidad",
        cancelWindow: "Ventana de cancelación",
        startError: "Error al iniciar el trading",
        stopError: "Error al detener el trading",
        seconds: "segundos"
    }
};

// 语言名称映射
const languageNames = {
    en: "English",
    ja: "日本語",
    "zh-CN": "简体中文",
    ko: "한국어",
    de: "Deutsch",
    fr: "Français",
    es: "Español"
};

// 获取当前语言
function getCurrentLang() {
    return localStorage.getItem("lang") || "zh-CN";
}

// 翻译函数
function t(key) {
    const lang = getCurrentLang();
    return translations[lang]?.[key] || translations["en"][key] || key;
}

// 设置语言
function setLanguage(lang) {
    localStorage.setItem("lang", lang);
    updateUI();
}

// 获取主题
function getTheme() {
    return localStorage.getItem("theme") || "system";
}

// 设置主题
function setTheme(theme) {
    localStorage.setItem("theme", theme);
    applyTheme(theme);
}

// 应用主题
function applyTheme(theme) {
    const root = document.documentElement;
    
    if (theme === "system") {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        root.setAttribute("data-theme", prefersDark ? "dark" : "light");
    } else {
        root.setAttribute("data-theme", theme);
    }
}

// 监听系统主题变化
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (getTheme() === "system") {
        applyTheme("system");
    }
});

// 更新 UI 文本
function updateUI() {
    document.getElementById("title").textContent = t("title");
    document.getElementById("settings-title").textContent = t("settings");
    document.getElementById("private-key-label").textContent = t("privateKey");
    document.getElementById("private-key").placeholder = t("privateKeyPlaceholder");
    document.getElementById("private-key-hint").textContent = t("privateKeyHint");
    document.getElementById("theme-label").textContent = t("theme");
    document.getElementById("language-label").textContent = t("language");
    document.getElementById("start-btn").textContent = t("start");
    document.getElementById("stop-btn").textContent = t("stop");
    document.getElementById("clear-logs-btn").textContent = t("clearLogs");
    document.getElementById("status-title").textContent = t("status");
    document.getElementById("config-title").textContent = t("config");
    document.getElementById("logs-title").textContent = t("logs");
    
    // 更新主题选项
    document.getElementById("theme-system").textContent = t("themeSystem");
    document.getElementById("theme-light").textContent = t("themeLight");
    document.getElementById("theme-dark").textContent = t("themeDark");
    
    // 更新状态文本
    updateStatusDisplay();
}

// 更新状态显示
function updateStatusDisplay() {
    const statusIndicator = document.getElementById("status-indicator");
    const statusText = document.getElementById("status-text");
    const isRunning = window.tradingState?.running;
    
    if (isRunning) {
        statusIndicator.className = "status-indicator running";
        statusText.textContent = t("running");
    } else {
        statusIndicator.className = "status-indicator stopped";
        statusText.textContent = t("stopped");
    }
}
