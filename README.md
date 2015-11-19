# bearychat_irc
a robot bridge between bearychat and irc

## Dependences
```shell
sudo pip3 install -r reqirements.txt
```

## Usage
#### 1. cp the template
```shell
cp config.ini_example config.ini
cp bearychat.ini_example bearychat.ini
```

#### 2. just fill the template as the guid inside


## Known issues
The websocket connection of bearychat will be closed by some unkonw problem after connect long time (maybe 2 or 3 days), I have no idea how to fix this bug now :( , I just handle with restarting the service every morning with automated tool.

## License
This project is licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt).
