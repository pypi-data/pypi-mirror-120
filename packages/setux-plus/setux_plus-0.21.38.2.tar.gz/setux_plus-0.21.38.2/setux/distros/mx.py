from setux.distros.debian import Debian_10


class MX_19(Debian_10):
    Service = 'SystemV'

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        ver = infos['DISTRIB_RELEASE'].split('.')[0]
        return f'{did}_{ver}'
