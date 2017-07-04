try:
    import pyzmail
except ImportError:
    import pip
    def install(pkg):
        pip.main(['install', pkg])
    install(pyzmail)
finally:
    import pyzmail


