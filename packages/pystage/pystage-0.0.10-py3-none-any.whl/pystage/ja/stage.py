
from pystage.core.stage import CoreStage
from pystage.ja.sprite import スプライト


class ステージ():

    def __init__(self):
        self._core = CoreStage()
        self._core.facade = self
        self._core.sprite_facade_class = スプライト

    def スプライトを追加しよう(self, costume="default"):
        return self._core.pystage_createsprite(costume=costume)

    def 再生(self):
        self._core.pystage_play()
        
            
    def のクローンを作る(self, sprite='_myself_'):
        """%1 のクローンを作る

        Translation string: %1 のクローンを作る
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.control_create_clone_of(sprite)
                
                
                
                
    def 秒待つ(self, secs):
        """%1 秒待つ

        Translation string: %1 秒待つ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        secs : FILL
        

        Returns
        -------

        """
        return self._core.control_wait(secs)
                
    def を_ずつ変える(self, name, value):
        """%1 を %2 ずつ変える

        Translation string: %1 を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        value : FILL
        

        Returns
        -------

        """
        return self._core.data_changevariableby(name, value)
                
    def 変数_を隠す(self, name):
        """変数 %1 を隠す

        Translation string: 変数 %1 を隠す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        

        Returns
        -------

        """
        return self._core.data_hidevariable(name)
                
    def を_にする(self, name, value):
        """%1 を %2 にする

        Translation string: %1 を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        value : FILL
        

        Returns
        -------

        """
        return self._core.data_setvariableto(name, value)
                
    def 変数_を表示する(self, name):
        """変数 %1 を表示する

        Translation string: 変数 %1 を表示する
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        

        Returns
        -------

        """
        return self._core.data_showvariable(name)
                
    def data_variable(self, name):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        

        Returns
        -------

        """
        return self._core.data_variable(name)
                
    def を送る(self, message):
        """%1 を送る

        Translation string: %1 を送る
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        message : FILL
        

        Returns
        -------

        """
        return self._core.event_broadcast(message)
                
    def を送って待つ(self, message):
        """%1 を送って待つ

        Translation string: %1 を送って待つ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        message : FILL
        

        Returns
        -------

        """
        return self._core.event_broadcastandwait(message)
                
    def 背景が_になったとき(self, backdrop, generator_function, name='', no_refresh=False):
        """背景が %1 になったとき

        Translation string: 背景が %1 になったとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        backdrop : FILL
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whenbackdropswitchesto(backdrop, generator_function, name, no_refresh)
                
    def を受け取ったとき(self, message, generator_function, name='', no_refresh=False):
        """%1 を受け取ったとき

        Translation string: %1 を受け取ったとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        message : FILL
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whenbroadcastreceived(message, generator_function, name, no_refresh)
                
    def GREENFLAG_が押されたとき(self, generator_function, name='', no_refresh=False):
        """<greenflag> が押されたとき

        Translation string: <greenflag> が押されたとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whenflagclicked(generator_function, name, no_refresh)
                
    def 音量_GREATERTHAN_のとき(self, value, generator_function, name='', no_refresh=False):
        """音量 <greater> %2 のとき

        Translation string: 音量 <greater> %2 のとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whengreaterthan_loudness(value, generator_function, name, no_refresh)
                
    def タイマー_GREATERTHAN_のとき(self, value, generator_function, name='', no_refresh=False):
        """タイマー <greater> %2 のとき

        Translation string: タイマー <greater> %2 のとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whengreaterthan_timer(value, generator_function, name, no_refresh)
                
    def キーが押されたとき(self, key, generator_function, name='', no_refresh=False):
        """%1 キーが押されたとき

        Translation string: %1 キーが押されたとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        key : FILL
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whenkeypressed(key, generator_function, name, no_refresh)
                
    def このスプライトが押されたとき(self, generator_function, name='', no_refresh=False):
        """このスプライトが押されたとき

        Translation string: このスプライトが押されたとき
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        generator_function : FILL
        name : FILL
        no_refresh : FILL
        

        Returns
        -------

        """
        return self._core.event_whenthisspriteclicked(generator_function, name, no_refresh)
                
    def 背景の_名前(self):
        """背景の 名前

        Translation string: 背景の 名前
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_backdropnumbername_name()
                
    def 背景の_番号(self):
        """背景の 番号

        Translation string: 背景の 番号
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_backdropnumbername_number()
                
    def 明るさ_の効果を_ずつ変える(self, value):
        """明るさ の効果を %2 ずつ変える

        Translation string: 明るさ の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_brightness(value)
                
    def 色_の効果を_ずつ変える(self, value):
        """色 の効果を %2 ずつ変える

        Translation string: 色 の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_color(value)
                
    def 魚眼レンズ_の効果を_ずつ変える(self, value):
        """魚眼レンズ の効果を %2 ずつ変える

        Translation string: 魚眼レンズ の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_fisheye(value)
                
    def 幽霊_の効果を_ずつ変える(self, value):
        """幽霊 の効果を %2 ずつ変える

        Translation string: 幽霊 の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_ghost(value)
                
    def モザイク_の効果を_ずつ変える(self, value):
        """モザイク の効果を %2 ずつ変える

        Translation string: モザイク の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_mosaic(value)
                
    def ピクセル化_の効果を_ずつ変える(self, value):
        """ピクセル化 の効果を %2 ずつ変える

        Translation string: ピクセル化 の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_pixelate(value)
                
    def 渦巻き_の効果を_ずつ変える(self, value):
        """渦巻き の効果を %2 ずつ変える

        Translation string: 渦巻き の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_changeeffectby_whirl(value)
                
    def 画像効果をなくす(self):
        """画像効果をなくす

        Translation string: 画像効果をなくす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_cleargraphiceffects()
                
    def 次の背景(self):
        """次の背景

        Translation string: 次の背景
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_nextbackdrop()
                
    def 明るさ_の効果を_にする(self, value):
        """明るさ の効果を %2 にする

        Translation string: 明るさ の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_brightness(value)
                
    def 色_の効果を_にする(self, value):
        """色 の効果を %2 にする

        Translation string: 色 の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_color(value)
                
    def 魚眼レンズ_の効果を_にする(self, value):
        """魚眼レンズ の効果を %2 にする

        Translation string: 魚眼レンズ の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_fisheye(value)
                
    def 幽霊_の効果を_にする(self, value):
        """幽霊 の効果を %2 にする

        Translation string: 幽霊 の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_ghost(value)
                
    def モザイク_の効果を_にする(self, value):
        """モザイク の効果を %2 にする

        Translation string: モザイク の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_mosaic(value)
                
    def ピクセル化_の効果を_にする(self, value):
        """ピクセル化 の効果を %2 にする

        Translation string: ピクセル化 の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_pixelate(value)
                
    def 渦巻き_の効果を_にする(self, value):
        """渦巻き の効果を %2 にする

        Translation string: 渦巻き の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_seteffectto_whirl(value)
                
    def 背景を_にする(self, backdrop):
        """背景を %1 にする

        Translation string: 背景を %1 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        backdrop : FILL
        

        Returns
        -------

        """
        return self._core.looks_switchbackdropto(backdrop)
                
    def 背景を_にして待つ(self, backdrop):
        """背景を %1 にして待つ

        Translation string: 背景を %1 にして待つ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        backdrop : FILL
        

        Returns
        -------

        """
        return self._core.looks_switchbackdroptoandwait(backdrop)
                
    def の(self, operator, number):
        """%2 の %1

        Translation string: %2 の %1
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        operator : FILL
        number : FILL
        

        Returns
        -------

        """
        return self._core.operator_mathop(operator, number)
                
    def から_までの乱数(self, start, end):
        """%1 から %2 までの乱数

        Translation string: %1 から %2 までの乱数
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        start : FILL
        end : FILL
        

        Returns
        -------

        """
        return self._core.operator_random(start, end)
                
    def pystage_addbackdrop(self, name, center_x=None, center_y=None):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        center_x : FILL
        center_y : FILL
        

        Returns
        -------

        """
        return self._core.pystage_addbackdrop(name, center_x, center_y)
                
    def pystage_addsound(self, name):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        

        Returns
        -------

        """
        return self._core.pystage_addsound(name)
                
    def pystage_createsprite(self, costume='default'):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        costume : FILL
        

        Returns
        -------

        """
        return self._core.pystage_createsprite(costume)
                
    def pystage_insertbackdrop(self, index, name, center_x=None, center_y=None):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        index : FILL
        name : FILL
        center_x : FILL
        center_y : FILL
        

        Returns
        -------

        """
        return self._core.pystage_insertbackdrop(index, name, center_x, center_y)
                
    def pystage_makevariable(self, name, all_sprites=True):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        all_sprites : FILL
        

        Returns
        -------

        """
        return self._core.pystage_makevariable(name, all_sprites)
                
    def pystage_play(self):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.pystage_play()
                
    def pystage_replacebackdrop(self, index, name, center_x=None, center_y=None):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        index : FILL
        name : FILL
        center_x : FILL
        center_y : FILL
        

        Returns
        -------

        """
        return self._core.pystage_replacebackdrop(index, name, center_x, center_y)
                
    def pystage_setmonitorposition(self, name, x, y):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        x : FILL
        y : FILL
        

        Returns
        -------

        """
        return self._core.pystage_setmonitorposition(name, x, y)
                
    def 答え(self):
        """答え

        Translation string: 答え
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_answer()
                
    def と聞いて待つ(self, question):
        """%1 と聞いて待つ

        Translation string: %1 と聞いて待つ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        question : FILL
        

        Returns
        -------

        """
        return self._core.sensing_askandwait(question)
                
    def 現在の_日(self):
        """現在の 日

        Translation string: 現在の 日
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_date()
                
    def 現在の_曜日(self):
        """現在の 曜日

        Translation string: 現在の 曜日
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_dayofweek()
                
    def 現在の_時(self):
        """現在の 時

        Translation string: 現在の 時
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_hour()
                
    def 現在の_分(self):
        """現在の 分

        Translation string: 現在の 分
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_minute()
                
    def 現在の_月(self):
        """現在の 月

        Translation string: 現在の 月
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_month()
                
    def 現在の_秒(self):
        """現在の 秒

        Translation string: 現在の 秒
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_second()
                
    def 現在の_年(self):
        """現在の 年

        Translation string: 現在の 年
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_current_year()
                
    def 年からの日数(self):
        """2000年からの日数

        Translation string: 2000年からの日数
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_dayssince2000()
                
    def キーが押された(self, key):
        """%1 キーが押された

        Translation string: %1 キーが押された
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        key : FILL
        

        Returns
        -------

        """
        return self._core.sensing_keypressed(key)
                
    def 音量(self):
        """音量

        Translation string: 音量
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_loudness()
                
    def マウスが押された(self):
        """マウスが押された

        Translation string: マウスが押された
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_mousedown()
                
    def マウスのx座標(self):
        """マウスのx座標

        Translation string: マウスのx座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_mousex()
                
    def マウスのy座標(self):
        """マウスのy座標

        Translation string: マウスのy座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_mousey()
                
    def の_背景の名前(self, stage='_stage_'):
        """%2 の 背景の名前

        Translation string: %2 の 背景の名前
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        stage : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_backdropname(stage)
                
    def の_背景(self, stage='_stage_'):
        """%2 の 背景 #

        Translation string: %2 の 背景 #
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        stage : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_backdropnumber(stage)
                
    def の_コスチューム名(self, sprite):
        """%2 の コスチューム名

        Translation string: %2 の コスチューム名
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_costumename(sprite)
                
    def の_コスチューム(self, sprite):
        """%2 の コスチューム #

        Translation string: %2 の コスチューム #
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_costumenumber(sprite)
                
    def の_向き(self, sprite):
        """%2 の 向き

        Translation string: %2 の 向き
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_direction(sprite)
                
    def の_大きさ(self, sprite):
        """%2 の 大きさ

        Translation string: %2 の 大きさ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_size(sprite)
                
    def の(self, variable, sprite='_stage_'):
        """%2 の %1

        Translation string: %2 の %1
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        variable : FILL
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_variable(variable, sprite)
                
    def の_音量(self, sprite='_stage_'):
        """%2 の 音量

        Translation string: %2 の 音量
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_volume(sprite)
                
    def の_x座標(self, sprite):
        """%2 の x座標

        Translation string: %2 の x座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_xposition(sprite)
                
    def の_y座標(self, sprite):
        """%2 の y座標

        Translation string: %2 の y座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_of_yposition(sprite)
                
    def タイマーをリセット(self):
        """タイマーをリセット

        Translation string: タイマーをリセット
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_resettimer()
                
    def ドラッグ_できる_ようにする(self):
        """ドラッグ できる ようにする

        Translation string: ドラッグ できる ようにする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_setdragmode_draggable()
                
    def ドラッグ_できない_ようにする(self):
        """ドラッグ できない ようにする

        Translation string: ドラッグ できない ようにする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_setdragmode_notdraggable()
                
    def タイマー(self):
        """タイマー

        Translation string: タイマー
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_timer()
                
    def ユーザー名(self):
        """ユーザー名

        Translation string: ユーザー名
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_username()
                
    def 左右にパン_の効果を_ずつ変える(self, value):
        """左右にパン の効果を %2 ずつ変える

        Translation string: 左右にパン の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_changeeffectby_pan(value)
                
    def ピッチ_の効果を_ずつ変える(self, value):
        """ピッチ の効果を %2 ずつ変える

        Translation string: ピッチ の効果を %2 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_changeeffectby_pitch(value)
                
    def 音量を_ずつ変える(self, value):
        """音量を %1 ずつ変える

        Translation string: 音量を %1 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_changevolumeby(value)
                
    def 音の効果をなくす(self):
        """音の効果をなくす

        Translation string: 音の効果をなくす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sound_cleareffects()
                
    def の音を鳴らす(self, name, loop=0):
        """%1 の音を鳴らす

        Translation string: %1 の音を鳴らす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        loop : FILL
        

        Returns
        -------

        """
        return self._core.sound_play(name, loop)
                
    def 終わるまで_の音を鳴らす(self, name):
        """終わるまで %1 の音を鳴らす

        Translation string: 終わるまで %1 の音を鳴らす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        

        Returns
        -------

        """
        return self._core.sound_playuntildone(name)
                
    def 左右にパン_の効果を_にする(self, value):
        """左右にパン の効果を %2 にする

        Translation string: 左右にパン の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_seteffectto_pan(value)
                
    def ピッチ_の効果を_にする(self, value):
        """ピッチ の効果を %2 にする

        Translation string: ピッチ の効果を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_seteffectto_pitch(value)
                
    def 音量を_にする(self, value):
        """音量を %1 %にする

        Translation string: 音量を %1 %にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.sound_setvolumeto(value)
                
    def すべての音を止める(self):
        """すべての音を止める

        Translation string: すべての音を止める
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sound_stopallsounds()
                
    def 音量(self):
        """音量

        Translation string: 音量
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sound_volume()
                
