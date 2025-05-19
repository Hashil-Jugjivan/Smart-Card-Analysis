# Smart Card Analysis 🚋🔐


## Overview

This project demonstrates the security features, data interaction mechanisms, and vulnerability considerations of chip-based smart cards such as **MIFARE Ultralight**, **MIFARE Classic**, and **CEPAS (NETS FlashPay)** cards. Using Python and the `pyscard` library, the code interfaces directly with smart card readers to extract, analyze, and interpret memory blocks, purse balances, and transaction logs.

Smart cards are critical in digital payment systems and secure access control, and this project illustrates how attackers and security analysts can interact with such cards at a low level using APDU (Application Protocol Data Unit) commands.

## Features

✅ **Read Smart Card UID**  
✅ **Query Purse Balance (NETS FlashPay)**  
✅ **Extract & Interpret Transaction Logs**  
✅ **APDU Command Transmission**  
✅ **MIFARE Ultralight Data Read/Write**  
✅ **Demonstrate XOR/XNOR Error Detection**  
✅ **Authentication and Memory Access on MIFARE Classic**

## 📂 Project Structure

```bash
.
├── smart_card.py              # Python script to interact with smart cards
├── CPS Smart Card Report.pdf  # Detailed lab report and documentation
```

## 🚀 How It Works

The script performs the following:

1. Detects connected smart card readers
2. Connects to a selected reader
3. Sends APDU commands to:
   - Retrieve UID (`FF CA 00 00 00`)
   - Read stored balance (`90 32 03 00 00`)
   - Fetch transaction logs (`90 32 03 00 01 00 00`)
4. Converts hex responses into human-readable balance and transaction types:
   - **MRT Payment** (`0x30`)
   - **Bus Payment** (`0x31`)
   - **Offline Top-up** (`0x75`)
   - **Bus Refund** (`0x76`)
5. Decodes ASCII data for enhanced traceability

## 🛠 Setup & Requirements

**Dependencies**
- Python 3.x
- [pyscard](https://pypi.org/project/pyscard/)

```bash
pip install pyscard
```

**Hardware**
- USB Smart Card Reader (e.g. ACS ACR 1281)
- MIFARE or NETS FlashPay Card

## 📊 Sample Output

```plaintext
Available smart card readers:
ACS ACR1281 1S Dual Reader PICC 0

Response: 04 62 0E C2 98 11 94
Balance = $10.08

Offline Value Add
Amount = $5.00
Date: ['20', '01', '01', '10']
Merchant: SBS Transit

MRT Payment
Amount = $-1.23
Date: ['20', '01', '01', '11']
Merchant: SMRT
```

## 🔒 Security Concepts Explored

- **Sector Authentication** (Key A/Key B in MIFARE Classic)
- **Error Detection using XOR/XNOR**
- **Secure APDU Formatting**
- **Two’s Complement Handling** for negative transaction values
- **Memory Organisation** (Page vs Block Structure)
- **Contactless Data Access over RF**

## 📘 Lab Report

The full technical and theoretical background of this project is available in the [CPS Smart Card Report (PDF)](./CPS%20Smart%20Card%20Report%20(Hashil%20Jugjivan)%20(1).pdf). It includes memory maps, sample ATRs, error handling logic, and manual APDU encoding.

## 🧠 Key Learning Points

- Distinguishing between **MIFARE Ultralight** and **Classic** security models
- Parsing smart card responses into real-world financial transactions
- Understanding how **low-level protocols (ISO 7816-4)** secure or expose card data
- Automation of forensic analysis on smart card data

## 📄 License

This project is provided for educational purposes only and should not be used to interact with production payment systems.
