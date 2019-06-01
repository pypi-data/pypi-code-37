from Homevee.Item import Item


class SystemInfoItem(Item):
    def __init__(self, name, icon, value):
        super(SystemInfoItem, self).__init__()
        self.name: str = name
        self.icon: str = icon
        self.value: str = value