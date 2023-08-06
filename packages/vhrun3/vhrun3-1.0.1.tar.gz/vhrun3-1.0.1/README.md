    基于httprunner==3.1.6版本，根据特定需求二次定制开发
    
    1、保留2.x版本的用例分层机制，避免冗余出现api基本信息（url、headers、method等）
    2、除支持http和https协议外，支持SSH协议，可以远程执行shell命令、文件上传和下载
    3、兼容支持2.x测试报告，便于测试时调试
    4、数据驱动改成一个Class N个test_*用例方式，便于用例扫描
    5、支持test_xx的__doc__自动生成，并支持config.variables和parameters变量解析
    6、yml中config中usefixtures字段，支持pytest指定添加fixture

    参考：
    homepage = "https://github.com/httprunner/httprunner"
    repository = "https://github.com/httprunner/httprunner"
    documentation = "https://docs.httprunner.org"
    blog = "https://debugtalk.com/