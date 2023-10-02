# Requirements

- Docker Windows
- Hyper-V enabled
- Rare instances where you need to re-enable hyper-visor if you disabled it to run say Valorant. Use this command: `bcdedit /set hypervisorlaunchtype auto`, set it to `off` if you play games like valorant to reenable the anti-cheat.

# Spinning up environment

- Clone this repository locally
- Open up your favorite command line prompt, I use git bash. personally
- Inside the folder where docker is located, rename the `.mysql.env.rename` file to `.mysql.env` 
- Change nothing as we're using dummy db/pw for this demo
- Head to the cli/command prompt and in the folder that contains the docker file type `docker-compose build` this will build the local container and install the requirements from the text file. 
- Once the environment is built, run `docker-compose up -d` And this will start your environment.

# Setting up the environment

- By default, your environment needs to be setup now, which for this demo is creating a dummy root account and the database tables by visiting `http://127.0.0.1:8000/env_setup`
- Once you create the db tables and setup the root account (`root:abc123`) you can now visit `http://127.0.0.1:8000/login` to login. If setup correctly else it'll show an error template.
- Once setup visit the dashboard and hit the generate button (note: again there's no html setup)

# Using generated data

- Professor passwords are: `1234` and the generated student passwords are `abcd`
- When complete it'll show the generated data on the dashboard. You can keep regenerating it currently.
    - When regenerating it'll truncate a lot of the data in the tables. 

# Using DataGrip

- Honestly you only need the `127.0.0.1` and the default MySQL port `3306` to connect to the local docker container's db and you can see all the data. Youtube how to use datagrip. 