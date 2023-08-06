# ddns

ddns for dynu.com. 

## install

```sh
sudo python3 -m pip install ddns-dynu --upgrade
```

> NOTE: `sudo` guarantees package installed into `/usr/local/lib`, and `ddns-dynu` in `/usr/local/bin`, which is necessary when you want to run it as service.


## usage

1. update ipv4 record

```sh
ddns-dynu t $token $hostname 4
```
`$token` is dynu api-key, checking here https://www.dynu.com/en-US/ControlPanel/APICredentials. 

`$hostname` is dns hostname you want to update.

> NOTE: Please confirm that you **have $hostname record in dynu**, or program can never work properly. 

2. update ipv6 record

```sh
ddns-dynu t $token $hostname 6 $interface
```

`$interface` is the name of network card, which provides ipv6.

3. run as daemon

```sh
ddns-dynu d $token_file ...

# #eg:
# $ ddns-dynu d /etc/ddns-dynu-api-key ipv6.test.com 6 wlp2s0
# $ cat /etc/ddns-dynu-api-key
# AakjozEaxdfWaadEQTjjuvkakqhioqQa
```

`$token_file` is where your api-key stored.

`t` means test mode, and `d` means daemon mode. 

If you want to install it as a systemd service, there is one sample `ddns.service` file.

```
[Unit]
Description=ddns for dynu update
After=network.target nss-lookup.target

[Service]
ExecStart=/usr/local/bin/ddns-dynu d /etc/ddns-dynu-token ipv6.agfn.tk 6 enp3s0
ExecStop=kill $MAINPID

[Install]
WantedBy=multi-user.target
```

Copy this file into `/etc/system/systemd/ddns.service`.

Then

```sh
sudo systemctl daemon-reload
sudo systemctl enable ddns.service
sudo systemctl start ddns.service
```

Log file is at `/var/log/ddns.log`
