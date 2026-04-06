## 🍯 HoneyTrap

![honeypot image](assets/banner.png)

`HoneyTrap` is a `Python`-based honeypot that supports multiple protocols (`HTTP` & `SSH`).  
It is designed to attract attackers or automated bots, track their activities, analyze their methodologies, and help protect systems from such threats.

---
## 🖥️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Arunachalam-1435/Honeytrap.git
```
### 2. Create SSH keys
```bash
ssh-keygen -t rsa -b 2048 -f server.key
```
### 3. Choose how to run the honeypot
You have two options:
- Run locally
- Run using Docker
## ▶️ Run Locally
### 4. Create a Python virtual environment and install dependencies

```bash
python3 -m venv .env  
source .env/bin/activate  
pip install -r requirements.txt
```
### 5. Give execution permission and run
```bash
chmod +x start-up.sh
./start-up.sh
```
This will start both `SSH` and `HTTP` honeypots in the background.
To verify:
```bash
ps aux | grep "python"
```
To stop:
```bash
kill <pid_of_each_honeypot_process>
```


---

## 🐳 Run with Docker
Ensure Docker is installed, then:
### Build image
```bash
docker build -t honeytrap .
```
### Run container
```bash
docker run -p 2222:2222 -p 8080:8080 -d honeytrap
```
## 💡 Usage

### 🏳️ `HoneyTrap` Flags
| Flag     | Description                                                               |
| -------- | ------------------------------------------------------------------------- |
| `--help` | Show help message                                                         |
| `-a`     | Set IP address (required)                                                 |
| `-p`     | Set port (required)                                                       |
| `-u`     | Set custom username (optional). Default: `username` (SSH), `admin` (HTTP) |
| `-pw`    | Set custom password (optional). Default: `password`                       |
| `--ssh`  | Run SSH honeypot                                                          |
| `--web`  | Run HTTP honeypot                                                         |
## 📁 Logging Files

- `audit.log` → Logs SSH usernames and passwords
- `cmd_audit.log` → Logs commands executed in SSH honeypot
- `http_audit.log` → Logs HTTP honeypot activity

---
## 📔 Future Features
- Integrate `ELK Stack` (Elasticsearch, Logstash, Kibana) to:
    - Visualize live attacks
    - Analyze credentials and commands
    - Monitor attacker behavior
- Implement `Docker Compose` to:
    - Run multiple services together
    - Simplify deployment on a VPS

---

## 📎 References
This honeypot was inspired by a tutorial by **Grant Collins**:  
<iframe width="560" height="315" src="https://www.youtube.com/embed/gDjDxS55890?si=EJeqcdHpU3Lw91ii" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
The Docker setup was independently designed to simplify deployment.