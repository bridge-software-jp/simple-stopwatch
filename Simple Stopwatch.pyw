# -*- coding: UTF-8 -*-

'''
---------------------------------------------------------------------------
 FileName : Simple Stopwatch.pyw
 Overview : シンプルストップウォッチ
 Version  : 1.0.2

 Copyright(c) 2016 Takeshi Hashimoto All Right Reserved.
---------------------------------------------------------------------------

----------------------------------------------------------------------------
 Revision History
----------------------------------------------------------------------------

 Version 1.0.2
 Date    2016年05月23日
 Content 現状の設定内容を設定ダイアログに反映するように変更

 Version 1.0.1
 Date    2016年05月19日
 Content 個別設定を可能にした

 Version 1.0.0
 Date    2016年05月吉日
 Content 新規作成
----------------------------------------------------------------------------
'''

import wx
import datetime
import xml.etree.ElementTree as ET
from datetime import timedelta

# xmlファイルの取得
xml = ET.parse("Settings.xml")
x = int(xml.find('x').text) # ポジション：X
y = int(xml.find('y').text) # ポジション：Y
bc1 = int(xml.find('back_c1').text) # 背景色1
bc2 = int(xml.find('back_c2').text) # 背景色2
bc3 = int(xml.find('back_c3').text) # 背景色3
fc1 = int(xml.find('fore_c1').text) # 文字色1
fc2 = int(xml.find('fore_c2').text) # 文字色2
fc3 = int(xml.find('fore_c3').text) # 文字色3
fr = int(xml.find('front').text) # 最前面可否
tr = int(xml.find('trans').text) # 透過度
tr2 = tr - 155

bc = (bc1, bc2, bc3)
fc = (fc1, fc2, fc3)


# メインクラス
class App(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(200,180))

        # 背景色
        self.SetBackgroundColour(bc)
        # 透過度
        self.SetTransparent(tr)

        # スタイル
        if fr == 0:
            self.SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        # アイコン
        icon = wx.Icon("clock.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 表示位置
        posi = wx.Point(x, y)
        self.SetPosition(posi)

        # タイマーイベント
        self.Bind(wx.EVT_TIMER, self.course)

        # クローズイベント
        self.Bind(wx.EVT_CLOSE, self.close)

        # フォント
        self.font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, face=u'メイリオ')
        self.font2 = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, face=u'メイリオ')
        self.SetFont(self.font)

        # パネル
        self.panel = wx.Panel(self, wx.ID_ANY)

        # 時間表示テキスト
        self.label = wx.TextCtrl(self.panel, -1, '0:00:00.00', style=wx.TE_CENTRE | wx.TE_READONLY | wx.NO_BORDER)
        self.label.SetFont(self.font2)
        self.label.SetBackgroundColour(bc)
        self.label.SetForegroundColour(fc)

        # 各種ボタン
        self.button1 = wx.Button(self.panel, -1, u'開始')
        self.button1.SetBackgroundColour("#e0ffff")
        self.button1.Bind(wx.EVT_BUTTON, self.start)
        self.button2 = wx.Button(self.panel, -1, u'停止')
        self.button2.Bind(wx.EVT_BUTTON, self.pause)
        self.button2.Enable(False)
        self.button3 = wx.Button(self.panel, -1, u'再開')
        self.button3.Bind(wx.EVT_BUTTON, self.restart)
        self.button3.Enable(False)
        self.button4 = wx.Button(self.panel, -1, u'消去')
        self.button4.Bind(wx.EVT_BUTTON, self.reset)
        self.button4.Enable(False)

        layout = wx.GridSizer(2,2)
        layout.Add(self.button1, flag=wx.EXPAND, proportion=1)
        layout.Add(self.button2, flag=wx.EXPAND, proportion=1)
        layout.Add(self.button3, flag=wx.EXPAND, proportion=1)
        layout.Add(self.button4, flag=wx.EXPAND, proportion=1)

        # 設定ボタン
        self.Setting_button = wx.Button(self.panel, wx.ID_ANY, u'設定')
        self.Setting_button.Bind(wx.EVT_BUTTON, self.settings)

        # レイアウト
        main_layout = wx.BoxSizer(wx.VERTICAL)
        main_layout.Add(wx.Size(0,10))
        main_layout.Add(self.label, flag=wx.EXPAND, proportion=1)
        main_layout.Add(layout, flag=wx.EXPAND, proportion=1)
        main_layout.Add(self.Setting_button, flag=wx.EXPAND, proportion=1)

        self.panel.SetSizer(main_layout)

        self.Show()

    # 開始 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def start(self, event):
        self.button1.Enable(False) # 開始：押せない
        self.button1.SetBackgroundColour("")
        self.button2.Enable(True) # 一時停止：押せる
        self.button2.SetBackgroundColour("yellow")
        self.button4.Enable(False) # 消去：押せない
        self.time = wx.Timer(self)
        self.time.Start(50)
        self.watch = wx.StopWatch()
        self.watch.Start()

    # 停止 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def pause(self, event):
        self.watch.Pause()
        self.button2.Enable(False) # 一時停止：押せない
        self.button2.SetBackgroundColour("")
        self.button3.Enable(True) # 再開：押せる
        self.button3.SetBackgroundColour("green")
        self.button4.Enable(True) # 消去：押せる
        self.button4.SetBackgroundColour("pink")
        self.SetTitle(u'停止中')

    # 再開 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def restart(self, event):
        self.watch.Resume()
        self.button2.Enable(True) # 一時停止：押せる
        self.button2.SetBackgroundColour("yellow")
        self.button3.Enable(False) # 再開：押せない
        self.button3.SetBackgroundColour("")
        self.button4.Enable(False) # 消去：押せない
        self.button4.SetBackgroundColour("")
        self.SetTitle('')

    # 消去 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def reset(self, event):
        self.time.Stop()
        self.button1.Enable(True) # 開始：押せる
        self.button1.SetBackgroundColour("#e0ffff")
        self.button3.Enable(False) # 再開：押せない
        self.button3.SetBackgroundColour("")
        self.button4.Enable(False) # 消去：押せない
        self.button4.SetBackgroundColour("")
        self.label.SetLabel('0:00:00.00')
        self.SetTitle(u'ストップウォッチ')

    # 経過時間表示 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def course(self, event):
        now = str(self.watch.Time())
        now = int(now)
        d = timedelta(milliseconds=now)
        d = str(d)
        self.label.SetLabel(d[:10])
        if self.GetTitle() != u"停止中":
            self.SetTitle(d[:10])

    # 閉じるとき  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def close(self, event):
        self.Destroy()

        # 閉じた時点の表示位置を取得
        position = self.GetPosition()

        # xmlファイルを書き換え
        new_x = xml.find('x')
        new_y = xml.find('y')
        new_x.text = str(position[0])
        new_y.text = str(position[1])

        # XMLファイルの上書き保存
        xml.write('Settings.xml', 'utf-8', True)

    # 設定ダイアログ = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def settings(self, event):

        # 現在の各値をグローバル関数に取得（クラスをまたぐため） - - - - - - - - - -
        global now_bc # 背景色
        global now_fc # 文字色
        now_bc = self.label.GetBackgroundColour()
        now_fc = self.label.GetForegroundColour()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        f2 = CustomDialog(self, u'各種設定')
        result = f2.ShowModal()

        # 設定ダイアログでOKが押された場合
        if result == 100:
            # 設定内容を取得
            set_data = f2.DoAction(self)

            back_c = set_data[0] # 背景色
            fore_c = set_data[1] # 文字色
            front = set_data[2] # 最前面する
            trans = set_data[4] # 透過度

            tuple_bc = (back_c[0], back_c[1], back_c[2])
            tuple_fc = (fore_c[0], fore_c[1], fore_c[2])

            # 各種設定を適用
            # 背景色
            self.SetBackgroundColour(tuple_bc)
            self.label.SetBackgroundColour(tuple_bc)

            # 文字色
            self.label.SetForegroundColour(tuple_fc)

            # 最前面
            if front:
                self.SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP)
                prop = 0
            else:
                self.SetWindowStyle(style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
                prop = 1

            # 透過度
            self.SetTransparent(trans)

            # xmlファイルへの保存
            new_bc1 = xml.find('back_c1')
            new_bc2 = xml.find('back_c2')
            new_bc3 = xml.find('back_c3')
            new_fc1 = xml.find('fore_c1')
            new_fc2 = xml.find('fore_c2')
            new_fc3 = xml.find('fore_c3')
            new_fr = xml.find('front')
            new_tr = xml.find('trans')

            # 書き込み
            new_bc1.text = str(back_c[0])
            new_bc2.text = str(back_c[1])
            new_bc3.text = str(back_c[2])
            new_fc1.text = str(fore_c[0])
            new_fc2.text = str(fore_c[1])
            new_fc3.text = str(fore_c[2])
            new_fr.text = str(prop)
            new_tr.text = str(trans)

            # XMLファイルの上書き保存
            xml.write('Settings.xml', 'utf-8', True)


class CustomDialog(wx.Dialog):
    """ カスタムダイアログ """
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size=(300, 410))

        # フォント
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, face=u'メイリオ')
        self.SetFont(font)

        # リターンコードセット
        self.SetReturnCode(100)

        # パネル
        panel = wx.Panel(self, wx.ID_ANY)

        # 背景色
        label_1 = wx.StaticText(panel, wx.ID_ANY, u'・背景色を変更する')
        picker_1 = wx.ColourPickerCtrl(panel, 11, col=now_bc, style=wx.CLRP_SHOW_LABEL)

        hbox_1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_1.Add(label_1, flag=wx.TOP, border=3)
        hbox_1.Add(picker_1, flag=wx.LEFT, border=30)

        # 文字色
        label_2 = wx.StaticText(panel, wx.ID_ANY, u'・文字色を変更する')
        picker_2 = wx.ColourPickerCtrl(panel, 22, col=now_fc, style=wx.CLRP_SHOW_LABEL)

        hbox_2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_2.Add(label_2, flag=wx.TOP, border=3)
        hbox_2.Add(picker_2, flag=wx.LEFT, border=30)

        # 「色の管理」サイザー
        box_1 = wx.StaticBox(panel, wx.ID_ANY, u'色の管理')
        box1 = wx.StaticBoxSizer(box_1, wx.VERTICAL)
        box1.Add(hbox_1, flag=wx.LEFT | wx.RIGHT, border=10)
        box1.Add(hbox_2, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # 最前面の有無
        radio_1 = wx.RadioButton(panel, 33, u'常に最前面に表示する')
        radio_2 = wx.RadioButton(panel, 44, u'最前面に表示しない')
        if fr == 0:
            radio_1.SetValue(True)
        else:
            radio_2.SetValue(True)

        # 「表示の管理」サイザー
        box_2 = wx.StaticBox(panel, wx.ID_ANY, u'表示の管理')
        box2 = wx.StaticBoxSizer(box_2, wx.VERTICAL)
        box2.Add(radio_1, flag=wx.LEFT | wx.RIGHT, border=10)
        box2.Add(radio_2, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # 透過度用スライダー
        self.slider = wx.Slider(panel, 55, tr2, 0, 100, style=wx.SL_LABELS | wx.SL_AUTOTICKS)
        self.slider.Bind(wx.EVT_SLIDER, self.slide)

        # スライダー用サイザー
        box_3 = wx.StaticBox(panel, wx.ID_ANY, u'透過度の管理')
        box3 = wx.StaticBoxSizer(box_3, wx.VERTICAL)
        box3.Add(self.slider, flag= wx.EXPAND)

        # ボタン
        ok_button = wx.Button(panel, wx.ID_OK, u'決定')
        ca_button = wx.Button(panel, wx.ID_CANCEL, u'キャンセル')
        ok_button.Bind(wx.EVT_BUTTON, self.DoAction)

        # ボタンレイアウト
        bbox = wx.BoxSizer(wx.HORIZONTAL)
        bbox.Add(ok_button, flag=wx.RIGHT, border=20)
        bbox.Add(ca_button)

        # バージョン情報
        ver = wx.StaticText(panel, wx.ID_ANY, u'<ver 1.0.2>')

        # メインレイアウト
        d_layout = wx.BoxSizer(wx.VERTICAL)
        d_layout.Add(box1, flag=wx.ALL | wx.EXPAND, border=10)
        d_layout.Add(box2, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        d_layout.Add(box3, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        d_layout.Add(bbox, flag=wx.ALL | wx.CENTER, border=10)
        d_layout.Add(ver, flag=wx.CENTER)
        panel.SetSizer(d_layout)

        self.Centre()

    # スライダー用関数 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def slide(self, event):
        t = self.slider.GetValue()
        t = int(t) + 155
        self.SetTransparent(t)

    # 設定完了 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def DoAction(self, event):
        target_1 = self.FindWindowById(11) # 背景色
        target_2 = self.FindWindowById(22) # 文字色
        target_3 = self.FindWindowById(33) # 最前面する
        target_4 = self.FindWindowById(44) # 最前面しない
        target_5 = self.FindWindowById(55) # 透過度
        self.Destroy()

        array = []
        array.append(target_1.GetColour())
        array.append(target_2.GetColour())
        array.append(target_3.GetValue())
        array.append(target_4.GetValue())
        array.append(target_5.GetValue() + 155 )

        return array

app = wx.App()
App(None, -1, 'Simple StopWatch')
app.MainLoop()