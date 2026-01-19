# Email Subject Line Performance Analysis

## 📌 Objective
The goal of this project is to identify **high-performing email subject lines** using historical campaign data in a **statistically reliable and decision-ready way**.

Instead of running new A/B tests, this analysis treats **past campaigns as implicit A/B tests**, while correcting for:
- Different send volumes
- Duplicate or very similar subject lines
- Statistical uncertainty in open rates

The result is a **ranked list of subject line ideas** that can be confidently reused or prioritized in future campaigns.

---

## 📊 Input Data
The analysis uses historical email campaign data with the following fields:

- **subject** – Email subject line text  
- **sendings** – Number of emails sent  
- **opens** – Number of opens  
- **open_rate** – Open rate (used for validation only)

**Dataset characteristics**
- ~5,900 subject line records
- Extremely skewed send volume distribution  
  (from 1 send to more than 64 million sends)

---

## 🧹 Step 1 — Data Cleaning
We performed basic validation and cleaning to ensure correctness:

- Kept only required columns
- Converted metrics to numeric types
- Removed rows with missing or invalid values
- Ensured `opens ≤ sendings`
- Removed rows with zero or negative sendings

This guarantees the analysis is based only on **valid historical performance data**.

---

## ✂️ Step 2 — Minimum Send Volume Threshold
To reduce noise from very small samples, we analyzed the distribution of send volumes and applied a minimum cutoff:

### **Minimum sendings used: `50`**

**Why this threshold**
- Removes extreme noise (1–49 sends)
- Retains ~66% of the dataset
- Higher thresholds removed very little additional noise
- Preserves diversity while improving reliability

This balances **data quality** with **data coverage**.

---

## 🧠 Step 3 — Subject Line Standardization
Many subject lines differ only by numeric values:

Examples:
- “30% discount today”
- “90% discount today”

From a messaging perspective, these represent the **same idea**.

### Standardization rules:
- Convert text to lowercase
- Remove **all numbers**
- Remove punctuation and extra whitespace
- Normalize text encoding

Example transformation:

