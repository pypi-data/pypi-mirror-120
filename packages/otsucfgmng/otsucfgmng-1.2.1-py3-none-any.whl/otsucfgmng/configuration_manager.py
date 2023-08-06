import copy
import json

from pathlib import Path
from typing import Any, List, Union, cast

from otsutil import OtsuNone, load_json, save_json
from otsuvalidator import CPath
from otsuvalidator.validators import VTuple

from .funcs import get_dict_keys_position, support_json_dump


class MetaCM(type):
    def __new__(cls, name: str, bases: tuple, attrs: dict):
        excludes = {'__module__', '__qualname__', '__defaults__', '__hidden_options__', '__annotations__'}
        attr_keys = set(attrs.keys()) - excludes
        if (dflt := attrs.get('__defaults__', OtsuNone)) is not OtsuNone:
            dflt = cast(dict, dflt)
            kp: dict = {}
            for k, v, position in get_dict_keys_position(dflt):
                if k not in attr_keys:
                    msg = f'属性"{k}"は宣言されていません。'
                    raise AttributeError(msg)
                if kp.get(k, OtsuNone) is not OtsuNone:
                    msg = f'属性"{k}"は異なるセクションに存在しています。'
                    raise AttributeError(msg)
                kp[k] = position
            if (undefined := attr_keys - set(kp.keys())):
                msg = f'これらの属性の初期値が設定されていません。{undefined}'
                raise AttributeError(msg)
            attrs['__attr_keys__'] = attr_keys
            attrs['__key_place__'] = kp
            attrs['__user__'] = {}
        return type.__new__(cls, name, bases, attrs)


class BaseCM(metaclass=MetaCM):
    """設定ファイル管理クラス用の基底クラスです。

    このクラスを継承したクラスに__defaults__, <attribute>を定義するだけで、設定ファイルの読み書きに必要な処理を行えるようになります。

    拡張子に制約はありませんが、読み込んだ際に辞書形式のjsonである必要があります。
    """
    __file__ = CPath()
    __hidden_options__ = VTuple(str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.save_cm()
        except Exception as e:
            return False

    def __init__(self, __file__: Union[str, Path]):
        """設定ファイルを指定して、扱えるようにします。

        Args:
            __file__ (Union[str, Path]): 設定ファイルのパスです。
        """
        self.__file__ = cast(Path, __file__)
        dflt = self.defaults_cm()
        cfu = cast(dict, self.__user__)
        kp = self.key_place_cm()
        for k in self.attributes_cm():
            d = dflt
            u = cfu
            if (place := kp[k]) is not None:
                for p in place:
                    d = d[p]
                    if u.get(p, OtsuNone) is OtsuNone:
                        u[p] = {}
                    u = u[p]
            setattr(self, k, d[k])
            setattr(self, f'default_{k}_cm', getattr(self, k))
        self.load_cm()

    def __getattr__(self, key):
        msg = f'属性"{key}"は存在しません。'
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: Any) -> None:
        nsp = name.split('_')
        if nsp[0] == 'default' and nsp[-1] == 'cm':
            f, *n, l = nsp
            n = '_'.join(n)
            if getattr(self, n, OtsuNone) is not OtsuNone:
                if self.__dict__.get(name, OtsuNone) is not OtsuNone:
                    msg = f'属性"{name}"は上書きできません。'
                    raise AttributeError(msg)
            else:
                msg = f'属性"{n}"が存在しないため、その初期値を表す属性"{name}"も存在しません。'
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def cfg_to_str_cm(self, all: bool = False) -> str:
        """設定をjson.dumpsして返します。

        self.__hidden_options__はユーザが変更している場合のみ表示されます。

        allが有効の場合、defaults, userという2つのセクションからなる辞書として扱われます。

        Args:
            all (bool, optional): 標準設定を表示するかどうかです。

        Returns:
            str: 設定の文字列です。
        """
        if all:
            tmp = {'defaults': copy.deepcopy(self.defaults_cm()), 'user': self.user_cm()}
            kp = cast(dict, self.key_place_cm())
            if (ho := getattr(self, '__hidden_options__', OtsuNone)) is not OtsuNone:
                ho = set(cast(tuple, ho))
                for key in ho:
                    if (place := kp.get(key, OtsuNone)) is OtsuNone:
                        continue
                    dflt = tmp['defaults']
                    user = tmp['user']
                    if place is not None:
                        place = cast(List[str], place)
                        for p in place:
                            dflt = dflt[p]
                            user = user[p]
                    if user.get(key, OtsuNone) is OtsuNone:
                        del dflt[key]
        else:
            tmp = self.user_cm()
        return json.dumps(tmp, indent=4, ensure_ascii=False, default=support_json_dump, sort_keys=True)

    def load_cm(self, **kwargs):
        """設定ファイルを読み込みます。

        読み込んだ設定を基にインスタンスの属性を更新します。

        Raises:
            TypeError: 設定ファイルが既定の形式ではない場合に投げられます。
        """
        if not self.__file__.exists():
            return
        kwargs['file'] = self.__file__
        try:
            jsn = load_json(**kwargs)
        except:
            return
        if not isinstance(jsn, dict):
            msg = f'{self.__file__}は対応していない形式です。'
            raise TypeError(msg)
        jsn = cast(dict, jsn)
        for key, places in self.key_place_cm().items():
            d = jsn
            if places is not None:
                for p in places:
                    d = d.get(p, OtsuNone)  # type: ignore
                    if d is OtsuNone:
                        continue
            if (dk := d.get(key, OtsuNone)) is OtsuNone:  # type: ignore
                continue
            setattr(self, key, dk)

    def save_cm(self, **kwargs):
        """設定ファイルを書き出します。

        書き出す項目はユーザが変更を行ったもののみになり、クラス既定の初期設定が書き出されることはありません。

        キーワード引数にはjson.dumpで使用できる引数を与えることができます。
        一部引数は指定しなかった場合以下の値が使用されます。
        またfpはself.__file__固定になります。

        indent: 4
        encoding: utf-8
        ensure_ascii: False
        default: support_json_dump
        sort_keys: True
        """
        user = self.user_cm()
        kwargs['file'] = self.__file__
        kwargs['data'] = user
        set_kwargs = (('indent', 4), ('ensure_ascii', False), ('default', support_json_dump), ('sort_keys', True))
        for k, v in set_kwargs:
            if kwargs.get(k, OtsuNone) is OtsuNone:
                kwargs[k] = v
        save_json(**kwargs)

    def reset_cm(self):
        """各属性を初期値に戻します。
        """
        dflt = lambda x: f'default_{x}_cm'
        for key in self.attributes_cm():
            setattr(self, key, getattr(self, dflt(key)))

    def defaults_cm(self) -> dict:
        """各属性の初期値の辞書を返します。

        Returns:
            dict: 各属性の初期値です。
        """
        return copy.deepcopy(cast(dict, self.__defaults__))

    def user_cm(self) -> dict:
        """ユーザが変更した属性の辞書を返します。

        Returns:
            dict: ユーザが変更した属性の辞書です。
        """
        user = cast(dict, self.__user__)
        place = self.key_place_cm()
        for k in self.attributes_cm():
            uv = getattr(self, k)
            dv = getattr(self, f'default_{k}_cm')
            position = place[k]
            u = user
            if position is not None:
                for p in position:
                    u = u[p]
            if uv == dv:
                if u.get(k, OtsuNone) is not OtsuNone:
                    del u[k]
            else:
                u[k] = uv
        return user

    def key_place_cm(self) -> dict:
        """各属性の保存先を記録する辞書です。

        Returns:
            dict: 各属性の保存先を記録する辞書です。
        """
        return cast(dict, self.__key_place__)

    def attributes_cm(self) -> set:
        """クラス定義の属性名セットです。

        Returns:
            set: クラス定義の属性名セットです。
        """
        return cast(set, self.__attr_keys__)
