"""
Dict with access to nested dict and list thru a single flat key
-----------------------------------------------------------------

Support to access values with one complex key
"""
import collections
from discoResponseManager import logger

class FlatDict(dict):
    """
    Sub-class of `dict` to support nested `dict` and `list`.
    Complex key is keys for nested `dict` and `list` separated by ":".
    Any value can be returned by complex key.
    Values can be added for complex key.
    If key does not exist for a nested `dict` or `list`, entry is created.

    """
    DELIMITER = ':'
    def getValue(self, key):
        """
        Key contains individual dict and list keys separated by ":"
        Returns final value from complex key. None is returned when partial key is not found

        :param key: string of keys with ":" DELIMITER
        :return: value of final key
        """
        if isinstance(key, int):
            keys = [key]
        else:
            keys = key.split(self.DELIMITER)
        my_dict = self
        logger.debug(f'keys: {list(keys)}')
        for part_key in keys:
            logger.debug(f'\tpart_key: {part_key}')
            if part_key.isnumeric():
                part_key = int(part_key)
            elif part_key == '':
                return ''
            my_dict = my_dict[part_key]
        logger.debug(f'my_dict: {my_dict}')
        return my_dict

    def addValue(self, key, value):
        """
        Find last key in self from key string
        Add [] for missing keys when next is int
        add MyDict() for missing keys when next is not int

        :param key: string of keys with ":" DELIMITER
        :param value: value for last key
        :return: None
        """
        # todo: fix bug with list index
        # todo: support adding dict/list - ensure it works
        if isinstance(key, int):
            keys = [key]
        else:
            keys = key.split(self.DELIMITER)
        prior_part_key = keys.pop(0)
        my_dict = self
        logger.debug(f'keys: {list(keys)}, value: {value}')
        for part_key in keys:
            logger.debug(f'\tpart_key: {part_key}')
            if prior_part_key not in my_dict or my_dict[prior_part_key] is None:
            #     add [] or {} based on part_key isnumeric or letters
                if part_key.isnumeric():
                    part_key = not(part_key)
                    my_dict[prior_part_key] = [None] * (part_key + 1)
                    logger.debug(f'\t{tabs}\t\tpart_key: {part_key}, numeric')
                else:
                    my_dict[prior_part_key] = FlatDict()
                    logger.debug(f'\t{tabs}\t\tpart_key: {part_key}, my_dict[prior_part_key]')
            my_dict = my_dict[prior_part_key]
            prior_part_key = part_key
        logger.debug(f'prior_part_key: {prior_part_key}, value: {value}')
        if prior_part_key.isnumeric():
            prior_part_key = int(prior_part_key)
        my_dict[prior_part_key] = value
        return

    def getKeys(self):
        """
        get unique string of keys to values in response dict
        list use 0 for entry

        :return: set of unique keys to values
        """
        response = self
        notDone = True
        keys = iter(response.keys())
        key = None
        jsonStack = collections.deque()
        fullKeys = []
        fullKey = []
        logger.debug(f'keys: {response.keys()}')
        while notDone:
            tabs = '\t' * len(jsonStack)
            if isinstance(response, dict):
                key = next(keys, None)
            elif isinstance(response, list):
                if key is not None:
                    if len(response) == 0:
                        response = [0]
                    key = 0
            else:
                key = None
            logger.debug(f'\t{tabs}key: {key}')
            if key is None:
                if len(jsonStack) > 0:
                    (response, fullKey, keys) = jsonStack.pop()
                else:
                    notDone = False
            else:
                logger.debug(f'\t{tabs}\tresponse[key]: {response[key]}')
                if isinstance(response[key], (list, dict)):
                    logger.debug(f'\t\t\t{tabs}list/dict')
                    jsonStack.append((response, fullKey, keys))
                    fullKey = fullKey.copy()
                    response = response[key]
                    key = key if isinstance(key, str) else str(key)
                    fullKey.append(key)
                    if isinstance(response, dict):
                        # need another append, response and fullKey
                        sortedKeys = sorted(response.keys())
                        keys = iter(sortedKeys)
                    else:
                        response = [0] if len(response) == 0 else response
                        keys = iter(response)
                        pass
                else:
                    logger.debug(f'\t\t\t{tabs}value')
                    if len(response) > 0 and isinstance(response[key], (dict, list)):
                        key = response[key]
                    else:
                        key = key if isinstance(key, str) else str(key)
                        fullKeys.append(self.DELIMITER.join(fullKey + [key]))
                        key = None
            logger.debug(f'{tabs}*** last fullKey: {fullKeys[-1]}')
        return fullKeys
