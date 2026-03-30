// 多语言支持
const translations = {
    en: {
        title: "BTC 5m Bot", settings: "Settings", privateKey: "Private Key",
        privateKeyPlaceholder: "Enter private key (0x...)", privateKeyHint: "Stored in memory only",
        theme: "Theme", themeSystem: "System", themeLight: "Light", themeDark: "Dark",
        language: "Language", start: "Start", stop: "Stop", clearLogs: "Clear",
        status: "Status", running: "Running", stopped: "Stopped",
        currentPeriod: "Current Period", seconds: "sec", yesOrder: "YES", noOrder: "NO",
        config: "Config", logs: "Logs", connected: "Connected", disconnected: "Disconnected",
        tradingPair: "Pair", price: "Price", quantity: "Qty", cancelWindow: "Cancel",
        account: "Account", saveKey: "Save locally", proxy: "Proxy (Optional)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "Bypass region restrictions", positions: "Positions",
        history: "Trade History", balance: "Balance", eoaAddress: "EOA Address", funderAddress: "Funder", address: "Address",
        noPositions: "No positions", noHistory: "No trade history",
        thMarket: "Market", thSide: "Side", thQty: "Qty", thAvg: "Avg", thValue: "Value",
        thTime: "Time", thPrice: "Price", thAmount: "Amount", wsStatus: "WS",
        periodStart: "Start", periodEnd: "End", waiting: "Waiting"
    },
    ja: {
        title: "BTC 5m Bot", settings: "設定", privateKey: "秘密鍵",
        privateKeyPlaceholder: "秘密鍵を入力 (0x...)", privateKeyHint: "メモリのみに保存",
        theme: "テーマ", themeSystem: "システム", themeLight: "ライト", themeDark: "ダーク",
        language: "言語", start: "開始", stop: "停止", clearLogs: "クリア",
        status: "ステータス", running: "実行中", stopped: "停止",
        currentPeriod: "現在期間", seconds: "秒", yesOrder: "YES", noOrder: "NO",
        config: "設定", logs: "ログ", connected: "接続済み", disconnected: "切断",
        tradingPair: "ペア", price: "価格", quantity: "数量", cancelWindow: "キャンセル",
        account: "アカウント", saveKey: "ローカル保存", proxy: "プロキシ（任意）", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "地域制限を回避", positions: "ポジション",
        history: "取引履歴", balance: "残高", eoaAddress: "EOA アドレス", funderAddress: "ファンダー", address: "アドレス",
        noPositions: "ポジションなし", noHistory: "取引履歴なし",
        thMarket: "マーケット", thSide: "方向", thQty: "数量", thAvg: "平均", thValue: "価値",
        thTime: "時間", thPrice: "価格", thAmount: "金額", wsStatus: "WS",
        periodStart: "開始", periodEnd: "終了", waiting: "待機中"
    },
    "zh-CN": {
        title: "BTC 5m Bot", settings: "设置", privateKey: "私钥",
        privateKeyPlaceholder: "输入私钥 (0x...)", privateKeyHint: "仅存储在内存中",
        theme: "主题", themeSystem: "跟随系统", themeLight: "浅色", themeDark: "深色",
        language: "语言", start: "开始交易", stop: "停止交易", clearLogs: "清空",
        status: "状态", running: "运行中", stopped: "已停止",
        currentPeriod: "当前周期", seconds: "秒", yesOrder: "YES", noOrder: "NO",
        config: "交易配置", logs: "日志", connected: "已连接", disconnected: "未连接",
        tradingPair: "交易对", price: "价格", quantity: "数量", cancelWindow: "取消窗口",
        account: "账户", saveKey: "保存到本地", proxy: "代理 (可选)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "绕过地区限制，如 Clash/V2Ray", positions: "持仓",
        history: "交易历史", balance: "余额", eoaAddress: "EOA 地址", funderAddress: "Funder 地址", address: "地址",
        noPositions: "暂无持仓", noHistory: "暂无交易记录",
        thMarket: "市场", thSide: "方向", thQty: "数量", thAvg: "均价", thValue: "价值",
        thTime: "时间", thPrice: "价格", thAmount: "数量", wsStatus: "WS",
        periodStart: "开始", periodEnd: "结束", waiting: "等待中"
    },
    ko: {
        title: "BTC 5m Bot", settings: "설정", privateKey: "개인 키",
        privateKeyPlaceholder: "개인 키 입력 (0x...)", privateKeyHint: "메모리에만 저장",
        theme: "테마", themeSystem: "시스템", themeLight: "라이트", themeDark: "다크",
        language: "언어", start: "시작", stop: "중지", clearLogs: "지우기",
        status: "상태", running: "실행 중", stopped: "중지됨",
        currentPeriod: "현재 기간", seconds: "초", yesOrder: "YES", noOrder: "NO",
        config: "설정", logs: "로그", connected: "연결됨", disconnected: "끊김",
        tradingPair: "쌍", price: "가격", quantity: "수량", cancelWindow: "취소",
        account: "계정", saveKey: "로컬 저장", proxy: "프록시 (선택)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "지역 제한 우회", positions: "포지션",
        history: "거래 내역", balance: "잔액", eoaAddress: "EOA 주소", funderAddress: "펀더", address: "주소",
        noPositions: "포지션 없음", noHistory: "거래 내역 없음",
        thMarket: "시장", thSide: "방향", thQty: "수량", thAvg: "평균", thValue: "가치",
        thTime: "시간", thPrice: "가격", thAmount: "금액", wsStatus: "WS",
        periodStart: "시작", periodEnd: "종료", waiting: "대기 중"
    },
    de: {
        title: "BTC 5m Bot", settings: "Einstellungen", privateKey: "Privater Schlüssel",
        privateKeyPlaceholder: "Privaten Schlüssel eingeben (0x...)", privateKeyHint: "Nur im Speicher",
        theme: "Design", themeSystem: "System", themeLight: "Hell", themeDark: "Dunkel",
        language: "Sprache", start: "Starten", stop: "Stoppen", clearLogs: "Löschen",
        status: "Status", running: "Läuft", stopped: "Gestoppt",
        currentPeriod: "Aktuelle Periode", seconds: "Sek", yesOrder: "YES", noOrder: "NO",
        config: "Konfiguration", logs: "Protokoll", connected: "Verbunden", disconnected: "Getrennt",
        tradingPair: "Paar", price: "Preis", quantity: "Menge", cancelWindow: "Abbruch",
        account: "Konto", saveKey: "Lokal speichern", proxy: "Proxy (Optional)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "Regionsbeschränkungen umgehen", positions: "Positionen",
        history: "Handelshistorie", balance: "Guthaben", eoaAddress: "EOA Adresse", funderAddress: "Funder", eoaAddress: "EOA Adresse", funderAddress: "Funder", address: "Adresse",
        noPositions: "Keine Positionen", noHistory: "Keine Historie",
        thMarket: "Markt", thSide: "Seite", thQty: "Menge", thAvg: "Durchschnitt", thValue: "Wert",
        thTime: "Zeit", thPrice: "Preis", thAmount: "Betrag", wsStatus: "WS",
        periodStart: "Start", periodEnd: "Ende", waiting: "Warten"
    },
    fr: {
        title: "BTC 5m Bot", settings: "Paramètres", privateKey: "Clé privée",
        privateKeyPlaceholder: "Entrez la clé privée (0x...)", privateKeyHint: "En mémoire uniquement",
        theme: "Thème", themeSystem: "Système", themeLight: "Clair", themeDark: "Sombre",
        language: "Langue", start: "Démarrer", stop: "Arrêter", clearLogs: "Effacer",
        status: "Statut", running: "En cours", stopped: "Arrêté",
        currentPeriod: "Période actuelle", seconds: "sec", yesOrder: "YES", noOrder: "NO",
        config: "Configuration", logs: "Journaux", connected: "Connecté", disconnected: "Déconnecté",
        tradingPair: "Paire", price: "Prix", quantity: "Qté", cancelWindow: "Annulation",
        account: "Compte", saveKey: "Sauvegarder", proxy: "Proxy (Optionnel)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "Contourner les restrictions", positions: "Positions",
        history: "Historique", balance: "Solde", eoaAddress: "EOA Adresse", funderAddress: "Funder", eoaAddress: "EOA Adresse", funderAddress: "Funder", address: "Adresse",
        noPositions: "Aucune position", noHistory: "Aucun historique",
        thMarket: "Marché", thSide: "Côté", thQty: "Qté", thAvg: "Moy", thValue: "Valeur",
        thTime: "Heure", thPrice: "Prix", thAmount: "Montant", wsStatus: "WS",
        periodStart: "Début", periodEnd: "Fin", waiting: "En attente"
    },
    es: {
        title: "BTC 5m Bot", settings: "Configuración", privateKey: "Clave privada",
        privateKeyPlaceholder: "Ingresa la clave privada (0x...)", privateKeyHint: "Solo en memoria",
        theme: "Tema", themeSystem: "Sistema", themeLight: "Claro", themeDark: "Oscuro",
        language: "Idioma", start: "Iniciar", stop: "Detener", clearLogs: "Limpiar",
        status: "Estado", running: "Ejecutando", stopped: "Detenido",
        currentPeriod: "Período actual", seconds: "seg", yesOrder: "YES", noOrder: "NO",
        config: "Configuración", logs: "Registros", connected: "Conectado", disconnected: "Desconectado",
        tradingPair: "Par", price: "Precio", quantity: "Cant", cancelWindow: "Cancelación",
        account: "Cuenta", saveKey: "Guardar local", proxy: "Proxy (Opcional)", proxyPlaceholder: "http://127.0.0.1:7890", proxyHint: "Evitar restricciones regionales", positions: "Posiciones",
        history: "Historial", balance: "Saldo", eoaAddress: "EOA Dirección", funderAddress: "Funder", address: "Dirección",
        noPositions: "Sin posiciones", noHistory: "Sin historial",
        thMarket: "Mercado", thSide: "Lado", thQty: "Cant", thAvg: "Prom", thValue: "Valor",
        thTime: "Hora", thPrice: "Precio", thAmount: "Monto", wsStatus: "WS",
        periodStart: "Inicio", periodEnd: "Fin", waiting: "Esperando"
    }
};

const languageNames = {
    en: "English", ja: "日本語", "zh-CN": "简体中文",
    ko: "한국어", de: "Deutsch", fr: "Français", es: "Español"
};

function getCurrentLang() { return localStorage.getItem("lang") || "zh-CN"; }

function t(key) {
    const lang = getCurrentLang();
    return translations[lang]?.[key] || translations["en"][key] || key;
}

function setLanguage(lang) {
    localStorage.setItem("lang", lang);
    updateUI();
}

function getTheme() { return localStorage.getItem("theme") || "system"; }

function setTheme(theme) {
    localStorage.setItem("theme", theme);
    applyTheme(theme);
}

function applyTheme(theme) {
    const root = document.documentElement;
    if (theme === "system") {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        root.setAttribute("data-theme", prefersDark ? "dark" : "light");
    } else {
        root.setAttribute("data-theme", theme);
    }
}

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (getTheme() === "system") applyTheme("system");
});

function updateUI() {
    document.getElementById("title").textContent = t("title");
    document.getElementById("settings-title").textContent = t("settings");
    document.getElementById("theme-label").textContent = t("theme");
    document.getElementById("language-label").textContent = t("language");
    document.getElementById("account-title").textContent = t("account");
    document.getElementById("private-key-label").textContent = t("privateKey");
    document.getElementById("private-key").placeholder = t("privateKeyPlaceholder");
    document.getElementById("private-key-hint").textContent = t("privateKeyHint");
    document.getElementById("proxy-label").textContent = t("proxy");
    document.getElementById("proxy").placeholder = t("proxyPlaceholder");
    document.getElementById("proxy-hint").textContent = t("proxyHint");
    document.getElementById("save-key-label").textContent = t("saveKey");
    document.getElementById("start-text").textContent = t("start");
    document.getElementById("stop-text").textContent = t("stop");
    document.getElementById("eoa-label").textContent = t("eoaAddress");
    document.getElementById("funder-label").textContent = t("funderAddress");
    document.getElementById("ws-status-label").textContent = t("wsStatus");
    document.getElementById("period-title").textContent = t("currentPeriod");
    document.getElementById("seconds-label").textContent = t("seconds");
    document.getElementById("start-time-label").textContent = t("periodStart");
    document.getElementById("end-time-label").textContent = t("periodEnd");
    document.getElementById("orders-title").textContent = t("status");
    document.getElementById("config-title").textContent = t("config");
    document.getElementById("pair-label").textContent = t("tradingPair");
    document.getElementById("price-label").textContent = t("price");
    document.getElementById("qty-label").textContent = t("quantity");
    document.getElementById("cancel-label").textContent = t("cancelWindow");
    document.getElementById("positions-title").textContent = t("positions");
    document.getElementById("history-title").textContent = t("history");
    document.getElementById("logs-title").textContent = t("logs");
    document.getElementById("clear-logs-btn").textContent = t("clearLogs");
    document.getElementById("no-positions").textContent = t("noPositions");
    document.getElementById("no-history").textContent = t("noHistory");
    document.getElementById("th-market").textContent = t("thMarket");
    document.getElementById("th-side").textContent = t("thSide");
    document.getElementById("th-qty").textContent = t("thQty");
    document.getElementById("th-avg").textContent = t("thAvg");
    document.getElementById("th-value").textContent = t("thValue");
    document.getElementById("th-market2").textContent = t("thMarket");
    document.getElementById("th-side2").textContent = t("thSide");
    document.getElementById("th-price").textContent = t("thPrice");
    document.getElementById("th-amount").textContent = t("thAmount");
    document.getElementById("th-time").textContent = t("thTime");

    document.getElementById("theme-system").textContent = t("themeSystem");
    document.getElementById("theme-light").textContent = t("themeLight");
    document.getElementById("theme-dark").textContent = t("themeDark");

    updateStatusDisplay();
}

function updateStatusDisplay() {
    const badge = document.getElementById("status-badge");
    const text = document.getElementById("status-text");
    const isRunning = window.tradingState?.running;
    if (isRunning) {
        badge.className = "status-badge running";
        text.textContent = t("running");
    } else {
        badge.className = "status-badge stopped";
        text.textContent = t("stopped");
    }
}