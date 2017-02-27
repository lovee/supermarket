#coding:utf-8
#超市收银员
#@author: caohang
#@date: 2017-02-25
#@version: v0.1
import Queue
import random
import time

class Cashier:
    '''
    收银员
    '''
    def __init__(self, name, super_market):
        self.name = name
        self.super_market = super_market
        #消费者请求数
        self.request_count = 0

    def process_request(self, customer_queue):
        '''
        处理消费者购买请求,并随机等待5~10秒;
        '''
        while not self.super_market.is_sale_end():
            try:
                cust = customer_queue.get_nowait()
            except Queue.Empty:
                #time.sleep(0.01)
                continue
            #随机等待5~10秒;
            sleep_time = random.randint(5, 10)
            #sleep_time = 3
            time.sleep(sleep_time)
            #设置消费状态
            cust.set_status(2)
            #缓存已处理过的消费者;
            self.super_market.all_customer.append(cust)
            #累计消费者请求数;
            self.request_count += 1