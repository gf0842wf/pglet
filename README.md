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

Example
--

	from pglet import PPool
	
    def foo(arg):
        return arg
        
    try:
        ppool = PPool(2)
        ppool.init()

        print ppool.spawn_block(foo, "abc")
        print ppool.spawn_unblock(foo, "def")
        
        gevent.wait()
    except KeyboardInterrupt:
        ppool.close_pipes()