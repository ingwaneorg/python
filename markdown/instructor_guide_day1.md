# Day 1 Instructor Guide: ETL Foundations in Python

## Session Overview
**Duration**: 6.5 hours (9:30-16:00)
**Objective**: Build complete ETL pipeline from scratch using Python
**Outcome**: Every learner completes a working Extract-Transform-Load solution

---

## Pre-Session Setup (15 mins before start)

### **Technical Checklist:**
- [ ] VM environment accessible to all learners
- [ ] SQL Server instance running (localhost connection)
- [ ] Jupyter Notebooks functional
- [ ] Python libraries available: pandas, requests, pyodbc
- [ ] Internet connectivity for API calls
- [ ] VS Code available for L3 learners

### **Materials Checklist:**
- [ ] Customer cleaning lab (all tiers L1/L2/L3)
- [ ] API enrichment lab 
- [ ] Database loading lab
- [ ] Solution notebooks ready
- [ ] Discussion question cards

---

## Session Timeline & Facilitation Guide

### **Opening (9:30-9:45) - 15 mins**

**Frame the Day:**
> "Today you're building a complete ETL pipeline that solves a real business problem. By lunch, you'll have cleaned messy customer data. By day's end, you'll be pulling live data from APIs and loading it into a database."

**Key Messages:**
- ETL from hour 1 (not theory first)
- Python is the tool, ETL is the skill
- Three difficulty levels available
- Real business scenarios throughout

**Tier Selection Process:**
1. Explain three tiers briefly (2 mins)
2. Let learners self-select
3. Emphasize flexibility to change levels

---

### **Morning Session 1: Transform Focus (9:45-11:00) - 75 mins**

#### **Opening Hook (5 mins)**
Show the messy customer data:
> "This is what real data looks like. Your job: make it usable for business."

#### **Lab Introduction (10 mins)**
- Business scenario: CRM data quality project
- Success criteria: clean, validated, reportable data
- Quality metrics matter (not just completion)

#### **Hands-on Lab (50 mins)**
**L1 Track (Guided):**
- Pair them up if possible
- Walk through first 2 examples together
- Check every 15 mins, provide hints
- Focus on concept understanding over syntax

**L2 Track (Semi-Independent):**
- Brief requirements overview
- Check every 20 mins
- Help with logic, not syntax
- Encourage experimentation

**L3 Track (Advanced):**
- Full requirements only
- Available for architecture discussions
- Challenge with edge cases
- May finish early (mentoring opportunity)

#### **Common Issues & Solutions:**
- **pandas syntax errors**: Point to examples, don't fix for them
- **Logic confusion**: Ask "what should happen?" before "how to code it"
- **L1 learners stuck**: Pair with L2 learner
- **L3 learners finished early**: Code review with others

#### **Wrap-up (10 mins)**
Quick wins celebration:
- "Show one data quality issue you fixed"
- "What business impact does clean data have?"

---

### **Break (11:00-11:20) - 20 mins**

**Informal Check-ins:**
- How are the tiers working?
- Any technical issues?
- Confidence levels?

---

### **Morning Session 2: Extract Focus (11:20-12:30) - 70 mins**

#### **Bridge from Transform (5 mins)**
> "You've cleaned internal data. Now let's enrich it with external sources - this is the Extract component."

#### **API Integration Lab (55 mins)**
**Key Teaching Moments:**
- **API failures are normal** - show error handling
- **Rate limiting matters** - explain delays between calls
- **Business logic applies** - not just technical integration

**Facilitation Strategy:**
- **First 15 mins**: Everyone does postcode API together
- **Next 30 mins**: Independent enrichment work
- **Last 10 mins**: Results comparison and discussion

#### **Discussion Points (10 mins)**
*"How does your organisation currently get external data? Manual lookup? Automated? What could be automated?"*

**Facilitation Tips:**
- Let them share experiences first
- Connect to workplace scenarios
- Avoid technical "quiz" questions

---

### **Lunch (12:30-13:30) - 60 mins**

**Lunch Learning (Optional):**
- Leave solution notebooks available
- Encourage peer comparison of approaches
- Address any morning issues

---

### **Afternoon Session 1: Load Focus (13:30-14:45) - 75 mins**

#### **Complete the ETL Story (5 mins)**
> "Extract ✅ Transform ✅ Now for Load - getting data into your data warehouse."

#### **Database Loading Lab (60 mins)**
**Critical Teaching Points:**
- **Upsert logic** - handle existing records gracefully
- **Error handling** - one bad record shouldn't break everything
- **Audit trails** - production systems need tracking
- **Performance** - batch operations vs. row-by-row

**Common Student Challenges:**
- **SQL syntax errors**: Provide working examples, focus on concepts
- **Connection issues**: Have standard connection string ready
- **Performance concerns**: Explain it's demo data, production is different

#### **Business Value Discussion (10 mins)**
*"You now have enriched customer data in your database. How would different teams in your organisation use this?"*

**Expected Responses:**
- Customer support: Better context
- Sales: Lead qualification
- Marketing: Segmentation
- Risk: Proactive management

---

### **Break (14:45-15:05) - 20 mins**

---

### **Afternoon Session 2: Integration & Reflection (15:05-16:00) - 55 mins**

#### **Complete Pipeline Demonstration (15 mins)**
- Run end-to-end pipeline
- Show business intelligence queries
- Highlight audit trails and monitoring

#### **ETL Concepts Consolidation (15 mins)**
**Structured Discussion:**
1. "What did Extract involve?" (APIs, data sources)
2. "What did Transform involve?" (Cleaning, business logic)
3. "What did Load involve?" (Database operations, quality checks)
4. "How do these connect?" (Pipeline thinking)

#### **Tomorrow's Bridge (10 mins)**
> "Tomorrow: Same pipeline, different tool. You'll rebuild this in Azure Data Factory and see how ETL concepts apply across platforms."

#### **Reflection & Wrap-up (15 mins)**
**Individual Reflection (5 mins):**
- Biggest learning today?
- What will you try at work?
- What was most challenging?

**Group Share (10 mins):**
- Volunteer sharing only
- Focus on insights, not just completion

---

## Troubleshooting Guide

### **Technical Issues**

**API Timeouts:**
- Expected behavior, show error handling
- Use as teaching moment about production resilience

**SQL Connection Problems:**
- Have localhost connection string ready
- Check SQL Server service is running
- Provide alternative SQLite option if needed

**Python Errors:**
- Don't debug live unless critical
- Point to working examples
- Focus on understanding over perfect syntax

### **Engagement Issues**

**L1 Learners Overwhelmed:**
- Pair with stronger peer
- Focus on guided sections only
- Celebrate small wins frequently

**L3 Learners Bored:**
- Provide extension challenges
- Ask them to mentor others
- Code review discussions

**Mixed Progress:**
- Normal and expected
- Use faster learners as peer mentors
- Ensure everyone achieves minimum viable ETL

### **Discussion Facilitation**

**Dead Silence:**
- Ask specific workplace questions
- Share your own experience first
- Use think-pair-share format

**Technical Debates