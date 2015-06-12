class GroupType(object):
    def __init__(self, g_type, value, addon_value):
        self.g_type = g_type
        self.value = value
        self.addon_value = addon_value

        self.data = self.get_data()

    def get_data(self):
        if self.g_type == "singles":
            # 3
            return [self.value]
        if self.g_type == "twices":
            # 3
            return [self.value] * 2
        if self.g_type == "fours":
            # 3
            return [self.value] * 4
        if self.g_type == "triples":
            # 3 | [4, 2]
            return [self.value] * 3 + \
                self.addon_value[0] * self.addon_value[1]
        if self.g_type = "jokers":
            #
            return [53, 54]
        if self.g_type == "shunzi_s":
            # [3, 4, 5, 6, 7]
            return self.value
        if self.g_type == "shunzi_ss":
            # [3, 4, 5, 6, 7]
            return self.value * 2
        if self.g_type == "shunzi_sss":
            # [3, 4] | [[5, 6], 2]
            return self.value * 3 + \
                self.addon_value[0] * self.addon_value[1]

