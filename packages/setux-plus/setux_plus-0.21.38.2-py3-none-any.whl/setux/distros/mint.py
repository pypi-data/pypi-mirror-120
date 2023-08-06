from setux.distros.debian import Debian_10


class Mint_20(Debian_10):

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        if did=='LinuxMint':
            did='Mint'
        ver = infos['DISTRIB_RELEASE']
        return f'{did}_{ver}'
