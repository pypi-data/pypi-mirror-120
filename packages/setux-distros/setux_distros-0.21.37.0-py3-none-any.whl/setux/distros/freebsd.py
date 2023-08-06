from setux.core.distro import Distro


class FreeBSD(Distro):
    Package = 'pkg'
    Service = 'Service'
    pkgmap = dict(
    )
    svcmap = dict(
        ssh = 'sshd',
    )

    @classmethod
    def release_infos(cls, target):
        ret, out, err = target.run('uname -s', report='quiet')
        distro = out[0]
        if distro=='FreeBSD':
            ret, out, err = target.run('uname -r', report='quiet')
            ver = out[0].split('.')[0]
            return dict(
                ID         = distro,
                VERSION_ID = ver,
            )


class FreeBSD_12(FreeBSD):
    pkgmap = dict(
        pip        = 'py37-pip',
        setuptools = 'py37-setuptools',
    )


class FreeBSD_13(FreeBSD):
    pkgmap = dict(
        pip        = 'py38-pip',
        setuptools = 'py38-setuptools',
    )

