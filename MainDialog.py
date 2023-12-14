import json
import os
import sys
from time import sleep

import requests as requests
from PyQt5.QtWidgets import QApplication, QDialog

import weather


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.ui = weather.Ui_Dialog()
        self.ui.setupUi(self)

    def searchWeather(self):
        citiName = self.ui.comboBox.currentText()
        citiCode = self.search_code_by_name(citiName)
        self.ui.textEdit.setText("正在查询[{}]，请稍后...".format(citiName))

        sleep(3)

        uri = "http://t.weather.sojson.com/api/weather/city/{}".format(citiCode)

        resp = requests.get(uri)
        if resp.status_code != 200:
            self.ui.textEdit.setText("无法连接网络,查询失败")
            return
        resp_json = resp.json()
        if resp_json.get("status") != 200:
            self.ui.textEdit.setText("查询失败：{}".format(resp_json.get("message")))
            return
        # 格式化展示天气信息
        # weatherMsg = '城市：{}\n日期：{}\n天气：{}\nPM 2.5：{} {}\n温度：{}\n湿度：{}\n风力：{}\n\n{}'.format(
        #     resp_json['cityInfo']['city'],
        #     resp_json['data']['forecast'][0]['ymd'],
        #     resp_json['data']['forecast'][0]['type'],
        #     int(resp_json['data']['pm25']),
        #     resp_json['data']['quality'],
        #     resp_json['data']['wendu'],
        #     resp_json['data']['shidu'],
        #     resp_json['data']['forecast'][0]['fl'],
        #     resp_json['data']['forecast'][0]['notice'],
        # )
        # self.ui.textEdit.setText(weatherMsg)
        # 美化展示json
        self.ui.textEdit.setText(json.dumps(resp_json, indent=4, ensure_ascii=False))

    def refresh(self):
        self.ui.textEdit.setText("查一查天气怎么样？")
        self.ui.comboBox.setCurrentIndex(0)

    def search_code_by_name(self, name):
        if os.path.exists("weather.json"):
            with open("weather.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for city in data:
                    if city["name"] == name:
                        return city["code"]
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainDialog = MainDialog()
    mainDialog.show()
    sys.exit(app.exec_())
