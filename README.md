# Avahi Aliases (CNAME)

Add `CNAME` aliases to current Avahi host.

Dependencies:
 * Python 2.7
 * python-avahi, python-pip

## Installation

```bash
# apt-get install -y python-avahi python-pip
# pip install --upgrade git+https://github.com/Dalee/avahi-cname-aliases.git
```

## Systemd configuration
```
[Unit]
Description=Avahi Aliases stack
Requires=avahi-daemon.service
After=avahi-daemon.service

[Service]
ExecStart=/usr/local/bin/avahi-cname-aliases

[Install]
WantedBy=multi-user.target
```

```bash
# systemctl daemon-reload
# systemctl enable avahi-aliases
# systemctl start avahi-aliases
```

## Set aliases

```bash
# mkdir /etc/avahi/aliases.d
# echo "hello.local" > /etc/avahi/aliases.d/hello.txt
# systemctl restart avahi-aliases
```

## Common pitfalls

Avahi allows 32 CNAME aliases per group.

In order to increase this value just tune `entries-per-entry-group-max` 
value of `/etc/avahi/avahi-daemon.conf`.


## License

Code is unlicensed. Do whatever you want with it. [Set Your Code Free](http://unlicense.org/).
