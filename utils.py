# -*- coding: utf-8 -*-
import multiprocessing
import threading

def divide_list(lis, part):
    '''
    将列表分成part份，返回嵌套的列表
    '''
    num = int( len(lis)/part )
    out = [ lis[ i*num:(i+1)*num] for i in range(part-1) ]
    out.append( lis[ (part-1)*num: ])
    return out

def multiprocess(lis0, num, func):
    print('开始main_multiproces…')
    lis = divide_list(lis0, num)
    pool = multiprocessing.Pool(processes = num)
    for i in range(num):
        pool.apply_async(func=func, args=(lis[i], ))
#        pool.apply_async(func=func, args=(lis[i], ))
    pool.close()
    pool.join()
    pool.terminate()


def multithread(lis0, num, func):
    print('开始multithread…')
    lis = divide_list(lis0, num)
    threads = []
    for i in range(num):
        threads.append(threading.Thread(target=func, args=(lis[i], )))
    for t in threads:
        t.start()
#        t.join()


def multiprocess_with_return(lis0, num, func):
    print('开始multiprocess_with_return。进程数',num)
    out = []
    tem = []
    lis = divide_list(lis0, num)
    pool = multiprocessing.Pool(processes = num)
#    pool.map(tt, lis)
    for i in range(num):
        tem.append( pool.apply_async(func=func, args=(lis[i], )) )
#        out.extend()
    pool.close()
    pool.join()
    pool.terminate()
    for tem_item in tem:
        out.append(tem_item.get())
    return out

class myThread(threading.Thread):#用class 可以收集返回结果
    def __init__(self,func,args=()):
        super(myThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def multithread_with_return(lis0, num, func):
    print('开始multithread_with_return。线程数', num)
    out =[]
    threads = []
    lis = divide_list(lis0, num)
    for i in range(num):
        tem = myThread(func=func, args=(lis[i],))
        threads.append( tem)
#        tem.start()
    for t in threads:
        t.start()
        t.join()
        out.extend(t.get_result())

    return out