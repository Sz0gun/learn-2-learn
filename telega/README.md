# Architecture from Etcd as backend
+------------------+                 +------------------+
|     Userbot      |                 |       Vault      |
|    (Pyrogram)    |  HTTPS/IPC/gRPC |   (Frontend API) |
+------------------+-----------------+------------------+
                                              |
       +------------------------------------------------+
       |                                                |
+------------------+         +------------------+        +------------------+
|     Etcd Node 1  |         |     Etcd Node 2  |        |     Etcd Node 3  |
|   (Key-Value DB) |  TLS    |   (Key-Value DB) |  TLS   |   (Key-Value DB) |
+------------------+         +------------------+        +------------------+

## **Userbot integration with HashiCorp Vault**

### **Main assumptions**

- Userbot will act as an intermediary between the application and Vault.
- Keys and secrets will be stored in Vault and available upon request.
- Communication with Vault will be via API, and the userbot will sends requests in response to commands.
- Storing keys and secrets in encrypted form. Support for auto-unseal and dynamic key generation.
- Apply Kubernetes NetworkPolicy so that the pod can only communicate with selected resources.
- Apply dynamic tokens for the userbot, refreshed by Vault.
- Create ACL policies in Vault and Etcd to minimize access.

### **TODO**

**Automation**
Deploy Vault and configure userbot uses Ansible.
**Monitoring**
Userbot interaction with Vault.
**Extensions**
CRUD keys in Vault on demand.

### **Required tokens**

- *Vault* encrypt it in secure env

### **Vault ↔ Etcd**
- Data encrypiton in-transit.
- Data encryption at-rest.

### **For consideration**
- Pyrogram MTProto Proxy
- Telethon p2p
- Inter-Process Communication (Unix Domain Sockets)
- Instead of using the HTTP API, use HashiCorp Vault SDK (data is transfred directly in aplication memory).


---

###  **Launching Userbot and Testing the Connection to Vault** 

####  **1. Starting Userbot** 

1. In the file`telega/session_keys.json`make sure you have the correct keys`api_id`and`api_hash`: : 
 
   ```json
   {
       "api_id": "123456",
       "api_hash": "abcdef1234567890"
   }
   ```

2. Generate a userbot session by running the script:

   ```bash
   python telega/generate_session.py
   ```
Follow the instructions in the terminal (e.g. enter your Telegram authorization code).

3. >>>todo Start userbot: 

   ```bash
   python telega/userbot.py
   ```

4. >>>todo Open Telegram and send a message to the userbot with the command`/get_keys`. If everything works correctly, the bot will respond: 
 
   ```
   API_ID: 123456
   API_HASH: abcdef1234567890
   ```

---

####  **2. Vault Configuration in the Local Environment** 

1.  **Set Vault environment variables:**  
 
`.env` in project root directory:
   ```env
   VAULT_ADDR=http://127.0.0.1:8200
   VAULT_TOKEN=your_token
   ```

2.  **Loading environment variables in Python:**  
 
>>>todo `userbot.py` code to load environment variables:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   VAULT_ADDR = os.getenv("VAULT_ADDR")
   VAULT_TOKEN = os.getenv("VAULT_TOKEN")
   ```

3.  **Storing keys in Vault:**  

Launch Vault in your development environment:
   ```bash
   vault server -dev
   ```

Log in to Vault:
   ```bash
   export VAULT_ADDR=http://127.0.0.1:8200
   export VAULT_TOKEN=your_token
   ```

Add Telegram API keys to Vault:
   ```bash
   vault kv put secret/telegram api_id=123456 api_hash=abcdef1234567890
   ```

4. **Testing your connection to Vault**

Check if Vault is working properly, use:
```bash
   curl --header "X-Vault-Token: your_token" http://127.0.0.1:8200/v1/sys/health
   ```
Expected result:
   ```json
   {
       "initialized": true,
       "sealed": false,
       "standby": false
   }
   ```

Check the keys stored in Vault:
```bash
   vault kv get secret/telegram
   ```