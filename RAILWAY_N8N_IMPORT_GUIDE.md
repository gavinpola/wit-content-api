# 🚀 Railway n8n Workflow Import Guide

## **✅ Your Railway API is Ready!**

**Railway URL**: `https://web-production-9dfd.up.railway.app`

## **📁 Available Workflow Files**

I've created **5 complete n8n workflows** configured for your Railway API:

### **Individual Workflow Files:**
1. **`workflow_1_basic_generator_railway.json`** - Basic question generation (every 2 hours)
2. **`workflow_2_bulk_generator_railway.json`** - Bulk question generation (10k questions)
3. **`workflow_3_daily_challenge_railway.json`** - Daily challenge generation (every hour)
4. **`workflow_4_bulk_daily_challenges_railway.json`** - 2 years of daily challenges
5. **`workflow_5_progress_monitor_railway.json`** - Progress monitoring (every 6 hours)

### **Combined File:**
- **`all_railway_workflows.json`** - All 5 workflows in one file

---

## **🔧 Import Instructions**

### **Option 1: Import Individual Workflows**
1. **Go to your n8n dashboard**
2. **Click "Import from file"**
3. **Select any individual workflow file** (e.g., `workflow_1_basic_generator_railway.json`)
4. **Click "Import"**
5. **Repeat for each workflow**

### **Option 2: Import All at Once**
1. **Go to your n8n dashboard**
2. **Click "Import from file"**
3. **Select `all_railway_workflows.json`**
4. **Click "Import"**
5. **All 5 workflows will be imported**

---

## **⚙️ Configure Supabase Connection**

After importing, you need to configure the Supabase nodes:

1. **Click on any Supabase node**
2. **Click "Add Credential"**
3. **Select "Supabase"**
4. **Enter your Supabase details:**
   - **URL**: Your Supabase project URL
   - **API Key**: Your Supabase anon key
5. **Click "Save"**
6. **Repeat for all Supabase nodes**

---

## **🧪 Test Your Workflows**

### **Step 1: Test Basic Generator**
1. **Open "Wit Basic Question Generator (Railway)"**
2. **Click "Test step"** on the HTTP Request node
3. **Should return success** with questions

### **Step 2: Test Small Bulk**
1. **Open "Wit Bulk Question Generator (Railway)"**
2. **Change `questions_per_domain` to 10** (for testing)
3. **Click "Execute Workflow"**
4. **Check Supabase** for new questions

### **Step 3: Test Daily Challenge**
1. **Open "Wit Daily Challenge Generator (Railway)"**
2. **Click "Test step"** on the HTTP Request node
3. **Should return success** with daily challenge

---

## **🎯 Workflow Descriptions**

### **1. Basic Question Generator**
- **Trigger**: Every 2 hours
- **Generates**: 50 quant questions
- **Difficulty**: Intermediate
- **Purpose**: Steady question generation

### **2. Bulk Question Generator**
- **Trigger**: Manual
- **Generates**: 10,000 questions across all domains
- **Purpose**: Reach your 10k goal quickly

### **3. Daily Challenge Generator**
- **Trigger**: Every hour
- **Generates**: 1 daily challenge for tomorrow
- **Purpose**: Daily challenges for 2 years

### **4. Bulk Daily Challenges Generator**
- **Trigger**: Manual
- **Generates**: 730 daily challenges (2 years)
- **Purpose**: Generate all daily challenges at once

### **5. Progress Monitor**
- **Trigger**: Every 6 hours
- **Purpose**: Monitor progress toward 10k goal

---

## **🚀 Ready to Start!**

1. **Import the workflows**
2. **Configure Supabase**
3. **Test each workflow**
4. **Activate the ones you want**

**Your Railway API is running 24/7 and ready to generate 10k questions and 2 years of daily challenges!** 🎉 