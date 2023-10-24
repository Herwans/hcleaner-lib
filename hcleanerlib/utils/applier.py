import os
import re

from hcleanerlib.utils.config import Configuration


class Applier:
    def __init__(self, config_type):
        self.__config = Configuration(config_type)

    def apply_folder_rules(self, element):
        altered_element = element
        for rule in self.__config.get_folder_rules():
            # 0 = Pattern
            # 2 = Replacement
            altered_element = re.sub(rule[0], rule[1], altered_element)
        altered_element = altered_element.strip()
        return altered_element

    def apply_file_rules(self, element):
        sets = self.__config.get_extension_sets()
        file_name, file_extension = os.path.splitext(element)
        altered_element = file_name
        for rule in self.__config.get_file_rules():
            if len(rule) == 4:
                exclusion = rule[3].split(',')
            else:
                exclusion = []
            if (rule[2] == '*' or file_extension.lstrip(".") in sets[rule[2]]) \
                    and file_extension.lstrip(".") not in exclusion:
                altered_element = altered_element.strip()
                altered_element = re.sub(rule[0], rule[1], altered_element)
        altered_element = altered_element.strip()

        if altered_element == "":
            return element
        return altered_element + file_extension
