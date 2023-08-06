from setux.distros.debian import Debian_10


class Sparky_6(Debian_10):

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        ver = infos['DISTRIB_RELEASE']
        return f'{did}_{ver}'
