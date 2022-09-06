# Environment setup

### This is currently haphazard, mostly just putting reference for a later data, when I will format this well.

## **Requirements**

- [Visual Studio Code](https://code.visualstudio.com/) (*Highly reccomended for this stack*)

- [anaconda3 Distribution](https://www.anaconda.com/products/distribution)

- [Docker](https://www.docker.com/)
    - I recommend you utilize VSCode's Docker extension, to easily build and compose containers from within Code.

- ~~[NPM via node.js](https://nodejs.org/en/download/)~~

## **Steps**

### Conda

*With Linux, skip the anaconda3 PS prompt and init from VS Code/any terminal.*

1) Press your Windows Key, and type "anaconda power". You should see a "Anaconda Powershell Prompt" appear. Open the shell, and type the following commands in sequence "`conda update conda`", "`conda init`". This will allow conda to access libraries properly from Powershell/CMD. Note that you may have to prepend a `_` to any `conda` commands. You can rename the executable to change this.

2) Open VSC, and clone your forked repository locally. Open the cloned project, and ensure you are working from a newly created branch.

3) Open the terminal, and confirm that conda has loaded the base environment into your shell (you will see a `(base)` somewhere in your command prompt if so).

4) Ensuring you are within the `raptor-web` top level directory in your terminal, run the following command; `conda env create`. This will read the `environment.yml` file and set up a conda environment with the required dependencies.

5) In the same terminal, ater creating the `djangoWork` environment from the configuration, run the following command; `conda activate djangoWork`. This will activate the created virtual environment. __You need to run this command each time you begin work.__

6) Run the following commands in sequence to initialize the database; `python manage.py migrate, python manage.py makemigrations raptormc, python manage.py migrate, python manage.py shell`. Run these commands again any time you make changes to Models.

7) If you ever install a new module, use `pip`, and add it to the `environment.yml` file under the `pip:` category, in the same format as the other packages. `<package-name>=<version>`.

### Running dockerized environment

1) `compose up` the `docker-compose.yml` file located in the top level directory. This will do the following

    - Run a MariaDB container. This stores/persists it's data into a `raptor-db` docker volume.
    - Build and run a container of the RaptorMC website/application, running on asynchronous webserver `daphne`. This container servers `http` over port 80 in the docker network.
    - Build and run a container of the "RaptorBot" Discord Bot, which performs some actions on behalf of the web application on the Discord server.
    - Run a nginx container. This container binds to port 443 on the host, and proxies `https` requests to the RaptorMC/django application

### Setting up RaptorBot

1) Ensure you create a `.env` file at `raptorBot/.env`, with the following content and format;

        DISCORD_TOKEN=<'token'>

    Be sure to include the quotes around the token!

### Other things

1) To use the MySQL/MariaDB driver, you must run `sudo apt update` and `sudo apt install libmariadb-dev`. Windows behavior here is undetermined.

2) Create a `.env` file at both `/config/db/.env` and `raptorWeb/raptorWeb/.env`. Ensure they both have the exact same content, and that they are formatted like such;

        MYSQL_PASSWORD=<password>
        MYSQL_ROOT_PASSWORD=<strongerpassword>
        MYSQL_DATABASE=raptormc (keep this table name)
        MYSQL_USER=<username>
        BASE_PATH=/tmp

### NPM

- **Front end tooling not established**