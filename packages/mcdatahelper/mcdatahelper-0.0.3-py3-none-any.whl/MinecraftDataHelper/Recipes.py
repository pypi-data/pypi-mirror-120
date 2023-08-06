import os
import json

from MinecraftDataHelper.Items import Items
from MinecraftDataHelper.tags import Tags


class StoneCutting:
    js = {
        "type": "stonecutting",
        "ingredient": [],
        "count": 1,
        "result": ''
    }

    def ingredient(self, s):
        if len(self.js["ingredient"]) == 1:
            raise Exception('ingredients最多 1 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredient"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredient"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def count(self, count):
        if count <= 0 or count > 64:
            raise Exception(f'物品数量必须为 1-64 的整数, 你的值 {count}')
        else:
            self.js["count"] = count
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class Smoking:
    js = {
        "type": "smoking",
        "ingredient": [],
        "cookingtime": 100,
        "experience": 0,
        "result": ''
    }

    def ingredient(self, s):
        if len(self.js["ingredient"]) == 1:
            raise Exception('ingredients最多 1 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredient"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredient"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def cookingtime(self, time):
        if isinstance(time, int) and time > 0:
            self.js["cookingtime"] = time
        else:
            raise Exception(f'cookingtime 必须为大于 0 的整数，得到了 {time}')
        return self

    def experience(self, exp):
        if isinstance(exp, int) and exp >= 0:
            self.js["experience"] = exp
        else:
            raise Exception(f'experience 必须为大于等于 0 的整数，得到了 {exp}')
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class Smithing:
    js = {
        "type": "smithing",
        "base": {},
        "addition": {},
        "result": {}
    }

    def base(self, s):
        if hasattr(Tags, s.upper()):
            self.js["base"] = {}
            self.js["base"]["tag"] = s
        elif hasattr(Items, s.upper()):
            self.js["base"] = {}
            self.js["base"]["item"] = s
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def addition(self, s):
        if hasattr(Tags, s.upper()):
            self.js["addition"] = {}
            self.js["addition"]["tag"] = s
        elif hasattr(Items, s.upper()):
            self.js["addition"] = {}
            self.js["addition"]["item"] = s
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class Smelting:
    js = {
        "type": "smelting",
        "ingredient": [],
        "cookingtime": 100,
        "experience": 0,
        "result": ''
    }

    def ingredient(self, s):
        if len(self.js["ingredient"]) == 1:
            raise Exception('ingredients最多 1 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredient"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredient"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def cookingtime(self, time):
        if isinstance(time, int) and time > 0:
            self.js["cookingtime"] = time
        else:
            raise Exception(f'cookingtime 必须为大于 0 的整数，得到了 {time}')
        return self

    def experience(self, exp):
        if isinstance(exp, int) and exp >= 0:
            self.js["experience"] = exp
        else:
            raise Exception(f'experience 必须为大于等于 0 的整数，得到了 {exp}')
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class Campfire:
    js = {
        "type": "campfire_cooking",
        "ingredient": [],
        "cookingtime": 100,
        "experience": 0,
        "result": ''
    }

    def ingredient(self, s):
        if len(self.js["ingredient"]) == 1:
            raise Exception('ingredients最多 1 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredient"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredient"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def cookingtime(self, time):
        if isinstance(time, int) and time > 0:
            self.js["cookingtime"] = time
        else:
            raise Exception(f'cookingtime 必须为大于 0 的整数，得到了 {time}')
        return self

    def experience(self, exp):
        if isinstance(exp, int) and exp >= 0:
            self.js["experience"] = exp
        else:
            raise Exception(f'experience 必须为大于等于 0 的整数，得到了 {exp}')
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class Blasting:
    js = {
        "type": "blasting",
        "ingredient": [],
        "cookingtime": 100,
        "experience": 0,
        "result": ''
    }

    def ingredient(self, s):
        if len(self.js["ingredient"]) == 1:
            raise Exception('ingredients最多 1 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredient"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredient"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def cookingtime(self, time):
        if isinstance(time, int) and time > 0:
            self.js["cookingtime"] = time
        else:
            raise Exception(f'cookingtime 必须为大于 0 的整数，得到了 {time}')
        return self

    def experience(self, exp):
        if isinstance(exp, int) and exp >= 0:
            self.js["experience"] = exp
        else:
            raise Exception(f'experience 必须为大于等于 0 的整数，得到了 {exp}')
        return self

    def result(self, x):
        if hasattr(Items, x.upper()):
            self.js["result"] = x
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class CraftingShapeless:
    js = {
        "type": "crafting_shapeless",
        "ingredients": [],
        "result": {}
    }

    def ingredients(self, s):
        if len(self.js["ingredients"]) >= 9:
            raise Exception('ingredients最多 9 个物品')
        if hasattr(Tags, s.upper()):
            self.js["ingredients"].append({"tag": s})
        elif hasattr(Items, s.upper()):
            self.js["ingredients"].append({"item": s})
        else:
            raise Exception('不能使用非Tag/Item对象')
        return self

    def result(self, x, count=1):
        if hasattr(Items, x.upper()):
            self.js["result"]["item"] = x
            self.js["result"]["count"] = count
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return


class CraftingShaped:
    js = {
        "type": "crafting_shaped",
        "pattern": [],
        "key": {},
        "result": {}
    }

    def pattern(self, s):
        self.js["pattern"].append(s)
        return self

    def key(self, k, x):
        self.js["key"][k] = {}
        if hasattr(Tags, x.upper()):
            self.js["key"][k]["tag"] = x
        elif hasattr(Items, x.upper()):
            self.js["key"][k]["item"] = x
        return self

    def result(self, x, count=1):
        if count <= 0 or count > 64:
            raise Exception(f'物品数量必须为 1-64 的整数, 你的值 {count}')
        if hasattr(Items, x.upper()):
            self.js["result"]["item"] = x
            self.js["result"]["count"] = count
        return self

    def build(self, path):
        if not os.path.exists('data/gen/recipes/'):
            os.makedirs('data/gen/recipes/')
        with open(f'data/gen/recipes/{path}.json', 'w')as f:
            json.dump(self.js, f, indent=4)
        return
