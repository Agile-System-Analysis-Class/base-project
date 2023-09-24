# Requirements

- Docker Windows
- Hyper-V enabled
- Rare instances where you need to re-enable hyper-visor if you disabled it to run say Valorant. Use this command: `bcdedit /set hypervisorlaunchtype auto`, set it to `off` if you play games like valorant to reenable the anti-cheat.

# Spinning up environment

- Build source code before running docker `docker-compose build`

- Rename the `.env` files -> .env.rename -> .env, .mysql.env.rename -> .mysql.env 

- Spin up docker - `docker-compose up -d`