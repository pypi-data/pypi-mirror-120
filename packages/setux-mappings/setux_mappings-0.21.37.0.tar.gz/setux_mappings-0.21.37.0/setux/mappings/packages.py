from setux.core.mapping import Packages


class Debian(Packages):
    mapping = dict(
        sqlite = 'sqlite3',
    )


class FreeBSD(Packages):
    mapping = dict(
        sqlite = 'sqlite3',
    )
