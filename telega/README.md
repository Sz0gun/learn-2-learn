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
