# Speed test.

Simple application for monitoring internet speed connection at home continuously.

## Getting started.

### 1. Create a MySQL database to store tests data.

Create a new MySQL instance in order to save the speed test generated data. [Here](database/database.sql) is the database structure used by this application.

### 2. Setting up the application at your home device.

1. Install speed test cli in your device. Next instructions are for an old Raspberry Pi B+ but for other devices follow the instructions at [this link](https://www.speedtest.net/es/apps/cli).

  ```bash
  # Install dependencies.
  sudo apt-get install gnupg1 apt-transport-https dirmngr

  # Add the Speed test cli source repository.
  $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61
  $ sudo add-apt-repository \
      "deb https://ookla.bintray.com/debian \
      $(lsb_release -sc) \
      main"

  # Update source repositories.
  $ sudo apt-get update

  # Install speedtest-cli.
  sudo apt-get install speedtest
  ```

2. Copy [this python script](python/speed_test.py) to your device. Do not forget to change your access data before sending it to your device.

  ```python
  # Database hostname.
  DB_HOSTNAME = "my-own-domain.com";

  # Database's name.
  DB_NAME = "my-database-name";

  # Database user.
  DB_USERNAME = "my-database-user";

  # Database user's pass.
  DB_USER_PASSWORD = "my-user's-password";
  ```

3. Insert a new record to crontab to auto-run your script every time you want.

  ```bash
  # Editing crontab
  $ crontab -e

  # Add a scheduled task (this one runs every 15 minutes).
  */15 * * * * python /home/pi/Workspaces/github/speed_test/python/speed_test.py
  ```

### 3. Monitor the results using a web page.

 Open [this web page](web_page/index.html) in your browser to watch the results.
