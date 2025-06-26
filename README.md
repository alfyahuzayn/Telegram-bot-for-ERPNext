# Telegram-bot-for-ERPNext
Telegram bot for marking the employee checkins for ERPNext in just one click.


# 🤖 ERPNext Telegram Bot Integration

This project connects a **Telegram bot** to your **local ERPNext instance**, allowing employees to punch in and out using simple Telegram commands. The integration uses ERPNext’s REST API and the `python-telegram-bot` library.

---

## 🚀 Features

* `/start` — Displays a welcome message
* `/help` — Lists available commands
* `/id` — Returns the user's Telegram ID
* `/punch_in` — Records an "IN" attendance check
* `/punch_out` — Records an "OUT" attendance check

---

## 📦 Prerequisites

* Frappe Version 12+
* Python 3.x
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

## ⚖️ Step 1: Telegram Integration with ERPNext

### Install the ERPNext Telegram App

1. **Install ****\`\`**** inside the Frappe bench environment:**

   ```bash
   ./env/bin/pip install python-telegram-bot --upgrade
   ```

   > This ensures the package is installed in the correct environment (not globally).

2. **Get the integration app:**

   ```bash
   bench get-app erpnext_telegram_integration https://github.com/yrestom/erpnext_telegram.git
   ```

3. **Install the app on your site:**

   ```bash
   bench --site [your.site.name] install-app erpnext_telegram_integration
   ```

4. **Build and restart:**

   ```bash
   bench build
   bench restart
   ```

---

## 🤖 Step 2: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`.
2. Use `/newbot` and follow the prompts.
3. Save the **Telegram Bot Token** it gives you — you'll need this later.

---

## ⚙️ Step 3: Configure in ERPNext

### A. Telegram Settings

1. Go to **Telegram Settings** in ERPNext.
2. Create a new record and enter:

   * The **bot username**
   * The **token** from BotFather

### B. Telegram User Settings

1. Go to **Telegram User Settings**.
2. Create a new entry and fill in:

   * **Party** → `Employee`
   * **Employee** → the employee associated with the bot
   * **Telegram Settings** → select the one you created above
   * If it’s a group, check **"Is Group Chat"**
3. Click **Generate Telegram Token** — copy this token.
4. Send this token to the Telegram bot in a private message.
5. Return to ERPNext and click **Get Chat ID**.
6. If successful, save the document.

---

## 🧠 Step 4: Create the Bot Script

1. On your server, create a file named `erp_bot.py`.
2. Paste the Python bot logic (you’ve written) into it.

### 🔐 Update Configuration in `erp_bot.py`:

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ERP_URL = "http://your-local-erp-instance/"
ERP_API_KEY = "your-api-key"
ERP_API_SECRET = "your-api-secret"
```

Replace these with your actual credentials.

---

## 🏃 Step 5: Run the Bot

### A. Run Manually (For Testing)

```bash
python erp_bot.py
```

### B. Run as a Background Service (Recommended)

#### 1. Create a Virtual Environment

```bash
python3 -m venv erpbot-env
source erpbot-env/bin/activate
pip install python-telegram-bot requests
```

#### 2. Create systemd Service

Create the file `/etc/systemd/system/erpbot.service`:

```ini
[Unit]
Description=ERPNext Telegram Bot Service
After=network.target

[Service]
ExecStart=/home/your-username/erpbot-env/bin/python /home/your-username/Telegram-bot-for-ERPNext/erp_bot.py
WorkingDirectory=/home/your-username/Telegram-bot-for-ERPNext
Restart=always
User=your-username

[Install]
WantedBy=multi-user.target
```

> Replace `your-username` with your actual Linux username.

#### 3. Start the Bot

```bash
sudo systemctl daemon-reload
sudo systemctl enable erpbot.service
sudo systemctl start erpbot.service
sudo systemctl status erpbot.service
```

To stop or restart:

```bash
sudo systemctl stop erpbot.service
sudo systemctl restart erpbot.service
```

---

## 👨‍💼 Step 6: Link Telegram ID to Employee

1. In Telegram, type `/id` to get your user ID.
2. In ERPNext, go to the **Employee** document.
3. Add the Telegram ID to the `custom_telegram_id` field.
4. Ensure a shift is assigned to the employee.

---

## ✅ How It Works

Once everything is set:

* `/punch_in` → Creates an "IN" entry in Employee Checkin.
* `/punch_out` → Creates an "OUT" entry in Employee Checkin.

This works in real-time through the REST API.

---

## 📜 License

MIT
