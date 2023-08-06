# meris-checker

meris-checker is a command which helps you determine whether or not your IP addresses are listed in the Qrator Labs database of meris botnet IPs.

## Installation

Use the package manager [poetry](https://python-poetry.org/docs/) to install meris-checker.

```bash
poetry install meris-checker
```

## Usage

There are two ways to use this script. The first is to create a file named `ips.txt`:

```bash
$ echo 127.0.0.1 >> ips.txt
$ echo 127.0.0.0/29 >> ips.txt
$ poetry run meris-checker
IP 127.0.0.1 is safe, whew!
IP 127.0.0.0 is safe, whew!
IP 127.0.0.1 is safe, whew!
IP 127.0.0.2 is safe, whew!
IP 127.0.0.3 is safe, whew!
IP 127.0.0.4 is safe, whew!
IP 127.0.0.5 is safe, whew!
IP 127.0.0.6 is safe, whew!
IP 127.0.0.7 is safe, whew!
```

The second is to specify the IPs one-at-a-time on the command line:

```bash
$ poetry run meris-checker 127.0.0.1 127.0.0.0/30
IP 127.0.0.1 is safe, whew!
IP 127.0.0.0 is safe, whew!
IP 127.0.0.1 is safe, whew!
IP 127.0.0.2 is safe, whew!
IP 127.0.0.3 is safe, whew!
```

This should work with any valid IPv4/IPv6 address or subnet. However, please be aware that it hits the Qrator API for each address in the subnet individually, so you should probably limit your lookups to narrow ranges that you actually own.

The script is rate-limited to 1 IP query per second, so a /24 will take ~6 minutes to run.

## Contributing

Patches are welcome. Please email don@bloono.com

## License

[MIT](https://choosealicense.com/licenses/mit/)
