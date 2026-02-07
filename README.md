# 📌 Your_BookMark

Your_BookMark is a Flask-based web application designed to help students and developers
**bookmark, organize, and revise questions efficiently** instead of repeatedly forgetting
previously solved problems.

---

## 🚀 Why Your_BookMark?

Many learners solve DSA problems regularly, but after a few weeks, the same problems feel new.
This happens because we often don’t track:
- what mistake we made
- what key idea helped solve the problem

Your_BookMark focuses on **structured revision**, not just problem solving.

---

## ✨ Features

- 🔐 User Authentication (Register / Login / Logout)
- 📂 Topic-wise organization (Arrays, Strings, DP, Graphs, etc.)
- 📝 Store questions with:
  - Problem link
  - Difficulty level
  - Mistakes made
  - Key takeaways (in your own words)
- ✅ Mark questions as revised
- 📊 Dashboard showing:
  - Total topics
  - Total questions
  - Pending revisions
- 🎨 Clean, coding-themed UI with responsive design

---

## 🛠 Tech Stack

- **Backend:** Flask, Flask-Login, Flask-WTF
- **Database:** SQLite (via SQLAlchemy)
- **Authentication:** Bcrypt
- **Frontend:** HTML, CSS
- **Deployment:** Render (Free Tier)

---

## 🌍 Live Demo

🔗 Live Website: https://your-bookmark.onrender.com

---

## ⚠️ Important Note About Data Persistence

This application is deployed on **Render Free Tier** using **SQLite**.
Due to platform limitations, the database **resets on every redeploy**.
As a result:
- User accounts may need to be re-created
- Previously stored data may be cleared

For production use, the app can be easily migrated to a persistent database like **PostgreSQL**.

---

## 📌 Purpose of This Project

This project was built as a **learning** to practice:
- Flask backend development
- Authentication workflows
- Database relationships
- Clean project architecture
- Real-world deployment considerations

---

## 👤 Author

**Fahad Afzal Hussain**
