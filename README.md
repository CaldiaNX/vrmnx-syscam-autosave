# VRMNXシステムカメラ記憶くん

## 概要
「システムカメラ記憶くん」は「[鉄道模型シミュレーターNX](http://www.imagic.co.jp/hobby/products/vrmnx/ "鉄道模型シミュレーターNX")」（VRMNX）のシステムカメラ情報を自動記録するスクリプトです。

## ダウンロード
- [syscam_autosave.py](https://raw.githubusercontent.com/CaldiaNX/vrmnx-syscam-autosave/main/syscam_autosave.py)

## 利用方法
レイアウトファイルと同じフォルダ階層に「syscam_autosave.py」ファイルを配置します。  

フォルダ構成：
```
C:\VRMNX（一例）
├ syscam_autosave.py
├ VRMNXレイアウトファイル.vrmnx
└ VRMNXレイアウトファイル_scas.json（自動作成）
```

対象レイアウトのレイアウトスクリプトに以下の★内容を追記します。  

```py
import vrmapi
import syscam_autosave # ★インポート

def vrmevent(obj,ev,param):
    syscam_autosave.vrmevent(obj,ev,param) # ★メイン処理
    if ev == 'init':
        dummy = 1
    elif ev == 'broadcast':
        dummy = 1
    elif ev == 'timer':
        dummy = 1
    elif ev == 'time':
        dummy = 1
    elif ev == 'after':
        dummy = 1
    elif ev == 'frame':
        dummy = 1
    elif ev == 'keydown':
        dummy = 1
```

ファイル読み込みに成功するとビュワー起動直後にスクリプトログへ下記メッセージが表示されます。

```
import システムカメラ記憶くん Ver.x.x
```

システムカメラの位置・向き・FOV情報を1秒毎に確認し、前回差があればjsonファイルへセーブし、次回ビュワー起動時に前回記録情報をロードします。  
「試運転」の場合、自動記録は動きますが前回情報はロードされません。  
前回値を削除したい場合はレイアウトファイルと同じ場所に作成されたjsonファイルを削除してください。