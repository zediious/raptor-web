# Configuring raptorWeb

## Before you can start the application successfully, you need to create a file with the filename `.env` in the same location of this `README.md` file. Into the `.env` file, you need to copy the text within the code block below. After doing so, you will need to put information into each element that does not have a value. If a key has a value, except `''`, **it MUST stay as it is**. If an element has a pair of quotes `''`, **you must enter your value inside of those quotes**.

## The exception to this is `LANGUAGE_CODE` and `TIME_ZONE`. Preferred defaults are set, but you may change them.

## Below the code block you will find an explanation for each field, and what you should put in them.

```
DJANGO_SECRET_KEY=''
DEBUG=
RUNNING_IN_DOCKER=
DOMAIN_NAME=''
LANGUAGE_CODE='en-us'
TIME_ZONE='America/New_York'

USE_SQLITE=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=raptormc
MYSQL_USER=raptor
BASE_PATH=/tmp

ENABLE_SERVER_QUERY=
IMPORT_SERVERS=
DELETE_EXISTING=

DISCORD_OAUTH_APP_ID=
DISCORD_OAUTH_APP_SECRET=

DISCORD_BOT_TOKEN=''
DISCORD_BOT_DESCRIPTION=''
DISCORD_GUILD=
GLOBAL_ANNOUNCEMENT_CHANNEL_ID=
STAFF_ROLE_ID=

USE_GLOBAL_ANNOUNCEMENT=
SCRAPE_SERVER_ANNOUNCEMENT=
```
## *General*

### **DJANGO_SECRET_KEY**
This value must be a long and random set of numbers, letters, and special characters. I recommend using a Password Generator from something like BitWarden to generate these values. There are other resources available to create these as well https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key

### **DEBUG**
If you are running the app in production, this value MUST be set to `True`. Only set to `False` if you are in a development environement. https://docs.djangoproject.com/en/4.1/ref/settings/#debug

### **RUNNING_IN_DOCKER**
Set this to `True` if you are running this in a Docker Container (you would/should be if running in production), `False` if not. You will typically only run the app outside of Docker when in a development environment. Even so, you should do your best to always launch the app in Docker, as there can be key differences in how Models serialize to SQLite VS MySQL.

### **DOMAIN_NAME**
Set this to the public domain that you will be connecting to the server with in production. This is the domain that NGINX is listening for requests on. This is only relevant when running in production/Docker, and is overriden when in a development environment.

### **LANGUAGE_CODE**
A code representing the language used by Django. This is set to `en-us` by default, but can be changed. https://docs.djangoproject.com/en/4.1/ref/settings/#language-code

### **TIME_ZONE**
The time zone used by Django. This is set to `America/New_York` by default, but can be changed. https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-TIME_ZONE

## *Database*

### **USE_SQLITE**
Setting this to `True` will use a SQLite driver instead of a MYSQL driver. This should be set to `False`, and you should use MYSQL unless you have a specific reason.

### **MYSQL_PASSWORD**
The password that will be used by raptorWeb to connect to the MYSQL server. This is not the root password. **STORE IT IN A PASSWORD MANAGER!**

### **MYSQL_ROOT_PASSWORD**
The root password to the MYSQL database. This password is only used for debug purposes, if you must enter the MYSQL shell. **STORE IT IN A PASSWORD MANAGER!**

## *Game Servers*

### **ENABLE_SERVER_QUERY**
If this is set to `False`, the entire gameservers logic will be disabled.

### **IMPORT_SERVERS**
If this is set to `True`, then Servers will be imported from a `server_data_full.json` located at the top level directory of the app, alongside `manage.py`. After this process has completed, you MUST stop the server and restart it with this setting back to `False`.

### **DELETE_EXISTING**
If this set to `True`, then when `IMPORT_SERVERS` is set to `True`, all existing serves will be deleted before importing. This setting has no effect when `IMPORT_SERVERS` is set to `False`

## *Discord OAuth*

### **DISCORD_OAUTH_APP_ID**
The app ID of the Discord Application you will be using to process OAuth login requests.

### **DISCORD_OAUTH_APP_SECRET**
The app secret of the Discord Application you will be using to process OAuth login requests

## *Discord Bot*

### **DISCORD_BOT_TOKEN**
The Bot Token for the Discord Application Bot you will use for the Discord Bot

### **DISCORD_BOT_DESCRIPTION**
A description for the Discord Bot, used when creating the Bot

### **DISCORD_GUILD**
The Guild ID of the Discord Guild that you wish to have linked to the web application

### **GLOBAL_ANNOUNCEMENT_CHANNEL_ID**
The Channel ID of the Discord Channel you designate as the Global Announcement Channel.

### **STAFF_ROLE_ID**
The Role ID of the Discord Role you designate as a Staff Member.