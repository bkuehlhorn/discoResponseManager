"""
Dict with access to nexted dict and list thru a single flat key
-----------------------------------------------------------------

Support to access values with one complex key
"""
import collections

class FlatDict(dict):
    """

    """
    def getValue(self, key):
        """
        Key contains individual dict and list keys separated by ":"
        Returns final value from complex key. None is returned when partial key is not found

        :param key: string of keys with ":" delimiter
        :return: value of final key
        """
        if isinstance(key, int):
            keys = [key]
        else:
            keys = key.split(':')
        my_dict = self
        for part_key in keys:
            if isinstance(part_key, int):
                pass
            elif part_key.isnumeric():
                part_key = int(part_key)
            elif part_key == '':
                return ''
            my_dict = my_dict[part_key]
        return my_dict

    def addValue(self, key, value):
        """
        Find last key in self from key string
        Add [] for missing keys when next is int
        add MyDict() for missing keys when next is not int

        :param key: string of keys with ":" delimiter
        :param value: value for last key
        :return: None
        """
        keys = key.split(':')
        prior_part_key = keys.pop(0)
        my_dict = self
        for part_key in keys:
            if prior_part_key not in my_dict or my_dict[prior_part_key] is None:
            #     add [] or {} based on part_key isnumeric or letters
                if part_key.isnumeric():
                    part_key = int(part_key)
                    my_dict[prior_part_key] = [None] * (part_key + 1)
                else:
                    my_dict[prior_part_key] = MyDict()
            my_dict = my_dict[prior_part_key]
            prior_part_key = part_key
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
        while(notDone):
            if isinstance(response, dict):
                key = next(keys, None)
            elif isinstance(response, list):
                if key is not None:
                    if len(response) == 0:
                        response = [0]
                    key = 0
            else:
                key = None
            if key is None:
                if len(jsonStack) > 0:
                    (response, fullKey, keys) = jsonStack.pop()
                else:
                    notDone = False
            else:
                if isinstance(response[key], (list, dict)):
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
                    if len(response) > 0 and isinstance(response[key], (dict, list)):
                        key = response[key]
                    else:
                        key = key if isinstance(key, str) else str(key)
                        fullKeys.append(':'.join(fullKey + [key]))
                        key = None
        return fullKeys

