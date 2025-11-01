# 🔒 Security Guidelines - Project Samarth

## Overview
This document outlines security best practices and API key management for Project Samarth.

---

## 🔑 API Keys & Credentials

### Required API Keys

1. **Gemini AI API Keys** (2 keys recommended)
   - `SECRET_KEY` - Used for answer generation
   - `API_GUESSING_MODELKEY` - Used for query routing
   - Get from: https://aistudio.google.com/app/apikey
   - **⚠️ NEVER commit these to Git**

2. **MongoDB Connection String**
   - `DATABASE_URL` - MongoDB Atlas connection string
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/agri_qa_cache`
   - Get from: https://www.mongodb.com/cloud/atlas
   - **⚠️ Contains database password - NEVER expose**

3. **Data.gov.in API Key**
   - `DATA_GOV_API_KEY` - For accessing Indian government datasets
   - Get from: https://data.gov.in/catalogs
   - **⚠️ Has rate limits and quotas**

---

## 🛡️ Security Best Practices

### ✅ DO:

1. **Use Environment Variables**
   ```bash
   # Store credentials in .env file
   SECRET_KEY=your_actual_key_here
   ```

2. **Keep .env in .gitignore**
   ```gitignore
   .env
   .env.local
   .env.*.local
   *.env
   ```

3. **Use .env.example as Template**
   - Commit `.env.example` with placeholder values
   - Never put real credentials in `.env.example`

4. **Separate Keys for Dev/Prod**
   - Development: Use test/sample keys
   - Production: Use production keys with proper limits

5. **Rotate Keys Regularly**
   - Change API keys every 3-6 months
   - Immediately rotate if exposed

6. **Use Different Keys per Environment**
   - Local development
   - Staging
   - Production

### ❌ DON'T:

1. **Never Hardcode Credentials**
   ```python
   # ❌ BAD
   API_KEY = "AIzaSyCF0sJdvYgEd_lm..."
   
   # ✅ GOOD
   API_KEY = os.getenv('SECRET_KEY')
   ```

2. **Never Commit .env Files**
   - Check `.gitignore` before every commit
   - Use `git status` to verify

3. **Never Share Keys Publicly**
   - Don't post in Discord, Slack, email
   - Don't include in screenshots/videos
   - Don't paste in GitHub issues

4. **Never Use Production Keys in Testing**
   - Use separate test keys
   - Use mock data when possible

---

## 📁 File Security Status

### ✅ Secured (No real credentials exposed):

- ✅ `.env.example` - Template only
- ✅ `frontend/.env.example` - Template only
- ✅ `README.md` - Placeholder values
- ✅ `QUICK_REFERENCE.md` - Placeholder values
- ✅ `docs/SYSTEM_ARCHITECTURE.md` - Placeholder values
- ✅ `docs/QUICKSTART.md` - Placeholder values
- ✅ `docs/MONGODB_CACHING.md` - Placeholder values
- ✅ `src/config/settings.py` - Reads from env only

### 🔒 Protected (Real credentials, but NOT in Git):

- 🔒 `.env` - **In .gitignore** ✓
- 🔒 `frontend/.env` - **In .gitignore** ✓

### ⚠️ Test Files (Sample keys for testing):

Test files in `test/api_tests/` contain a public sample Data.gov.in key:
- `579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b`
- This is a **rate-limited public demo key**
- Only allows 10 records per request
- **Replace with your own key for production use**

---

## 🚨 What to Do If Keys Are Exposed

### If you accidentally commit API keys:

1. **Immediately Rotate Keys**
   - Generate new Gemini API keys
   - Update MongoDB password
   - Get new Data.gov.in key

2. **Remove from Git History**
   ```bash
   # Use BFG Repo Cleaner or git filter-branch
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force Push (Dangerous!)**
   ```bash
   git push origin --force --all
   ```

4. **Update All Environments**
   - Update `.env` locally
   - Update Render/Vercel environment variables
   - Restart all services

---

## 🔍 Pre-Commit Checklist

Before every `git commit` and `git push`:

- [ ] Check `git status` output
- [ ] Verify `.env` is NOT listed
- [ ] Review changed files for hardcoded secrets
- [ ] Run: `grep -r "AIza" . --exclude-dir=.git --exclude-dir=node_modules`
- [ ] Run: `grep -r "mongodb+srv://" . --exclude-dir=.git --exclude-dir=node_modules`
- [ ] Verify only `.env.example` files are being committed

---

## 🌐 Deployment Security

### Vercel (Frontend)
- Set environment variables in dashboard
- Use `VITE_` prefix for frontend vars
- Never expose backend keys to frontend

### Render/Railway (Backend)
- Set environment variables in dashboard
- Use secrets management feature
- Enable auto-deploy only after testing

### MongoDB Atlas
- Whitelist specific IPs only
- Use strong passwords (20+ chars)
- Enable monitoring and alerts
- Use separate users for dev/prod

---

## 📊 Environment Variable Matrix

| Variable | Frontend | Backend | Example Template | Public? |
|----------|----------|---------|------------------|---------|
| `VITE_API_URL` | ✅ | ❌ | `http://localhost:8000` | ✅ Yes |
| `SECRET_KEY` | ❌ | ✅ | `your_gemini_key_here` | ❌ NO |
| `API_GUESSING_MODELKEY` | ❌ | ✅ | `your_gemini_key_here` | ❌ NO |
| `DATABASE_URL` | ❌ | ✅ | `mongodb+srv://user:pass@...` | ❌ NO |
| `DATA_GOV_API_KEY` | ❌ | ✅ | `your_data_gov_key_here` | ❌ NO |

---

## 🔧 Tools for Security

### 1. Git-Secrets
Prevent committing secrets:
```bash
git secrets --install
git secrets --register-aws
```

### 2. GitGuardian
Automated secret detection in repos

### 3. TruffleHog
Find secrets in Git history:
```bash
truffleHog --regex --entropy=False .
```

### 4. Pre-commit Hooks
```bash
# .git/hooks/pre-commit
#!/bin/sh
if git diff --cached | grep -E "AIza|mongodb\+srv://"; then
    echo "⚠️  Potential API key detected!"
    exit 1
fi
```

---

## 📞 Contact

If you discover a security vulnerability:
- **DO NOT** open a public GitHub issue
- Contact repository owner privately
- Allow time for patching before disclosure

---

## ✅ Security Audit Status

**Last Updated**: November 1, 2025

**Status**: ✅ All credentials secured and moved to environment variables

**Files Audited**: 
- 547 total files
- 43 markdown documentation files
- 28 Python source files
- All test files reviewed

**Action Items Completed**:
- ✅ Removed all real API keys from documentation
- ✅ Updated all examples to use placeholders
- ✅ Verified `.env` is in `.gitignore`
- ✅ Confirmed `.env` not tracked by Git
- ✅ Updated `settings.py` to require env vars
- ✅ Created security documentation

---

**Remember: Security is not a one-time task, it's an ongoing practice! 🛡️**
