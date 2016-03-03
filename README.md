# bearychat_irc
a robot bridge between bearychat and irc

## Dependences
```shell
sudo pip3 install -r reqirements.txt
```

## Usage
#### 1. cp the template
```shell
cd etc
cp config.ini_example config.ini
cp bearychat.ini_example bearychat.ini
cd .. && ln -sf etc/config.ini config.ini
```

#### 2. just fill the template as the guid inside

### 3. run with irc3
```shell
irc3 config.ini
```

## License
This project is licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt).
