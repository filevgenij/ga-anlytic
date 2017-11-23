from cleo import Command


class BaseCommand(Command):
    container = None

    def get_container(self):
        return self.container
