from setux.core.mapping import Packages


class Fedora(Packages):
    mapping = dict(
        netcat = 'nmap-ncat',
    )


class Arch(Packages):
    mapping = dict(
        netcat = 'openbsd-netcat',
        sqlite = 'sqlite3',
    )


class Fedora(Packages):
    mapping = dict(
        netcat = 'nmap-ncat',
    )


class Artix(Packages):
    mapping = dict(
        netcat = 'openbsd-netcat',
        sqlite = 'sqlite3',
        cron   = 'cronie',
    )
