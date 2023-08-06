
djtest框架是一个接口自动化框架


框架模块:
    命令行模块
    http模块
    tests模块
    
    
v0.0.1
    1. call_api(method, url, type)



allure报告中json, 默认全部显示, 也可以指定需要显示的部分

URL的参数来自于ini文件
    api_protocol
    api_domain
    api_login_u
    api_login_p
    
todo:
    请求类型为文件的情况
    登录凭证(auth,cookie)
    请求前钩子: 实现签名功能(sign_logic_func, sign_save_loc), 支持发送同时进行异步任务(after_request_method)
        # 如果after_request_method有值,则开启一个子线程任务
        import threading
        t = threading.Thread(target=after_request_method)
        t.setDaemon(True)
        t.start()
    verify
    划分: 异常与断言
    
   日志:
        默认情况 verbose=False, 不打印info日志
        当verbose=True, 默认打印全部日志
            headers和type二选一, type为headers中的一个代表

   生成项目结构后, 解决登录问题
        从指定的配置文件中读取配置信息
            is_login
            cfg_title_path
            login_headers_cfgkey
        is_allure
        is_headers_convert
        after_request_method

    
    # print(res.capture_info)
    # res.extract()
    # res.parse()
    # res.assert_http_code()
    # res.assert_bns_code()






















