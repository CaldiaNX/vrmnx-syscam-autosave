__title__ = "システムカメラ記憶くん Ver.1.0"
__author__ = "Caldia"
__update__  = "2022/09/11"
__eventUID__ = 1100003

import vrmapi
import os
import json

# ファイル読み込みの確認用
vrmapi.LOG("import " + __title__)

# main
def vrmevent(obj,ev,param):
    if ev == 'init':
        # タイマーイベント登録
        obj.SetEventTimer(1.0, __eventUID__)
        # システムカメラ設定ロード
        loadCamera()
        # 前回値保存
        d = obj.GetDict()
        d['scas_pos'] = vrmapi.SYSTEM().GetGlobalCameraPos()
        d['scas_fov'] = vrmapi.SYSTEM().GetGlobalCameraFOV()
    elif ev == 'timer' and param['eventUID'] == __eventUID__:
        # システムカメラ設定取得
        pos = vrmapi.SYSTEM().GetGlobalCameraPos()
        fov = vrmapi.SYSTEM().GetGlobalCameraFOV()
        # 前回値と異なる
        d = obj.GetDict()
        if d['scas_pos'] != pos or d['scas_fov'] != fov:
            # 設定ファイル保存
            saveCamera(pos, fov)
            # 前回値更新
            d['scas_pos'] = vrmapi.SYSTEM().GetGlobalCameraPos()
            d['scas_fov'] = vrmapi.SYSTEM().GetGlobalCameraFOV()


def saveCamera(pos, fov):
    # ファイルパス有効確認
    path = os.path.splitext(vrmapi.SYSTEM().GetLayoutPath())[0] + '_scas.json'
    if len(path) == 0:
        vrmapi.LOG("ファイル名を定義できません。レイアウトファイルを保存してください。")
        return
    # 保存用Dict
    saveDic = {}
    saveDic['scas_pos'] = pos.copy()
    saveDic['scas_fov'] = fov
    # jsonファイルへ保存
    with open(path, 'w') as f:
        json.dump(saveDic, f, indent=1)
        vrmapi.LOG(path + " へ設定保存")


def loadCamera():
    # ファイルチェック
    path = os.path.splitext(vrmapi.SYSTEM().GetLayoutPath())[0] + '_scas.json'
    if os.path.isfile(path) == False:
        vrmapi.LOG("前回値ファイルがありません。-> " + path)
        return
    vrmapi.LOG(path + " から設定読み込み")
    # jsonファイルを読み込み
    loadDic = {}
    with open(path) as f:
        loadDic = json.load(f)
    if 'scas_pos' in loadDic:
        # 位置・向きを設定
        vrmapi.SYSTEM().SetGlobalCameraPos(loadDic['scas_pos'])
    else:
        vrmapi.LOG("scas_posがありません。")
    if 'scas_fov' in loadDic:
        # FOVを設定
        vrmapi.SYSTEM().SetGlobalCameraFOV(loadDic['scas_fov'])
    else:
        vrmapi.LOG("scas_fovがありません。")
