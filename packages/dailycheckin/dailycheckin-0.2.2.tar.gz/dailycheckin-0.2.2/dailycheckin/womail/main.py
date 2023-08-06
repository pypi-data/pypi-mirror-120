# -*- coding: utf-8 -*-
import json
import os
import re
import time

import requests

from dailycheckin import CheckIn


class WoMail(CheckIn):
    name = "沃邮箱"

    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def login(womail_url):
        try:
            url = womail_url
            headers = {
                "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
            }
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
            if "YZKF_SESSION" in cookies:
                return cookies
            else:
                print("沃邮箱获取 cookies 失败")
                return None
        except Exception as e:
            print("沃邮箱错误:", e)
            return None

    @staticmethod
    def dotask(cookies):
        msg = ""
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
            "Cookie": cookies,
        }
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxname = result.get("result").get("wxName")
            usermobile = result.get("result").get("userMobile")
            keep_sign = result['result']['keepSign']

            userdata = f"帐号信息: {wxname} - {usermobile[:3]}****{usermobile[-4:]}\n"
            msg += userdata
        except Exception as e:
            print("沃邮箱获取用户信息失败", e)
            keep_sign = 0
            msg += "沃邮箱获取用户信息失败\n"
        try:
            if keep_sign >= 21:
                msg += f"每日签到: 昨日为打卡{keep_sign}天，今日暂停打卡\n"
            else:
                url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
                res = requests.post(url=url, headers=headers).json()
                result = res.get("result")
                if result == -2:
                    msg += "每日签到: 已签到\n"
                elif result is None:
                    msg += f"每日签到: 签到失败\n"
                else:
                    msg += f"每日签到: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "每日首次登录手机邮箱": {"taskName": "loginmail"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
                "小积分抽大奖": {"taskName": "clubactivity"},
                "每日答题赢奖": {"taskName": "answer"},
                "下载沃邮箱": {"taskName": "download"},
            }
            for key, data in data_params.items():
                try:
                    res = requests.post(url=url, data=data, headers=headers).json()
                    result = res.get("result")
                    if result == 1:
                        msg += f"{key}: 做任务成功\n"
                    elif result == -1:
                        msg += f"{key}: 任务已做过\n"
                    elif result == -2:
                        msg += f"{key}: 请检查登录状态\n"
                    else:
                        msg += f"{key}: 未知错误\n"
                except Exception as e:
                    print(f"沃邮箱执行任务【{key}】错误", e)
                    msg += f"沃邮箱执行任务【{key}】错误"

        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        return msg

    @staticmethod
    def dotask2(womail_url):
        msg = ""
        userdata = re.findall("mobile.*", womail_url)[0]
        url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
        }
        try:
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("SESSION.*?;", set_cookie)[0]
            if "SESSION" in cookies:
                headers = {
                    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
                    "Cookie": cookies,
                    "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task",
                }
                # 获取用户信息
                try:
                    url = "https://club.mail.wo.cn/clubwebservice/club-user/user-info/get-user-score-info/"
                    res = requests.get(url=url, headers=headers)
                    result = res.json()
                    integraltotal = result.get("integralTotal")
                    usermobile = result.get("userPhoneNum")
                    userdata = f"帐号信息: {usermobile[:3]}****{usermobile[-4:]}\n当前积分:{integraltotal}\n"
                    msg += userdata
                    integral_task_data = [
                        {
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create",
                        },
                        {
                            "irid": 539,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "description": "Web端参与俱乐部活动+1积分",
                        },
                        {
                            "irid": 545,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "description": "Web端积分兑换+1积分",
                        },
                    ]
                    lenth = len(integral_task_data)
                    # msg+="--------积分任务--------\n"
                    # 执行积分任务
                    for i in range(lenth):
                        resource_name = integral_task_data[i]["resourceName"]
                        try:
                            if "每日签到" in resource_name:
                                url = integral_task_data[i]["url"]
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuous_day = res["data"]["continuousDay"]
                                    msg += f"{resource_name}: 签到成功~已连续签到{str(continuous_day)}天！\n"
                                else:
                                    msg += f"{resource_name}: {result}\n"
                            else:
                                resource_flag = integral_task_data[i]["resourceFlag"]
                                resource_flag = resource_flag.replace("+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={usermobile}&resourceType={resource_flag}"
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                msg += f"{resource_name}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resource_name}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resource_name}】错误"
                    growthtask_data = [
                        {
                            "resourceName": "每日签到（积分）",
                            "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create",
                        },
                        {
                            "irid": 254,
                            "resourceName": "参与俱乐部活动",
                            "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/club-index/activity-scope?currentPage=activityScope"}',
                            "description": "Web端参与俱乐部活动+1积分",
                        },
                        {
                            "irid": 561,
                            "resourceName": "俱乐部积分兑换",
                            "resourceFlag": "Web_jifenduihuan+2jifen",
                            "taskState": 0,
                            "scoreNum": 1,
                            "scoreResourceType": "add",
                            "attachData": '{"jumpLink":"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover"}',
                            "description": "Web端积分兑换+1积分",
                        },
                    ]
                    lenth = len(growthtask_data)
                    for i in range(lenth):
                        resource_name = growthtask_data[i]["resourceName"]
                        try:
                            if "每日签到" in resource_name:
                                url = growthtask_data[i]["url"]
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuous_day = res["data"]["continuousDay"]
                                    msg += f"{resource_name}: 签到成功~已连续签到{str(continuous_day)}天！\n"
                                else:
                                    msg += f"{resource_name}: {result}\n"
                            else:
                                resource_flag = growthtask_data[i]["resourceFlag"]
                                resource_flag = resource_flag.replace("+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?phoneNum={usermobile}&resourceType={resource_flag}"
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                msg += f"{resource_name}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resource_name}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resource_name}】错误"
                except Exception as e:
                    print("沃邮箱俱乐部获取用户信息失败", e)
                    msg += "沃邮箱俱乐部获取用户信息失败\n"
            else:
                msg += "沃邮箱俱乐部获取SESSION失败\n"
        except Exception as e:
            print("沃邮箱俱乐部获取cookies失败", e)
            msg += "沃邮箱俱乐部获取cookies失败\n"
        return msg

    def dotask3(self, womail_url):
        msg = "【集wo熊拼图】\n"
        try:
            dated = int(time.time())
            end_time = time.mktime(time.strptime("2021-10-9 23:59:59", "%Y-%m-%d %H:%M:%S"))  # 设置活动结束日期
            if dated < end_time:
                # 登录账户
                userdata = re.findall("mobile.*", womail_url)[0]
                s = requests.session()
                s.headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
                }
                # 做任务
                url = f"https://nyan.mail.wo.cn/cn/puzzle2/index/index?{userdata}"
                res = s.get(url)
                task_list = ["checkin", "viewclub", "loginmail"]
                for taskName in task_list:
                    url = f"https://nyan.mail.wo.cn/cn/puzzle2/user/doTask.do?taskName={taskName}"
                    res = s.get(url).json()
                    if res["success"] and res["result"] == 1:
                        msg += f"{taskName}：做任务成功\n"
                    elif res["success"] and res["result"] == -1:
                        msg += f"{taskName}：任务已完成\n"
                    else:
                        msg += f"{taskName}：做任务失败\n"
                    time.sleep(2)
                # 获取拼图个数
                timestamp = int(round(time.time() * 1000))
                url = f"https://nyan.mail.wo.cn/cn/puzzle2/index/userinfo.do?time={timestamp}"
                res = s.post(url).json()
                if res["success"]:
                    puzzle = res["result"]["puzzle"]
                    if puzzle == 6:
                        # 抽奖
                        url = "https://nyan.mail.wo.cn/cn/puzzle2/draw/draw"
                        res = s.get(url).json()
                        if res["success"]:
                            prizeTitle = res["result"]["prizeTitle"]
                            msg += f"抽奖结果：{prizeTitle}\n"
                        else:
                            msg += f'抽奖结果：{res["msg"]}\n'
                    else:
                        msg += f"抽奖结果：当前拼图{puzzle}块，未集齐\n"
                else:
                    msg += f"获取拼图个数失败\n"
                return msg
            else:
                msg += "活动已结束，不再执行\n"
        except Exception as e:
            msg += f"执行错误，原因：{e}\n"

    def main(self):
        url = self.check_item.get("url")
        try:
            cookies = self.login(womail_url=url)
            if cookies:
                msg = self.dotask(cookies=cookies)
                msg1 = self.dotask2(womail_url=url)
                msg2 = self.dotask3(womail_url=url)
                msg += f"\n【沃邮箱俱乐部】\n{msg1}\n{msg2}"
            else:
                msg = "登录失败"
        except Exception as e:
            print(e)
            msg = "登录失败"
        return msg


if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r", encoding="utf-8"
    ) as f:
        datas = json.loads(f.read())
    _check_item = datas.get("WOMAIL", [])[0]
    print(WoMail(check_item=_check_item).main())
