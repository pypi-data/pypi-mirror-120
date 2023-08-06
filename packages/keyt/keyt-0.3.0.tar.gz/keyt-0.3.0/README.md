# keyt

[![keyt-pypi](https://img.shields.io/pypi/v/keyt.svg)](https://pypi.python.org/pypi/keyt)

## Install

```shell
pip install keyt
```

## Usage

```txt
usage: keyt [domain] [username] [master_password] [options]

keyt stateless password manager and generator.

positional arguments:
  domain                Domain name/IP/service.
  username              Username/Email/ID.
  master_password       Master password used during the password generation.

optional arguments:
  -h, --help            show this help message and exit
  --version
  -c COUNTER, --counter COUNTER
                        An integer that can be incremented to change our the
                        password. default=0.
  -f FORMAT, --format FORMAT
                        Password format can be: 'max', 'high', 'mid', 'pin' or
                        'pin6'. default=max.
  -o, --output          Output the password, by default the password is copied
                        to the clipboard.
  -t [TIMER], --timer [TIMER]
                        Time before flushing the clipboard. default=20s, use 0
                        or nothing to disable the timer.
```

## Examples

```shell
$ keyt
domain: example.com
username: admin
master password:
Password copied to the clipboard for 20s.

$ keyt example.com admin admin
Password copied to the clipboard for 20s.

$ keyt example.com admin admin -o
Fg0XjW@a=vWi@3qGBjo|Vlic7Wo9`zVKp!{Vl_Bp

$ keyt example.com admin admin -o -f mid
5w8Hv23ZUvJCRt2t

$ keyt example.com admin admin -o -f pin
3070
```

## License

keyt is licensed under MIT.
