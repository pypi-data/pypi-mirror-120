
from pystage.core.sprite import CoreSprite


class スプライト():
    def __init__(self, core_sprite):
        self._core : CoreSprite = core_sprite
        self._core.facade = self


            
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
                
    def このクローンを削除する(self):
        """このクローンを削除する

        Translation string: このクローンを削除する
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.control_delete_this_clone()
                
    def クローンされたとき(self, key, generator_function, name='', no_refresh=False):
        """クローンされたとき

        Translation string: クローンされたとき
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
        return self._core.control_start_as_clone(key, generator_function, name, no_refresh)
                
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
                
    def 大きさを_ずつ変える(self, percent):
        """大きさを %1 ずつ変える

        Translation string: 大きさを %1 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        percent : FILL
        

        Returns
        -------

        """
        return self._core.looks_changesizeby(percent)
                
    def 画像効果をなくす(self):
        """画像効果をなくす

        Translation string: 画像効果をなくす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_cleargraphiceffects()
                
    def コスチュームの_名前(self):
        """コスチュームの 名前

        Translation string: コスチュームの 名前
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_costumenumbername_name()
                
    def コスチュームの_番号(self):
        """コスチュームの 番号

        Translation string: コスチュームの 番号
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_costumenumbername_number()
                
    def 層_奥に下げる(self, value):
        """%2 層 奥に下げる

        Translation string: %2 層 奥に下げる
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_goforwardbackwardlayers_backward(value)
                
    def 層_手前に出す(self, value):
        """%2 層 手前に出す

        Translation string: %2 層 手前に出す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.looks_goforwardbackwardlayers_forward(value)
                
    def 最背面_へ移動する(self):
        """最背面 へ移動する

        Translation string: 最背面 へ移動する
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_gotofrontback_back()
                
    def 最前面_へ移動する(self):
        """最前面 へ移動する

        Translation string: 最前面 へ移動する
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_gotofrontback_front()
                
    def 隠す(self):
        """隠す

        Translation string: 隠す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_hide()
                
    def 次の背景(self):
        """次の背景

        Translation string: 次の背景
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_nextbackdrop()
                
    def 次のコスチュームにする(self):
        """次のコスチュームにする

        Translation string: 次のコスチュームにする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_nextcostume()
                
    def と言う(self, text):
        """%1 と言う

        Translation string: %1 と言う
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        text : FILL
        

        Returns
        -------

        """
        return self._core.looks_say(text)
                
    def と_秒言う(self, text, secs):
        """%1 と %2 秒言う

        Translation string: %1 と %2 秒言う
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        text : FILL
        secs : FILL
        

        Returns
        -------

        """
        return self._core.looks_sayforsecs(text, secs)
                
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
                
    def 大きさを_にする(self, percent):
        """大きさを %1 %にする

        Translation string: 大きさを %1 %にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        percent : FILL
        

        Returns
        -------

        """
        return self._core.looks_setsizeto(percent)
                
    def 表示する(self):
        """表示する

        Translation string: 表示する
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_show()
                
    def 大きさ(self):
        """大きさ

        Translation string: 大きさ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.looks_size()
                
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
                
    def コスチュームを_にする(self, costume):
        """コスチュームを %1 にする

        Translation string: コスチュームを %1 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        costume : FILL
        

        Returns
        -------

        """
        return self._core.looks_switchcostumeto(costume)
                
    def と考える(self, text):
        """%1 と考える

        Translation string: %1 と考える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        text : FILL
        

        Returns
        -------

        """
        return self._core.looks_think(text)
                
    def と_秒考える(self, text, secs):
        """%1 と %2 秒考える

        Translation string: %1 と %2 秒考える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        text : FILL
        secs : FILL
        

        Returns
        -------

        """
        return self._core.looks_thinkforsecs(text, secs)
                
    def x座標を_ずつ変える(self, value):
        """x座標を %1 ずつ変える

        Translation string: x座標を %1 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.motion_changexby(value)
                
    def y座標を_ずつ変える(self, value):
        """y座標を %1 ずつ変える

        Translation string: y座標を %1 ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.motion_changeyby(value)
                
    def 向き(self):
        """向き

        Translation string: 向き
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_direction()
                
                
    def 秒で_マウスのポインター_へ行く(self, secs):
        """%1 秒で マウスのポインター へ行く

        Translation string: %1 秒で マウスのポインター へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        secs : FILL
        

        Returns
        -------

        """
        return self._core.motion_glideto_pointer(secs)
                
    def 秒で_どこかの場所_へ行く(self, secs):
        """%1 秒で どこかの場所 へ行く

        Translation string: %1 秒で どこかの場所 へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        secs : FILL
        

        Returns
        -------

        """
        return self._core.motion_glideto_random(secs)
                
    def 秒で_へ行く(self, secs, sprite):
        """%1 秒で %2 へ行く

        Translation string: %1 秒で %2 へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        secs : FILL
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.motion_glideto_sprite(secs, sprite)
                
    def マウスのポインター_へ行く(self):
        """マウスのポインター へ行く

        Translation string: マウスのポインター へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_goto_pointer()
                
    def どこかの場所_へ行く(self):
        """どこかの場所 へ行く

        Translation string: どこかの場所 へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_goto_random()
                
    def へ行く(self, sprite):
        """%1 へ行く

        Translation string: %1 へ行く
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.motion_goto_sprite(sprite)
                
    def 座標を座標を_にする(self, x, y):
        """x座標を %1 、y座標を %2 にする

        Translation string: x座標を %1 、y座標を %2 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        x : FILL
        y : FILL
        

        Returns
        -------

        """
        return self._core.motion_gotoxy(x, y)
                
                
    def 歩動かす(self, steps):
        """%1 歩動かす

        Translation string: %1 歩動かす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        steps : FILL
        

        Returns
        -------

        """
        return self._core.motion_movesteps(steps)
                
    def 度に向ける(self, direction):
        """%1 度に向ける

        Translation string: %1 度に向ける
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        direction : FILL
        

        Returns
        -------

        """
        return self._core.motion_pointindirection(direction)
                
    def マウスのポインター_へ向ける(self):
        """マウスのポインター へ向ける

        Translation string: マウスのポインター へ向ける
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_pointtowards_pointer()
                
    def へ向ける(self, sprite):
        """%1 へ向ける

        Translation string: %1 へ向ける
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.motion_pointtowards_sprite(sprite)
                
    def 回転方法を_自由に回転_にする(self):
        """回転方法を 自由に回転 にする

        Translation string: 回転方法を 自由に回転 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_setrotationstyle_allaround()
                
    def 回転方法を_回転しない_にする(self):
        """回転方法を 回転しない にする

        Translation string: 回転方法を 回転しない にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_setrotationstyle_dontrotate()
                
    def 回転方法を_明るさ_にする(self):
        """回転方法を 明るさ にする

        Translation string: 回転方法を 明るさ にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_setrotationstyle_leftright()
                
    def x座標を_にする(self, value):
        """x座標を %1 にする

        Translation string: x座標を %1 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.motion_setx(value)
                
    def y座標を_にする(self, value):
        """y座標を %1 にする

        Translation string: y座標を %1 にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.motion_sety(value)
                
    def 左_度回す(self, deg):
        """左 %2 度回す

        Translation string: 左 %2 度回す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        deg : FILL
        

        Returns
        -------

        """
        return self._core.motion_turnleft(deg)
                
    def 右_度回す(self, deg):
        """右 %2 度回す

        Translation string: 右 %2 度回す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        deg : FILL
        

        Returns
        -------

        """
        return self._core.motion_turnright(deg)
                
    def x座標(self):
        """x座標

        Translation string: x座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_xposition()
                
    def y座標(self):
        """y座標

        Translation string: y座標
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.motion_yposition()
                
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
                
    def ペンの明るさをずつ変える(self, value):
        """ペンの明るさを[VALUE]ずつ変える

        Translation string: ペンの明るさを[VALUE]ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_changePenColorParamBy_brightness(value)
                
    def ペンの色をずつ変える(self, value):
        """ペンの色を[VALUE]ずつ変える
        TODO TRANSLATORS: Needs to be distinguished from setPenColorToColor. This is only the hue value.
        

        Translation string: ペンの色を[VALUE]ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_changePenColorParamBy_color(value)
                
    def ペンの鮮やかさをずつ変える(self, value):
        """ペンの鮮やかさを[VALUE]ずつ変える

        Translation string: ペンの鮮やかさを[VALUE]ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_changePenColorParamBy_saturation(value)
                
    def ペンの透明度をずつ変える(self, value):
        """ペンの透明度を[VALUE]ずつ変える

        Translation string: ペンの透明度を[VALUE]ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_changePenColorParamBy_transparency(value)
                
    def ペンの太さをずつ変える(self, value):
        """ペンの太さを[SIZE]ずつ変える

        Translation string: ペンの太さを[SIZE]ずつ変える
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_changePenSizeBy(value)
                
    def 全部消す(self):
        """全部消す

        Translation string: 全部消す
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.pen_clear()
                
    def ペンを下ろす(self):
        """ペンを下ろす

        Translation string: ペンを下ろす
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.pen_penDown()
                
    def ペンを上げる(self):
        """ペンを上げる

        Translation string: ペンを上げる
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.pen_penUp()
                
    def ペンの明るさをにする(self, value):
        """ペンの明るさを[VALUE]にする

        Translation string: ペンの明るさを[VALUE]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenColorParamTo_brightness(value)
                
    def ペンの色をにする(self, value):
        """ペンの色を[VALUE]にする
        TODO TRANSLATORS: Needs to be distinguished from setPenColorToColor. This is only the hue value.
        

        Translation string: ペンの色を[VALUE]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenColorParamTo_color(value)
                
    def ペンの鮮やかさをにする(self, value):
        """ペンの鮮やかさを[VALUE]にする

        Translation string: ペンの鮮やかさを[VALUE]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenColorParamTo_saturation(value)
                
    def ペンの透明度をにする(self, value):
        """ペンの透明度を[VALUE]にする

        Translation string: ペンの透明度を[VALUE]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenColorParamTo_transparency(value)
                
    def ペンの色をにする(self, color):
        """ペンの色を[COLOR]にする

        Translation string: ペンの色を[COLOR]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        color : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenColorToColor(color)
                
    def ペンの太さをにする(self, value):
        """ペンの太さを[SIZE]にする

        Translation string: ペンの太さを[SIZE]にする
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        value : FILL
        

        Returns
        -------

        """
        return self._core.pen_setPenSizeTo(value)
                
    def スタンプ(self):
        """スタンプ

        Translation string: スタンプ
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.pen_stamp()
                
    def pystage_addcostume(self, name, center_x=None, center_y=None, factor=1):
        """

        Translation string: 
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        name : FILL
        center_x : FILL
        center_y : FILL
        factor : FILL
        

        Returns
        -------

        """
        return self._core.pystage_addcostume(name, center_x, center_y, factor)
                
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
                
    def pystage_insertcostume(self, index, name, center_x=None, center_y=None, factor=1):
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
        factor : FILL
        

        Returns
        -------

        """
        return self._core.pystage_insertcostume(index, name, center_x, center_y, factor)
                
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
                
    def pystage_replacecostume(self, index, name, center_x=None, center_y=None, factor=1):
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
        factor : FILL
        

        Returns
        -------

        """
        return self._core.pystage_replacecostume(index, name, center_x, center_y, factor)
                
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
                
    def 色が_色に触れた(self, sprite_color, color):
        """%1 色が %2 色に触れた

        Translation string: %1 色が %2 色に触れた
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite_color : FILL
        color : FILL
        

        Returns
        -------

        """
        return self._core.sensing_coloristouchingcolor(sprite_color, color)
                
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
                
    def マウスのポインター_までの距離(self):
        """マウスのポインター までの距離

        Translation string: マウスのポインター までの距離
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_distanceto_pointer()
                
    def までの距離(self, sprite):
        """%1 までの距離

        Translation string: %1 までの距離
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_distanceto_sprite(sprite)
                
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
                
    def 色に触れた(self, color):
        """%1 色に触れた

        Translation string: %1 色に触れた
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        color : FILL
        

        Returns
        -------

        """
        return self._core.sensing_touchingcolor(color)
                
    def 端_に触れた(self):
        """端 に触れた

        Translation string: 端 に触れた
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_touchingobject_edge()
                
    def マウスのポインター_に触れた(self):
        """マウスのポインター に触れた

        Translation string: マウスのポインター に触れた
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        

        Returns
        -------

        """
        return self._core.sensing_touchingobject_pointer()
                
    def に触れた(self, sprite):
        """%1 に触れた

        Translation string: %1 に触れた
        Engl. Translation for your reference: ...
        Engl. Documentation when available...

        
        Parameters
        ----------
        sprite : FILL
        

        Returns
        -------

        """
        return self._core.sensing_touchingobject_sprite(sprite)
                
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
                
