from cleo import Application
from .cli.about import AboutCommand


application = Application()
application.add(AboutCommand())


def main():
    application.run()


if __name__ == '__main__':
    main()
