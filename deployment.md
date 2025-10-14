# Deployment Guide

1. Install system dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

2. Create and configure PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE open_heavens_db;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE open_heavens_db TO myuser;
\q
```

3. Clone the repository and set up Python environment:
```bash
git clone <your-repo-url>
cd Open-Heavens
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. Set up your environment variables in `.env`:
```
DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/open_heavens_db"
API_KEY="your-production-api-key"
```

5. Initialize the database:
```bash
psql "$DATABASE_URL" -f sql/init_schema.sql
python migrate_all_tables.py
```

6. Create a systemd service for your application:
```bash
sudo nano /etc/systemd/system/openheavens.service
```

Add the following content:
```ini
[Unit]
Description=Open Heavens FastAPI Application
After=network.target

[Service]
User=your-user
Group=your-user
WorkingDirectory=/path/to/Open-Heavens
Environment="PATH=/path/to/Open-Heavens/venv/bin"
EnvironmentFile=/path/to/Open-Heavens/.env
ExecStart=/path/to/Open-Heavens/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

7. Configure Nginx as a reverse proxy:
```bash
sudo nano /etc/nginx/sites-available/openheavens
```

Add the following configuration:
```nginx
server {
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

8. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/openheavens /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. Start your application:
```bash
sudo systemctl start openheavens
sudo systemctl enable openheavens
```

10. Set up SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Remember to:
- Keep your production API keys secure
- Set up proper firewalls
- Configure regular database backups
- Monitor your application logs
- Update your dependencies regularly