# gevent进程协程池 #

使用场景
--
- 代替不跨服务器、不跨语言的RPC使用, 可以利用多核
- 在gevent程序中执行cpu绑定型函数, 不会阻塞主进程的协程

注意事项
--
- 仅在*nix系统运行很好
- 子进程会复制主进程的进程空间， 所以要在合适的时候调用`PPool`实例的`init`函数
- 必须手动调用`PPool`实例的`close`函数来关闭pipe、子进程和循环协程
- 如果使用`spawn`,请必须调用 `返回值.get`,否则请使用 `spawn_sub`


使用
--
- `spawn`: 返回`future`对象,函数必须是复制到子进程的,参数和返回值必须能够pickle序列化
- `spawn_sub`: 不返回值,函数必须是复制到子进程的,参数必须能够pickle序列化


benchmark:
--
因为没有实现join方法,所以测试数据是debug时期内嵌在源码中,然后被删除了

    1w个本地http get(urllib2)
    普通协程:     8.83s
    pglet 2核:   4.21s
    pglet 3核:   3.95s


Example
--
    # -*- coding: utf-8 -*-
	from pglet import PPool
	import gevent
	
    def foo(arg):
        return arg
        
    try:
        ppool = PPool(2)                       # 开启2个子进程,可放在启动文件开始出
        ppool.init()                           # 初始化,开启n个子进程,要在合适的时机调用

        print ppool.spawn(foo, "abc").get()    # 任务会均匀分配到子进程中用协程执行(返回future,future.get回去结果)
        print ppool.spawn_sub(foo, "def")      # 不返回结果,在子进程的子协程中执行(打印出None)
        
        gevent.wait()                          # 主进程协程等待
    except KeyboardInterrupt:
        ppool.close()                    # 关闭管道和循环协程