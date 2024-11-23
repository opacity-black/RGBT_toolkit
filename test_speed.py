from functools import reduce
import time
from multiprocessing.pool import Pool, ThreadPool
import joblib
import os
import numpy as np

"""
测试在需要处理返回结果情况下各种循环方式的执行效率
"""

def fun(li):
    li = np.array(li)+1
    return li.tolist()
    # return list(map(lambda x:x+1, li))
    # for i in range(len(li)):
    #     li[i]+=1

def blockfun(bli):
    return list(map(lambda x:list(map(lambda y:y+1, x)), bli))

if __name__=="__main__":

    count1 = 250
    count2 = 1000000
    print(f"{count1=}, {count2=}")
    a_li = [[0]*count2 for _ in range(count1)]

    # # for 循环
    # st = time.time()
    # for i in range(count1):
    #     for j in range(count2):
    #         a_li[i][j] += 1
    # print("for-time = ", time.time()-st)
            
    # # 列表解析
    # st = time.time()
    # a_li = [[a_li[i][j]+1 for j in range(count2)] for i in range(count1)]
    # print("loop-time = ", time.time()-st)


    # # map
    # st = time.time()
    # a_li = list(map(lambda x:list(map(lambda y:y+1, x)), a_li))
    # print("map-time = ", time.time()-st)


    # # 线程池 python并非真正的线程
    # # print(a_li[0][0])
    # # print(os.cpu_count())
    # st = time.time()
    # pool = ThreadPool(processes=None)
    # a_li = pool.map(fun, a_li)
    # pool.close()
    # pool.join()
    # print("tpool.map-time = ", time.time()-st)
    # # print(a_li[0][0])
    

    # 进程池
    # print(a_li[0][0])
    st = time.time()
    pool = Pool(processes=None)
    a_li = pool.map(fun, a_li)
    pool.close()
    pool.join()
    print("pool.map-time = ", time.time()-st)
    # print(a_li[0][0])
    

    # 进程加速
    st = time.time()
    pool = Pool(processes=None)
    cpu_count = os.cpu_count()
    block_num = len(a_li)//cpu_count                                        # type:ignore
    a_li = [a_li[i*block_num:(i+1)*block_num] for i in range(cpu_count)]        # type:ignore
    a_li = reduce(lambda a,b:a+b, pool.map(blockfun, a_li))
    pool.close()
    pool.join()
    print("blockpool.map-time = ", time.time()-st)

    
    # joblib
    # print(a_li[0][0])
    # print(os.cpu_count())
    st = time.time()
    a_li = joblib.Parallel(n_jobs=6)(joblib.delayed(fun)(li) for li in a_li)
    print("joblib-time = ", time.time()-st)
    # print(a_li[0][0])

"""
count1=250, count2=10000
for-time =  0.5123095512390137
loop-time =  0.30763721466064453
map-time =  0.26610469818115234
tpool.map-time =  0.2739686965942383
pool.map-time =  2.6028294563293457


count1=250, count2=100000
for-time =  4.795907020568848
loop-time =  3.071892023086548
map-time =  2.4250857830047607
tpool.map-time =  2.4609687328338623
pool.map-time =  3.992044448852539


count1=250, count2=1000000
for-time =  46.06924843788147
loop-time =  31.546589374542236
map-time =  26.868499755859375
tpool.map-time =  28.255198001861572
pool.map-time =  21.08586835861206


count1=250, count2=10000
pool.map-time =  2.9401659965515137
blockpool.map-time =  2.6042726039886475

count1=250, count2=100000
pool.map-time =  4.544187545776367
blockpool.map-time =  3.7374913692474365

count1=250, count2=1000000
pool.map-time =  21.84156084060669
blockpool.map-time =  20.47252368927002
"""