# gevent进程协程池 #

使用场景
--
- 代替不跨服务器、不跨语言的RPC使用, 可以利用多核
- 在gevent程序中执行cpu绑定型函数而不会阻塞主进程的协程

注意事项
--
- 仅在*nix运行很好
- 子进程会复制主进程的进程空间， 所以要在合适的时候调用PPool实例的init函数
- 必须手动调用PPool实例的close_pipes函数来关闭pipe和循环协程
- spawn_block是阻塞等待结果,参数和返回值必须能够pickle序列化,建议在场景1中使用
- spawn_unblock是非阻塞模式,参数必须能够pickle序列化,不能获取函数返回值

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

        print ppool.spawn_block(foo, "abc")    # 任务会均匀分配到子进程中用协程执行(返回结果)
        print ppool.spawn_unblock(foo, "def")  # 不返回结果,在子进程的子协程中执行(打印出None)
        
        gevent.wait()                          # 主进程协程等待
    except KeyboardInterrupt:
        ppool.close_pipes()                    # 关闭管道和循环协程