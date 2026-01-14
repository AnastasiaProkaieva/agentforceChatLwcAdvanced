# Agentforce Connection Testing

Python scripts to test your Agentforce configuration independently from Salesforce.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agentforce/testing
pip install -r requirements.txt
```

### 2. Configure Credentials

Your credentials are already configured in `../env`:
- ✅ INSTANCE_URL
- ✅ CONSUMER_KEY
- ✅ CONSUMER_SECRET
- ✅ AGENT_ID

### 3. Run Tests

**Test in order:**

```bash
# Test 1: OAuth Authentication
python test_oauth.py

# Test 2: Session Creation (if Test 1 passes)
python test_session.py

# Test 3: Full Flow (if Test 2 passes)
python test_full_flow.py
```

---

## 📋 Test Scripts

### `test_oauth.py`
Tests OAuth authentication with your Connected App.

**What it tests:**
- Consumer Key/Secret validity
- OAuth token generation
- Connection to Salesforce instance

**Expected output:**
```
✅ SUCCESS! Got access token
🎉 OAuth Test PASSED
```

---

### `test_session.py`
Tests creating an Agentforce session.

**What it tests:**
- Agent ID validity
- Agent activation status
- Session creation API
- Remote Site Settings

**Expected output:**
```
✅ SUCCESS! Session created
   Session ID: abc123...
🎉 Agent Session Test PASSED
```

---

### `test_full_flow.py`
Tests complete conversation flow.

**What it tests:**
- OAuth authentication
- Session creation
- Sending messages
- Receiving responses

**Expected output:**
```
🤖 Agent Response:
   [1] Hello! I'm here to help...
🎉 ALL TESTS PASSED!
```

---

## 🐛 Common Issues

### Issue: OAuth Test Fails (401 Unauthorized)

**Cause:** Wrong Consumer Key or Secret

**Fix:**
1. Check `.env` file for typos
2. Verify credentials in Salesforce:
   - Setup → App Manager → Your Connected App
   - Manage Consumer Details
3. Copy credentials exactly (no spaces)

---

### Issue: Session Test Fails (404 Not Found)

**Cause:** Agent not found or wrong Agent ID

**Fix:**
1. Verify Agent ID in `.env`
2. Check agent exists:
   - Setup → Agents → Your Agent
   - Copy ID from URL
3. Ensure agent is ACTIVATED

---

### Issue: Session Test Fails (500 Error)

**Cause:** Missing Remote Site Settings

**Fix:**
1. Setup → Remote Site Settings → New
2. Add these sites:
   ```
   Name: AgentforceAPI
   URL: https://api.salesforce.com
   Active: ✓
   
   Name: SalesforceAuth
   URL: https://login.salesforce.com
   Active: ✓
   ```

---

### Issue: Connection Errors

**Cause:** Network or firewall issues

**Fix:**
1. Check internet connection
2. Verify you can reach:
   - https://api.salesforce.com
   - Your Salesforce instance URL
3. Check firewall/proxy settings

---

## 📊 Understanding Results

### ✅ All Tests Pass
Your Agentforce setup is working correctly! The issue is likely in:
- Salesforce component configuration
- Permission sets
- User access

### ❌ OAuth Fails
Problem with Connected App or credentials:
- Check Consumer Key/Secret
- Verify Connected App settings
- Check OAuth scopes

### ❌ Session Fails (but OAuth passes)
Problem with agent configuration:
- Check Agent ID
- Verify agent is activated
- Check agent has API connection
- Verify Remote Site Settings

### ❌ Message Fails (but session passes)
Problem with agent topics or actions:
- Check agent has topics configured
- Verify topics have actions
- Check agent is properly trained

---

## 🔍 Debug Mode

For more detailed output, modify any script and add:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🆘 Still Having Issues?

1. Run all three tests in order
2. Copy the error messages
3. Check the troubleshooting checklist in test output
4. Verify all Salesforce configuration steps

---

## 📚 Related Documentation

- **Main README**: `../../README.md`
- **Setup Guide**: `../data/SETUP.md`
- **Agentforce README**: `../README.md`

---

**Happy Testing! 🧪**
