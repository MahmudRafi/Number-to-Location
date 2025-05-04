
# 📍 Number to Location Telegram Bot

A powerful Telegram bot that tracks **location using only a mobile number** – no internet or GPS required!  
This bot works exclusively with **Robi** and **Airtel** SIM numbers and leverages **SIM tower triangulation** for precise positioning.

> ⚠️ For **authorized users only** – the bot has built-in admin authentication.

---

## 🚀 Features

- 📡 Get real-time location from Robi or Airtel numbers
- 🔒 Admin-only access for maximum security
- ⚙️ API-based architecture for accurate results
- 📴 No need for mobile data or GPS on the target device

---

## 🛠️ Deployment (Heroku)

1. **Clone the repo**

```bash
git clone https://github.com/MahmudRafi/Number-to-Location.git
cd Number-to-Location
```

2. **Create a new app on Heroku** at [https://dashboard.heroku.com/new-app](https://dashboard.heroku.com/new-app)

3. **Install Heroku CLI** (if not already installed)  
[https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

4. **Login to Heroku CLI**

```bash
heroku login
```

5. **Create the Heroku app (if you haven’t already)**

```bash
heroku create your-app-name
```

6. **Push the code to Heroku**

```bash
git push heroku main
```

7. **Set environment variables** from your Heroku dashboard (Settings → Reveal Config Vars)

- `BOT_TOKEN`: Your Telegram bot token  
- `ADMIN_IDS`: Comma-separated list of Telegram user IDs allowed to use the bot  
- `API_KEY`: Your location API key (if required)

---

## 💡 Need help?

Just hit me up on Telegram! 🗯️😎  
[@MAHMUD_RAFI](https://t.me/MAHMUD_RAFI)

---

## 🧠 Disclaimer

This bot is for educational and authorized use only. Unauthorized use for tracking individuals without consent may be illegal in your jurisdiction.
