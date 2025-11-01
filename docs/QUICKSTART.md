# Quick Start Guide - Project Samarth

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn pandas requests google-generativeai python-dotenv motor pymongo
```

### Step 2: Configure Environment
Create `.env` file in project root:
```env
SECRET_KEY=your_gemini_api_key_here
API_GUESSING_MODELKEY=your_second_gemini_key_here
DATABASE_URL=your_mongodb_connection_string
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true
```

**Get API Keys:**
- Gemini API: https://aistudio.google.com/app/apikey
- MongoDB: https://www.mongodb.com/cloud/atlas (free tier)

### Step 3: Start the Backend

**Option A: Modular Version (Recommended)**
```bash
cd src
python app_modular.py
```

**Option B: Original Version (Backup)**
```bash
cd src
python app.py
```

You should see:
```
============================================================
APPLICATION STARTUP
============================================================
✅ Connected to MongoDB Atlas successfully!
Loading data from data.gov.in...
Data loaded successfully. Crop records: 104, Rainfall records: 8
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test the System

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Cache Statistics:**
```bash
curl http://localhost:8000/api/cache/stats
```

### Step 5: Try Sample Queries

**Basic Query (Cache Miss - ~13s):**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the rice production in Punjab for 2023?"}'
```

**Same Query Again (Cache Hit - ~0.1s):**
```bash
# Run the same command again - watch the speed!
```

**More Sample Queries:**
```
"Show wheat production in Karnataka for 2014"
"Compare maize production across states"
"Show rainfall in Pune for 2024"
"Punjab rainfall from 1950 to 1960"
```

## 📊 Verify Two-Model Architecture

Check the console output - you'll see:
```
🔀 STEP 1: ROUTING QUERY TO CORRECT APIs...
DEBUG: QueryRouter with API key: AIzaSy...
✅ Routing complete

💡 STEP 3: GENERATING NATURAL LANGUAGE ANSWER...
DEBUG: QueryProcessor with API key: AIzaSy...
✅ Answer generated
```

Two different API keys = Two models working! ✅

## 💾 Verify MongoDB Caching

**First Query (Cache Miss):**
```
💾 STEP 0: CHECKING CACHE
❌ Cache miss. Processing query from scratch...
[13.5 seconds later]
💾 STEP 4: CACHING RESPONSE FOR FUTURE USE...
```

**Second Query (Cache Hit):**
```
💾 STEP 0: CHECKING CACHE
💾 CACHE HIT! Query has been answered 0 times before
⚡ RETURNING CACHED RESPONSE (saved ~3-4 seconds!)
[0.1 seconds - 135x faster!]
```

## 🎬 Recording Your Loom Video

### Pre-Recording Checklist
- [ ] Modular server is running (python app_modular.py)
- [ ] MongoDB connected (check startup logs)
- [ ] Health endpoint working
- [ ] Cache stats endpoint working
- [ ] Test one query (cache miss + cache hit)
- [ ] Close unnecessary applications
- [ ] Clean desktop/background

### What to Show
1. **Architecture** (15 seconds)
   - Show folder structure (config/, models/, services/, api/, database/)
   - Mention modular design

2. **Two Models** (20 seconds)
   - Show .env with two keys
   - Show console logs of both models being used
   - Explain routing vs answer generation

3. **MongoDB Caching** (30 seconds)
   - Show first query (slow - cache miss)
   - Show same query again (fast - cache hit)
   - Show cache stats endpoint

4. **Live Queries** (45 seconds)
   - Test 2-3 different questions
   - Show source citations
   - Demonstrate speed improvement

### Recording Tips
1. **Use Loom Desktop App** for better quality
2. **Select "Screen + Camera"** if you want to be visible
3. **Test audio levels** before recording
4. **Practice your script** 2-3 times
5. **Keep it under 2 minutes** - aim for 1:45 to be safe

### Video Structure
```
0:00-0:15  Introduction & Problem Statement
0:15-0:35  System Architecture Quick Overview
0:35-1:30  Live Demo (3 queries)
1:30-1:50  Key Design Decisions
1:50-2:00  Wrap-up
```

### What to Show
1. **Terminal with server running** (3 seconds)
2. **Frontend interface** (majority of time)
3. **Live queries and results** (focus here)
4. **Source citations** (zoom in if needed)
5. **Brief code glimpse** (optional, 5 seconds max)

### What to Say

**Opening:**
"I built an intelligent Q&A system for Project Samarth that integrates data from data.gov.in to answer complex questions about India's agricultural economy."

**During Demo:**
"Watch how it handles this query... Notice the source citations... The system combines data from multiple datasets..."

**Key Points:**
- Direct integration with data.gov.in
- Multi-dataset synthesis
- Full source traceability
- Handles complex natural language queries

**Closing:**
"This prototype shows end-to-end functionality from question to cited answer, ready for deployment in secure environments."

## 🔍 Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Try a different port
PORT=5001 python app.py
# Then update API_URL in index.html to http://localhost:5001
```

### API Key Error
- Make sure you're using an Anthropic API key (starts with sk-ant-)
- Check that you have credits/quota available
- Verify key is entered correctly (no spaces)

### CORS Error
- Make sure backend is running on localhost:5000
- Try accessing from http://localhost not file://
- Check browser console for specific error

### No Results
- Check backend terminal for errors
- Verify API key has sufficient quota
- Try a simpler query first

## 📊 Understanding the Output

### Answer Format
The answer includes:
- Direct response to your question
- Specific numbers and statistics
- Source citations in [Source: ...] format

### Data Sources Section
Shows:
- Dataset name
- Source organization
- Link to original data on data.gov.in

### Raw Results (in API response)
Contains the actual data queried, useful for debugging

## 🎯 Best Practices for Demo

### Do:
✅ Start with simple queries, move to complex
✅ Highlight the source citations
✅ Show variety (comparison, top N, trends)
✅ Explain your design choices
✅ Keep energy high and pace quick

### Don't:
❌ Spend too long on code
❌ Get stuck debugging on camera
❌ Forget to show the citations
❌ Rush through the actual queries
❌ Go over 2 minutes

## 📝 Evaluation Criteria Mapping

| Criteria | How We Address It |
|----------|-------------------|
| **Problem Solving** | Shows data discovery, API integration, end-to-end flow |
| **System Architecture** | Clean separation: data layer, processing, presentation |
| **Accuracy** | Every answer includes specific numbers from data |
| **Traceability** | All claims linked to data.gov.in sources |
| **Data Security** | Deployed locally, no external data storage |

## 🎥 Final Checklist Before Publishing

- [ ] Video is under 2 minutes
- [ ] Audio is clear
- [ ] Shows working prototype
- [ ] Demonstrates 2-3 queries
- [ ] Highlights source citations
- [ ] Explains key design decisions
- [ ] Link is set to public
- [ ] Link works when you test it

## 🔗 Submission

After recording:
1. **Upload to Loom**
2. **Set visibility to "Public"** or "Anyone with link"
3. **Test the link** in incognito/private browser
4. **Copy the link**
5. **Submit it** in the challenge form

Good luck! 🚀
