# Polymarket BTC 5m Bot

> Bot de trading automatisé, spécialisé sur le marché BTC-updown-5m de Polymarket

## Fonctionnalités

- 🤖 **Trading Automatisé**: Place des ordres dans la première minute de chaque période de 5 minutes
- 📝 **Ordres Limités**: Achète simultanément Yes et No, prix 10, quantité 0,5
- 🔄 **Annulation Intelligente**: Annule automatiquement l'autre ordre si l'un est exécuté dans les 30 dernières secondes
- 🌐 **Interface Web**: Interface moderne et épurée avec mode sombre/clair
- 🌍 **Multi-langues**: Anglais, Japonais, Chinois, Coréen, Allemand, Français, Espagnol
- 💾 **Stockage Local**: Toute la configuration stockée dans le localStorage du navigateur

## Démarrage Rapide

```bash
# Cloner le dépôt
git clone https://github.com/whitebigfox/polymarket-btc5m-bot.git
cd polymarket-btc5m-bot

# Initialiser l'environnement
chmod +x scripts/*.sh
./scripts/init.sh

# Démarrer le bot
./scripts/manage.sh start
```

Puis ouvrir http://localhost:8000

## Logique de Trading

1. **Première Minute (0:00-1:00)**: Place des ordres limités pour Yes et No
   - Prix: 10
   - Quantité: 0,5 (chacun)
2. **30 Dernières Secondes (4:30-5:00)**: Vérifie le statut des ordres
   - Si un ordre est exécuté → annule l'autre
3. **Répéter**: Toutes les 5 minutes

## Scripts

```bash
# Initialiser l'environnement
./scripts/init.sh

# Gérer le bot
./scripts/manage.sh start    # Démarrer
./scripts/manage.sh stop     # Arrêter
./scripts/manage.sh restart  # Redémarrer
./scripts/manage.sh info     # Afficher le statut
```

## Stack Technique

- **Backend**: Python 3 + FastAPI
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **WebSocket**: Mises à jour en temps réel

## Sécurité

⚠️ **Utilisation locale uniquement** — déploiement non recommandé  
⚠️ Clé privée stockée uniquement en mémoire (perdue au redémarrage/arrêt)  
⚠️ Pas d'authentification — utiliser uniquement dans un environnement de confiance

## Licence

MIT