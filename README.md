# bearychat_irc
a robot bridge between bearychat and irc

## Dependences
```shell
sudo pip3 install -r requirements.txt
```

## Usage
#### 1. cp the template
```shell
cd etc
cp config.ini_example config.ini
cp bearychat.ini_example bearychat.ini
cd .. && ln -sf etc/config.ini config.ini
```

#### 2. fill config files
- config.ini file
```ini
#
# ...
autojoins = deepin  # change this channel to what you want to listen
# ...
#
```

- bearychat.ini file

```ini
# 
# ...

# you may need to add a incoming robot inner your bearychat team
# and copy the hook address to the follow
grouphook = https://hook.bearychat.com/=bwxxx/incoming/xxxxxxxxxxxx

# bc channel id, irc msg will be forwarded to this channel
channel_id = =bwxxx

# any words said by the filter ids won't be forwarded to irc
# attention!! the incoming robot id must be written here
id_filter = 
    =bwxxA
    =bwxxB

# this robot work is to recv the bearychat channel msg
# and send to irc
# this robot need
[robot]
username = name@domain.com
password = passwd


```


### 3. run with irc3
```shell
irc3 config.ini
```

## License
This project is licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt).
