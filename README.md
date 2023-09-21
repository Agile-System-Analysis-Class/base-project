# Requirements

- Docker Windows
- Hyper-V enabled

- Rare instances where you need to re-enable hyper-visor if you disabled it to run say Valorant. Use this command: `bcdedit /set hypervisorlaunchtype auto`, set it to `off` if you play games like valorant to reenable the anti-cheat.

# Spinning up environment

- Rename the `.env` files -> .env.rename -> .env, .mysql.env.rename -> .mysql.env 

`docker-compose up -d`

# Updating requirements

`docker-compose build`

