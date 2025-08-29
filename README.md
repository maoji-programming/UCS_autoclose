# 🎫 Ticket Processing System - GUI Workflow

## 📌 Overview
This repository documents the process for handling tickets using the GUI interface. It supports validation and classification of tickets as **Normal Pass** or **ECN Pass**, and ensures proper logging and error handling throughout the workflow.

---

## 🚀 Workflow Summary

### 1. Serial Number Entry
- Users input:
  - **Org SN#** (Original Serial Number)
  - **New SN#** (New Serial Number)

### 2. Ticket Type Selection
- Choose one of:
  - `Normal Pass`
  - `ECN Pass`

### 3. Ticket Validation
- Search by **New SN#**
  - ❌ Error if ticket not found
  - ❌ Error if Org SN# does not match

### 4. ECN Type Check
- If ticket type is `ECN`, validate against ECN list:
  - ❌ Error if ECN selected but ticket is not ECN
  - ❌ Error if Normal Pass selected but ticket is ECN

---

## 🧪 Ticket Type Actions

### ✅ Normal Pass
- Check all items in **IRN list**
- In **ECN list**:
  - Conditional items → `Do not match the condition`
- Fill **Repair Detail**:
  - `Claim Group`: NBZU00 – Software / OS error  
  - `Claim Code`: NBZU99 – Other OS(Software) issues  
  - `Problem Group`: N0Z000 – Test ok  
  - `Problem Code`: N0Z000 – Test ok  
  - `Action Group`: N – NTF  
  - `Action Code`: N05 – Cannot duplicate the symptom

### ✅ ECN Pass
- Check all items in **IRN list**
- In **ECN list**:
  - Conditional items → `Do not match the condition`
  - Mandatory items → `Part Shortage`
- Fill **Repair Detail**:
  - `Claim Group`: NBZU00 – Software / OS error  
  - `Claim Code`: NBZU01 – Boot hangs at ASUS logo  
  - `Problem Group`: N0FZ00 – Other Error  
  - `Problem Code`: N0FZZZ – Inspection Fail  
  - `Action Group`: F – Repair Failed  
  - `Action Code`: F20 – Cannot duplicate the symptom  
  - `Org PN`: (from ticket)
- Click **Memo** → Enter: `Sent to ECN(pass)` in Problem Description

---

## ✅ Final Steps

1. Click **Next**
2. Check **WTP Result**:
   - ✅ If passed → Click `Confirm result`
   - ❌ If failed → Error: "Test not finished"
3. Alternatively, click `Confirm result` directly
4. When prompted: “Do you want to move to Ship state?” → Click **No**
5. Complete the ticket

---

## 📄 Logging

Append a row to `excel.txt` with the following fields:

| Field         | Description                  |
|---------------|------------------------------|
| Org SN        | Original Serial Number       |
| New SN        | New Serial Number            |
| RMA Number    | RMA Identifier               |
| UCS Status    | UCS System Status            |
| Closed Time   | Timestamp of closure         |
| Status        | Final ticket status          |
| Reason        | Reason (if applicable)       |

---

## 🛠 Requirements
- GUI access
- ECN and IRN lists
- Excel logging capability

## 📬 Contact
For issues or questions, please contact the support team or open an issue in this repository.
