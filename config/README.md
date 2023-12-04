# Configuring raptor-web

Before you can start the application successfully, you need to create a file with the filename `stack.env` in the same location of the `docker-compose-prod.yml` file, one directory above the directory this README file is in. Into the `stack.env` file, you need to copy the text within the code block below.

If you are deploying the application with [Portainer](https://www.portainer.io/), you can utilize the environment variable configuration Portainer offers to set these.

After doing so, you will need to put information into each element that does not have a value. If a key has a value, except `''`, **it MUST stay as it is**. If an element has a pair of quotes `''`, **you must enter your value inside of those quotes**. If the value is completely empty, enter your value without quotes. The exception to this is `LANGUAGE_CODE` and `TIME_ZONE`. Preferred defaults are set, but you may change them.

Below the code block you will find an explanation for each field, and what you should put in them.

```env
DJANGO_SECRET_KEY=''
DEBUG=
RUNNING_IN_DOCKER=
DOMAIN_NAME=''
ADMIN_BRAND_NAME=''
LANGUAGE_CODE='en-us'
TIME_ZONE='America/New_York'

USE_SQLITE=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=raptormc
MYSQL_USER=raptor
BASE_PATH=/tmp

DISCORD_OAUTH_APP_ID=
DISCORD_OAUTH_APP_SECRET=
DEFAULT_SUPERUSER_USERNAME=''
DEFAULT_SUPERUSER_EMAIL=''

DISCORD_BOT_TOKEN=''
DISCORD_BOT_DESCRIPTION=''

USE_CONSOLE_EMAIL=
ERROR_LOG_EMAIL=''
EMAIL_HOST=''
EMAIL_PORT=
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
```

# *General*

### **DJANGO_SECRET_KEY**
This value must be a long and random set of numbers, letters, and special characters. I recommend using a Password Generator from something like BitWarden to generate these values. There are other resources available to create these as well https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key

### **DEBUG**
If you are running the app in production, this value MUST be set to `True`. Only set to `False` if you are in a development environement. https://docs.djangoproject.com/en/4.1/ref/settings/#debug

### **RUNNING_IN_DOCKER**
Set this to `True` if you are running this in a Docker Container (you would/should be if running in production), `False` if not. You will typically only run the app outside of Docker when in a development environment. Even so, you should do your best to always launch the app in Docker, as there can be key differences in how Models serialize to SQLite VS MySQL.

### **DOMAIN_NAME**
Set this to the public domain that you will be connecting to the server with in production. This is the domain that NGINX is listening for requests on. This is only relevant when running in production/Docker, and is overriden when in a development environment.

### **ADMIN_BRAND_NAME**
The brand name used in admin interfaces. This will not be displayed on the typical user front end.

### **LANGUAGE_CODE**
A code representing the language used by Django. This is set to `en-us` by default, but can be changed. https://docs.djangoproject.com/en/4.1/ref/settings/#language-code

### **TIME_ZONE**
The time zone used by Django. This is set to `America/New_York` by default, but can be changed. https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-TIME_ZONE

# *Database*

### **USE_SQLITE**
Setting this to `True` will use a SQLite driver instead of a MYSQL driver. This should be set to `False`, and you should use MYSQL unless you have a specific reason.

### **MYSQL_PASSWORD**
The password that will be used by raptorWeb to connect to the MYSQL server. This is not the root password. **STORE IT IN A PASSWORD MANAGER!**

### **MYSQL_ROOT_PASSWORD**
The root password to the MYSQL database. This password is only used for debug purposes, if you must enter the MYSQL shell. **STORE IT IN A PASSWORD MANAGER!**

# *Users / Auth*

### **DISCORD_OAUTH_APP_ID**
The app ID of the Discord Application you will be using to process OAuth login requests.

### **DISCORD_OAUTH_APP_SECRET**
The app secret of the Discord Application you will be using to process OAuth login requests

### **DEFAULT_SUPERUSER_USERNAME**
The username for the superuser that will be created on first start, when there are no users created yet. Change the password for this user right away, it will be set to "admin" by default.

### **DEFAULT_SUPERUSER_EMAIL**
The email for the superuser that will be created on first start, when there are no users created yet. Change the password for this user right away, it will be set to "admin" by default.

# *Discord Bot*

### **DISCORD_BOT_TOKEN**
The Bot Token for the Discord Application Bot you will use for the Discord Bot

### **DISCORD_BOT_DESCRIPTION**
A description for the Discord Bot, used when creating the Bot

# *Email*

### **USE_CONSOLE_EMAIL**
If this is set to False, then emails sent by the application will *actually* be sent using the SMPT mail driver. While True, emails will be "sent" to the console as messages. Do NOT set this to False until you have configured the below settings and are ready to send emails.

### **ERROR_LOG_EMAIL**
An additional email you want error reports sent to, alongside the default superuser email. This cannot be the same as EMAIL_HOST_USER.

### **EMAIL_HOST**
The domain name/IP address for the SMTP server you wish to use. For example, gmail's SMTP domain is `smtp.gmail.com`. If you are using self-hosted email, you will place your connection address here.

### **EMAIL_PORT**
The port used for connecting to the SMTP server. This is typically `587`, but it may be different.

### **EMAIL_HOST_USER**
The User/email address you will be using to send email. This should be an email address.

### **EMAIL_HOST_PASSWORD**
The password for the supplied `EMAIL_HOST_USER`