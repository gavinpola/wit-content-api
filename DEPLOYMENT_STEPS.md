# 🚀 Step-by-Step Railway Deployment Guide

## **Phase 1: GitHub Repository Setup**

### **Step 1: Create GitHub Repository**
1. **Go to [github.com](https://github.com)**
2. **Click "New repository"**
3. **Repository name**: `wit-content-api`
4. **Description**: `Production API for Wit content generation`
5. **Make it Public** (Railway works better with public repos)
6. **Don't initialize** with README (we already have one)
7. **Click "Create repository"**

### **Step 2: Push Your Code**
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/wit-content-api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## **Phase 2: Railway Deployment**

### **Step 3: Deploy to Railway**
1. **Go to [railway.app](https://railway.app)**
2. **Sign up** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `wit-content-api` repository**
6. **Click "Deploy"**

### **Step 4: Wait for Deployment**
- Railway will automatically:
  - Install dependencies from `api_requirements.txt`
  - Start the server using `railway_deploy.py`
  - Set up HTTPS and domain
- **Wait 2-3 minutes** for deployment to complete

### **Step 5: Get Your API URL**
1. **Click on your project** in Railway dashboard
2. **Go to "Settings" tab**
3. **Copy your domain** (e.g., `https://wit-content-api-production.up.railway.app`)
4. **This is your new API base URL**

## **Phase 3: Test Your API**

### **Step 6: Test Health Endpoint**
```bash
curl https://your-railway-url.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-XX...",
  "version": "2.0.0",
  "environment": "production"
}
```

### **Step 7: Test Question Generation**
```bash
curl -X POST https://your-railway-url.railway.app/generate-questions \
  -H "Content-Type: application/json" \
  -d '{"domain": "quant", "count": 5}'
```

## **Phase 4: Update n8n Workflows**

### **Step 8: Update All HTTP Request URLs**

**Replace all instances of:**
```
http://localhost:5000
```

**With your Railway URL:**
```
https://your-railway-url.railway.app
```

### **Step 9: Update Each Workflow**

**Workflow 1: Basic Question Generator**
- URL: `https://your-railway-url.railway.app/generate-questions`

**Workflow 2: Bulk Question Generator**
- URL: `https://your-railway-url.railway.app/generate-bulk-questions`

**Workflow 3: Daily Challenge Generator**
- URL: `https://your-railway-url.railway.app/generate-daily-challenge`

### **Step 10: Test n8n Connection**
1. **Go to your n8n dashboard**
2. **Open any workflow**
3. **Click "Test step"** on the HTTP Request node
4. **Should return success** instead of timeout/connection refused

## **Phase 5: Production Testing**

### **Step 11: Run Small Test**
1. **Activate a workflow** with small count (e.g., 10 questions)
2. **Monitor the execution**
3. **Check Supabase** for new questions
4. **Verify no timeouts**

### **Step 12: Scale Up**
1. **Increase question count** gradually
2. **Test bulk generation** (1000+ questions)
3. **Test daily challenge generation**
4. **Monitor performance**

## **🎯 Success Checklist**

- [ ] GitHub repository created and pushed
- [ ] Railway deployment successful
- [ ] Health endpoint returns 200
- [ ] Question generation works
- [ ] n8n workflows updated with new URLs
- [ ] n8n can connect without timeouts
- [ ] Small test workflow runs successfully
- [ ] Bulk generation works
- [ ] Daily challenges generate

## **🚨 Troubleshooting**

### **If Railway deployment fails:**
- Check `api_requirements.txt` is correct
- Verify `railway_deploy.py` has no syntax errors
- Check Railway logs for specific errors

### **If n8n still can't connect:**
- Verify Railway URL is correct
- Check CORS settings (should be enabled)
- Test with curl first
- Check Railway logs for errors

### **If questions aren't generating:**
- Check Supabase connection in n8n
- Verify table name is "questions"
- Check Supabase logs for errors

## **🎉 You're Live!**

Once all steps are complete:
- ✅ **Your API is running 24/7**
- ✅ **n8n can access it reliably**
- ✅ **No more localhost issues**
- ✅ **Ready for 10k questions and 2 years of daily challenges**

**Your production system is now online!** 🚀 