__title__ = "カメラオートセーブくん Ver.1.0"
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
        # フレームイベント登録
        obj.SetEventFrame()
        # 毎秒カウント
        obj.SetEventTimer(1.0, __eventUID__)
        # ロード
        loadCamera()
        # 前回値
        d = obj.GetDict()
        d['scas_pos'] = vrmapi.SYSTEM().GetGlobalCameraPos()
        d['scas_fov'] = vrmapi.SYSTEM().GetGlobalCameraFOV()
    elif ev == 'timer':
        global __eventUID__
        if param['eventUID'] == __eventUID__:
            # システムカメラ設定を取得
            pos = vrmapi.SYSTEM().GetGlobalCameraPos()
            fov = vrmapi.SYSTEM().GetGlobalCameraFOV()
            # 前回値
            d = obj.GetDict()
            # 前回値と異なる
            if d['scas_pos'] != pos or d['scas_fov'] != fov:
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
    # レイアウト名のjsonファイルへ保存
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
    # レイアウト名のjsonファイルを読み込み
    loadDic = {}
    with open(path) as f:
        loadDic = json.load(f)

    if 'scas_pos' in loadDic:
        vrmapi.SYSTEM().SetGlobalCameraPos(loadDic['scas_pos'])
    else:
        vrmapi.LOG("scas_posがありません。")

    if 'scas_fov' in loadDic:
        vrmapi.SYSTEM().SetGlobalCameraFOV(loadDic['scas_fov'])
    else:
        vrmapi.LOG("scas_fovがありません。")
