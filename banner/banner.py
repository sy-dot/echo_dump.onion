class Banner(object):
    def LoadECHODUMPBanner(self):
        try:
            from termcolor import cprint, colored
            banner = '''
            
        █▀▀ █▀▀ █░█ █▀█ █▀▄ █░█ █▀▄▀█ █▀█
        ██▄ █▄▄ █▀█ █▄█ █▄▀ █▄█ █░▀░█ █▀▀
                                    v.1.0
        Fork By: 87SQUAD
        t.me/w87squad  
            '''
            cprint(banner, 'magenta', attrs=['bold'])

        except ImportError as ie:
            print(banner)
