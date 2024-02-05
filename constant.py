#定数を置いておっくためのモジュール
#参考元 https://qiita.com/nadu_festival/items/c507542c11fc0ff32529
#参考というかまんまであるが...

class ConstantError(Exception):
    """Constantクラスの例外"""
    pass

class ConstantMeta(type):
    """Constantクラスのメタクラス"""

    def __new__(mcls, classname, bases, dict):
        # 異なるConstantMetaを継承していないか検証する
        sub_clses = [cls for cls in bases if isinstance(cls, ConstantMeta)]
        for sub_cls in sub_clses[1:]:
            if sub_clses[0] != sub_cls:
                raise ConstantError(f"Can't inhelitance of [{sub_clses[0].__name__}] and [{sub_cls.__name__}] together")

        # 親クラス同士で定数の衝突が起こっていないか確認
        super_consts = set()
        for base in bases:
            base_consts = ConstantMeta.__get_constant_attr(mcls, base.__dict__)
            collisions = (super_consts & base_consts)
            if collisions:
                collis_str = ", ".join(collisions)
                raise ConstantError(f"Collision the constant [{collis_str}]")
            super_consts |= base_consts

        # 定義するクラスで定数の再定義をしていないか確認
        new_consts = ConstantMeta.__get_constant_attr(mcls, dict)
        rebinds = (super_consts & new_consts)
        if rebinds:
            rebinds_str = ", ".join(rebinds)
            raise ConstantError(f"Can't rebind constant [{rebinds_str}]")

        # __init__関数置き換えてインスタンス生成を禁止する
        def _meta__init__(self, *args, **kwargs):
            # インスタンスの生成をしようとした際、ConstantErrorを送出する。
            raise ConstantError("Can't make instance of Constant class")
        # __init__関数を置き換えてインスタンス生成を禁止する。
        dict["__init__"] = _meta__init__

        return type.__new__(mcls, classname, bases, dict)

    @staticmethod
    def __get_constant_attr(mcls, dict):
        """定数として扱うアトリビュートの集合を取得する"""
        # 特殊なアトリビュートを除くアトリビュートを取得する
        attrs = set(
            atr for atr in dict if not ConstantMeta.__is_special_func(atr)
        )
        # アトリビュートがすべて定数または例外的にクラス変数に格納可能な
        # 変数であることを確認する
        cnst_atr = set(atr for atr in attrs if mcls.is_constant_attr(atr))
        var_atr = set(atr for atr in attrs if mcls.is_settable_attr(atr))
        wrong_atr = attrs - (cnst_atr | var_atr)
        if wrong_atr:
            wrong_atr_str = ", ".join(wrong_atr)
            raise ConstantError(f"Attribute [{wrong_atr_str}] were not constant or not settable.")
        return cnst_atr

    @staticmethod
    def __is_special_func(name):
        """特殊アトリビュートかどうかを判定する"""
        return name.startswith("__") and name.endswith("__")

    @classmethod
    def is_constant_attr(mcls, name):
        """定数として扱うアトリビュートか判定する"""
        return (not name.startswith("__"))

    @classmethod
    def is_settable_attr(mcls, name):
        """例外的にクラス変数に格納することを許可するアトリビュートか判定する"""
        return (not mcls.is_constant_attr(name))

    def __setattr__(cls, name, value):
        mcls = type(cls)
        if mcls.is_constant_attr(name) or (not mcls.is_settable_attr(name)):
            raise ConstantError(f"Can't set attribute to Constant [{name}]")
        else:
            super().__setattr__(name, value)

class Constant(metaclass=ConstantMeta):
     """定数クラス"""
     pass

