# gevent进程协程池 #

使用场景
--
- 代替不跨服务器、不跨语言的RPC使用, 可以利用多核
- 在gevent程序中执行cpu绑定型函数

注意事项
--
- 子进程会复制主进程的进程空间， 所以要在合适的时候调用PPool实例的init函数
- 仅在*nix运行很好
- 手动调用PPool实例的close_pipes来关闭pipe和循环协程
- 建议尽量使用非阻塞模式(spawn_unblock)

Example
--

	from pglet import PPool
	
    def foo(arg):
        return arg
        
    try:
        ppool = PPool(2)                       # 开启2个子进程
        ppool.init()                           # 初始化

        print ppool.spawn_block(foo, "abc")    # 任务会均匀分配到子进程中庸协程执行(返回结果)
        print ppool.spawn_unblock(foo, "def")  # 不返回结果,打印出None
        
        gevent.wait()                          # 主进程协程等待
    except KeyboardInterrupt:
        ppool.close_pipes()                    # 关闭管道和循环协程