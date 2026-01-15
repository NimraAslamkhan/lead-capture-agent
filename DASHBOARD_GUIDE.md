# 🚀 DASHBOARD SETUP GUIDE

## What You Now Have

Your Lead Capture Agent now includes a **Beautiful Professional Dashboard** where you can:

✅ See all leads in a beautiful table format  
✅ View statistics (Total, Hot, Warm, Cold leads)  
✅ Filter leads by quality (Hot/Warm/Cold)  
✅ Download leads as Excel or CSV  
✅ Real-time auto-refresh every 30 seconds  
✅ Send the link to clients to view leads  

---

## 🔗 How to Access the Dashboard

### Option 1: Direct Link
```
http://localhost:8000/static/dashboard.html
```

### Option 2: From API Root
```
http://localhost:8000/
```
Shows endpoint: `/static/dashboard.html`

---

## 📊 What You See in the Dashboard

| Column | Description |
|--------|-------------|
| **#** | Lead number |
| **Name** | Customer name |
| **Email** | Customer email |
| **Phone** | Customer phone number |
| **Channel** | Where lead came from (WhatsApp, Instagram, Website, Email) |
| **Message** | Customer's message |
| **Intent** | What customer wants (Buy, Question, Complaint, Inquiry) |
| **Urgency** | How urgent (High 🔴, Medium 🟡, Low 🟢) |
| **Score** | Lead value 0-100 |
| **Quality** | Lead grade (🔥 HOT, 🔆 WARM, ❄️ COLD) |
| **Date** | When lead arrived |

---

## 📈 Statistics Cards

At the top, you see 4 cards:
- **Total Leads** - All leads in database
- **🔥 Hot Leads** - Score ≥ 60 (Priority!)
- **🔆 Warm Leads** - Score 40-59 (Follow up)
- **❄️ Cold Leads** - Score < 40 (Later)

---

## 🎛️ Controls & Buttons

### Filters
- **Filter by Quality** - Dropdown to show only Hot/Warm/Cold

### Buttons
- **🔄 Refresh** - Update leads from database right now
- **📥 Download Excel** - Save all leads as Excel file
- **📥 Download CSV** - Save all leads as CSV file

---

## 🌐 Sharing with Clients

You can send this link to your business partners/team:
```
http://YOUR_IP:8000/static/dashboard.html
```

Replace `YOUR_IP` with:
- `localhost:8000` - For local computer
- `192.168.x.x:8000` - For your local network
- `your-domain.com:8000` - For internet (with proper deployment)

### Example Links:
```
Local only:      http://localhost:8000/static/dashboard.html
Network:         http://192.168.1.100:8000/static/dashboard.html
Production:      http://leads.yourcompany.com/static/dashboard.html
```

---

## 🚀 Quick Start

### Step 1: Start the Server
```bash
python -m uvicorn app.main:app --port 8000
```

### Step 2: Add Test Leads (Optional)
```bash
python add_test_leads.py
```

This adds 4 sample leads so you can see the dashboard in action.

### Step 3: Open Dashboard
Visit: http://localhost:8000/static/dashboard.html

---

## 📥 How to Download Leads

### Download as Excel
1. Click **"📥 Download Excel"** button
2. File `leads.csv` downloads to your computer
3. Open in Microsoft Excel or Google Sheets

### Download as CSV
1. Click **"📥 Download CSV"** button
2. File `leads.csv` downloads
3. Open in any spreadsheet application

### Auto-Refresh
Dashboard automatically updates every 30 seconds - no need to refresh manually!

---

## 🎨 Dashboard Features

### Color Coding
- **🔥 Red** = HOT leads (Act immediately!)
- **🔆 Orange** = WARM leads (Follow up soon)
- **❄️ Light Blue** = COLD leads (Contact later)

### Intent Colors
- **Green** = Buy intent (Customer wants to purchase!)
- **Blue** = Question (Customer asking about product)
- **Red** = Complaint (Customer has problem)
- **Yellow** = Inquiry (General information)

### Channel Icons
- **💬** = WhatsApp
- **📷** = Instagram
- **🌐** = Website
- **📧** = Email

---

## 📱 Responsive Design

The dashboard works on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones
- ✅ All browsers (Chrome, Firefox, Safari, Edge)

---

## 🔄 Auto-Refresh

Dashboard automatically updates every 30 seconds:
- New leads appear without clicking refresh
- Statistics update in real-time
- You always see latest data

---

## 💾 Database Integration

All displayed data comes from your database:
- Shows exactly what's in database
- Downloads include all database fields
- Filtering happens on live data
- No data loss or delays

---

## 🛠️ API Endpoints Used

Dashboard uses these backend APIs:

### Get All Leads
```
GET http://localhost:8000/api/webhook/leads?limit=100
```

Response:
```json
{
  "status": "success",
  "leads": [
    {
      "id": 1,
      "user_name": "Ahmed Khan",
      "user_email": "ahmed@example.com",
      "user_phone": "+92300123456",
      "channel": "whatsapp",
      "message": "I want to buy...",
      "intent": "Buy",
      "urgency": "High",
      "score": 85,
      "quality": "HOT",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### Get Stats
```
GET http://localhost:8000/api/webhook/stats
```

---

## ❓ FAQ

**Q: Do I need to refresh manually?**
A: No! Dashboard auto-refreshes every 30 seconds.

**Q: Can I filter leads?**
A: Yes! Use "Filter by Quality" dropdown to show Hot/Warm/Cold only.

**Q: Can I export to Excel?**
A: Yes! Click "📥 Download Excel" button.

**Q: How do I send to clients?**
A: Get your computer IP and send: `http://YOUR_IP:8000/static/dashboard.html`

**Q: Will leads disappear?**
A: No! All leads are saved in database permanently.

**Q: How often is it updated?**
A: Every 30 seconds automatically, or click Refresh for instant update.

**Q: Can I delete/edit leads from dashboard?**
A: Current version shows read-only. Contact support to add edit feature.

**Q: Is it secure?**
A: For local use. For production, add password protection or deploy with security.

---

## 🔐 Security Note

Currently the dashboard has **NO PASSWORD PROTECTION**.

For production/internet use, add:
- Authentication (login)
- API key protection
- HTTPS encryption
- Access controls

See `DEPLOYMENT.md` for production setup instructions.

---

## 📞 Support

Having issues? Check:
1. Server running? `python -m uvicorn app.main:app --port 8000`
2. Correct URL? `http://localhost:8000/static/dashboard.html`
3. Database initialized? Check `leads.db` exists
4. Leads added? Run `python add_test_leads.py`

---

## 🎉 Summary

You now have:
- ✅ Professional dashboard
- ✅ Real-time lead display
- ✅ Download functionality
- ✅ Statistics & analytics
- ✅ Shareable link for clients
- ✅ No manual data entry needed!

**Next Step:** Share the dashboard link with your team and start capturing leads! 🚀
