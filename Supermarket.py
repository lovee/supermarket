#coding:utf-8
#超市
#@author: caohang
#@date: 2017-02-25
#@version: v0.1

from Cashier import Cashier
from Customer import Customer
from Goods import Goods

import threading
import Queue
import time
import random

#所有商品
ALL_GOODS_NAME = ["Apple", "Macbook", "Cookie"]
EACH_GOODS_COUNT = 15

#所有收银员
ALL_CASHIERS = ["A", "B", "C"]

class Supermarket:
    '''
    超市
    '''
    def __init__(self):
        #所有业务线程
        self.all_threades = []
        #所有已消费的消费者;
        self.all_customer = []
        #所有收银员
        self.all_cashiers = []
        #商品仓库
        self.warehouse = {}
        #商品总个数
        self.all_goods_count = 0
        #消费者队列
        self.customer_queue = Queue.Queue()
        #销售开始与结束时间:
        self.sale_begin_time = None
        self.sale_end_time = None
   
    def start(self):
        '''
        启动业务线程
        '''
        #初始化商品
        self.init_goods()
        #记录销售开始时间
        self.sale_begin_time = time.time()
        print(u"商品销售开始时间: %s" % time.asctime(time.localtime(self.sale_begin_time)))
        #初始化消费者线程
        self.init_customer_threads()        
        #初始化收银员线程
        self.all_cashiers = [Cashier(name, self) for name in ALL_CASHIERS]
        for cashier in self.all_cashiers:
            self.init_cashier_threads(cashier)
        #初始销售监控线程
        self.init_sale_goods_monitor_threads()
        for thd in self.all_threades:
            thd.join()

    def init_goods(self):
        '''
        初始化商品
        '''
        for goods in ALL_GOODS_NAME:
            self.warehouse[goods] = Queue.Queue()
            for i in range(EACH_GOODS_COUNT):
                self.all_goods_count += 1
                self.warehouse[goods].put(Goods(goods))

    def init_cashier_threads(self, cashier):
        '''
        初始化收银员线程
        '''
        cash_thd = threading.Thread(target=cashier.process_request, args=(self.customer_queue,))
        cash_thd.start()
        self.all_threades.append(cash_thd)

    def init_customer_threads(self):
        '''
        初始化消费者线程,随机1~3秒产生一个消费者并随机挑选一商品;
        '''
        def _create_customer():            
            while not self.is_sale_end(): 
                #随机等待1~3秒
                sleep_time = random.randint(1,3)
                #sleep_time = 1
                time.sleep(sleep_time)
                cust = Customer()
                if cust.choose_goods(self) == None:                    
                    break
                else:
                    cust.set_status(1)
                #压入消费者队列
                self.customer_queue.put(cust)
        cust_thd = threading.Thread(target=_create_customer)
        cust_thd.start()
        self.all_threades.append(cust_thd)

    def init_sale_goods_monitor_threads(self):
        '''
        初始化商品销售监控线程,用于记录商品销售完成时间;
        '''
        def _sale_goods_monitor():
            while True:
                if self.is_sale_end():
                    self.sale_end_time = time.time()
                    print(u"商品销售结束时间: %s" % time.asctime(time.localtime(self.sale_end_time)))
                    break
                else:
                    #print("all_customer=%d" % self.customer_queue.qsize())
                    time.sleep(1)
        mntr_thd = threading.Thread(target=_sale_goods_monitor)
        mntr_thd.start()
        self.all_threades.append(mntr_thd)

    def get_goods(self, goods_name):
        '''
        获取商品        
        '''
        if not self.warehouse.has_key(goods_name):
            return None
        if self.warehouse[goods_name].empty():
            return None
        goods = self.warehouse[goods_name].get()
        return goods

    def is_sale_end(self):
        '''
        判断是否所有请求和商品处理完成
        '''
        #所有消费者的请求是否处理完;
        # if not self.customer_queue.empty():
        #     return False
        # #所有商品是否售完;
        # for k,v in self.warehouse.items():
        #     if not v.empty():
        #         return False
        # #
        if len(self.all_customer) == EACH_GOODS_COUNT * len(ALL_GOODS_NAME):
            return True
        else:
            return False
    
    def get_goods_list(self):
        '''
        获取商品数量非0的商品名称清单
        '''
        goods_list = []
        for k, v in self.warehouse.items():
            if not v.empty():
                goods_list.append(k)
        return goods_list
        
    def statistical_info(self):
        '''
        统计信息并打印        
        '''
        print(u"\r\n====超市商品销售统计信息====")
        #统计出每个顾客平均等待时间(所有顾客等待时间/顾客总数)
        all_cust_count = len(self.all_customer)
        all_cust_wait_time = 0
        for cust in self.all_customer:
            all_cust_wait_time += cust.wait_time
        print(u"1.每个顾客平均等待时间为:%0.3f秒." % (all_cust_wait_time/all_cust_count,))
        #统计出每个商品平均售出时间(销售总时间/商品个数)
        sale_length = self.sale_end_time - self.sale_begin_time
        print(u"2.每个商品平均售出时间:%0.3f秒." % (sale_length/self.all_goods_count,))        
        #统计出从开始销售到销售完成总共时间
        print(u"3.开始销售到销售完成总共时间:%0.3f秒." % (sale_length,))
        #统计每个收银员接待的顾客数量
        print(u"4.每个收银员接待的顾客数量")
        for c in self.all_cashiers:
            print(u"--收银员\"%s\", 接待顾客数量:%d." % (c.name, c.request_count))

