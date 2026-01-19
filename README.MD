# Email Subject Line Performance Analysis

## Objective
This project identifies **high-performing email subject lines** using historical campaign data in a **statistically reliable** way.

Instead of running new A/B tests, we analyze past campaigns **as implicit experiments**, correcting for different send volumes and statistical uncertainty. The result is a ranked list of **subject line ideas** that can be confidently reused or prioritized.

---

## Input Data
Historical email campaign data with:
- **subject**: subject line text
- **sendings**: number of emails sent
- **opens**: number of opens
- **open_rate**: open rate (used for validation only)

Dataset size:
- ~5,900 subject records
- Send volumes range from 1 to ~64 million

---

## Methodology

### 1. Data Cleaning
- Kept only required columns
- Converted metrics to numeric types
- Removed invalid rows
- Ensured `opens ≤ sendings`

### 2. Minimum Send Threshold
To reduce noise, subject lines with fewer than **50 sendings** were removed.

This eliminates extreme outliers while preserving ~66% of the data.

### 3. Subject Line Standardization
Subject lines were standardized to evaluate **ideas, not formatting**:
- Converted to lowercase
- Removed all numbers
- Removed punctuation and extra whitespace
- Normalized text encoding

Example:

30% Discount Today  
90% Discount Today  

→ discount today

### 4. Merging Similar Subjects
After standardization:
- Subject lines that normalize to the same text were merged
- Sendings and opens were summed
- A representative subject with the highest send volume was kept

### 5. Performance Scoring
Subjects were ranked using the **Wilson Lower Bound score**, which:
- Accounts for both open rate and sample size
- Penalizes small samples automatically
- Produces reliable, volume-aware rankings

---

## Output
The final output is a ranked table containing:
- Subject line
- Total sendings
- Total opens
- Open rate
- Wilson lower bound score

Top-ranked subjects represent the most **statistically reliable historical performers**.

---

## Key Takeaway
This analysis answers one key question:

**Which subject line ideas have consistently performed best after accounting for volume and uncertainty?**

The results are statistically defensible and suitable for guiding future email campaign decisions.


