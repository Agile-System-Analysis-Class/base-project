# Requirements

- OS Requirements - one that supports Docker Desktop, windows will require hyper-v
  - Rare instances where you need to re-enable hyper-visor if you disabled it to run say Valorant. Use this command: `bcdedit /set hypervisorlaunchtype auto`, set it to `off` if you play games like valorant to reenable the anti-cheat.
- Python 3.11 (make sure pip works from the commandline - python package manager)
- Python packages: nose2 (for testing) `pip install nose2`

# Setting up and building docker environment

- Download docker desktop for your preferred os
- Git clone this repository
- Run `docker-compose build` to build the container, packages in that container, etc...

## mysql settings
- Rename `app/.env.rename` to `app/.env` and `app/.mysql.env.rename` to `app/.mysql.env`

- Inside the mysql file is the table you'll use, we use an example setup, but don't change the host as this allows docker's db to communicate to fastapi

(Note: any mysql config option prefixing with `MYSQLDB_` is an internal setting `MYSQL_` is a docker setting for the container. Also this environment was tuned for this demo and nothing more)

## setting up & running the application

- Note: delete `.setup_complete` when rerunning this on an existing setup if you're trying to nuke all the data else creating tables won't run

- We need to spin up our environment, so run `docker-compose up -d` this will spin up your environment into a docker container and you can visit the website using `http://127.0.0.1:8000` - if things worked correctly you should be shown an error message.

- (Note: Make sure the database is fully started before proceeding with this step.) Now you need to visit `http://127.0.0.1:8000/env_setup` - the first time you visit this page it will setp all database tables and creat the first admistrator account with the credentials `root:abc123`.

- To login visit the index page or `http://127.0.0.1:8000/login` to login with the root account. The root account allows you to generate the data

## generate data with root

- After you login with the root account press the generate button. This will truncate all data except the root account and create example professor data that the administrator can use to test the systems in place

- Once redirected or the page is refreshed you should see all the professors, the courses they teach and the students under each course they teach. You can keep regenerating this data if you like. 

## Logging in with professor account

(Note: Student passwords are: `abcd` and professors are: `1234`)

- Since the professor and student account is simulated, you'll have predefined courses when you are prompted to your dashboard.

- The dashboard will lead you to your courses. Inside these courses you will see the access token generation link and the students registered to that course you teach. Next to each student are checkboxes that allows the professor to generate a attendance report for the selected users by pressing a submission button at the bottom of the form.

- The access code generation page you can endlessly generate a new token which is used for those students to check in to the start time for their course when that course starts for the day between the start/finish dates. Clicking generating will generating a new token for just that course.

- TBD: Explaining attendance reports as its not implemented yet

## Logging in with the student account

(Note: Student passwords are: `abcd` and professors are: `1234`)

- Like the professor, you login with your student email and password. Then once complete, you will be prompted to all the pregenerated courses you were registered to.

- Once you click on a course, you are presented with your attendance information for that course and the option to check in to attend that class for the day.

- On the checkin page the student is presented a box to enter the access token and a submit button to check in for that course.

That's the limit to this demo.

## Running tests

- Install `nose2` with `pip` locally
- Then travel to the root folder and run `nose2` command. it'll run all the tests in the tests folder
