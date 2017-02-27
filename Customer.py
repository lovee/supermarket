#coding:utf-8
#超市消费者
#@author: caohang
#@date: 2017-02-25
#@version: v0.1
import time
import random

class Customer:
    '''
    消费者
    '''
    def __init__(self):
        #选购的商品
        self.goods = None
        #消费者状态, 0:未挑选商品,1:经挑选商品,未结账,2:已经结账
        self.status = 0
        #开始消费时间        
        self.begin_time = None
        #消费等待时长
        self.wait_time = 0
    
    def choose_goods(self, super_market):
        '''
        消费者随机挑选商品
        '''
        while not super_market.is_sale_end():
            goods_list = super_market.get_goods_list()
            if len(goods_list) == 0:
                return None
            goods_name = goods_list[random.randint(0, len(goods_list)-1)]
            goods = super_market.get_goods(goods_name)
            if goods == None:
                continue
            else:
                self.goods=goods
                #消费者开始等待时间
                self.begin_time = time.time()
                return goods
    
    def set_status(self, status):
        '''
        设置消费者状态,并计算消费等待时间
        '''
        if status == 2:
            #消费完成,及消费等待时长
            self.wait_time = time.time() - self.begin_time
            print(u"%s 顾客购买商品[%s], 本次消费等待时长:%0.3f秒." % (time.asctime(), self.goods.name.center(10), self.wait_time))
        self.status = status