# -*-coding:utf-8 -*-
import os
import time
import sched
from basic.crawler import get

schedule = sched.scheduler(time.time, time.sleep)

def func():
    print("------------------------开始爬取---------------------------")
    get()
    schedule.enter(10, 0, func)
    print("------------------------爬取完成---------------------------")

def main():
    # 第一个参数delay单位是s，第二个数值越小优先级越大
    # 该调度任务只能执行一次
    schedule.enter(10, 0, func)
    schedule.run()

if __name__ == '__main__':
    main()