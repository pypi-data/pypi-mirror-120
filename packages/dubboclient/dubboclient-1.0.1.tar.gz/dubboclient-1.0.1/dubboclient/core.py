import json
import telnetlib


class DubboClient:

    def __init__(self, host, port):
        """
        实例化dubbo客户端对象
        :param host: dubbo服务地址
        :param port: dubbo服务端口
        """
        self.telnet = telnetlib.Telnet(host, port)

    def invoke(self, service_name, method_name, *args):
        """
        调用接口
        :param service_name: 服务名称
        :param method_name: 方法名称
        :param args: 方法参数列表
        :return: 接口响应数据
        """
        # 处理参数
        new_args = self._deal_args(args)
        print("new_args==", new_args)

        # 调用接口
        command = "invoke {}.{}({})\n".format(service_name, method_name, new_args)
        print("command==", command)
        self.telnet.write(command.encode())

        # 读取响应数据
        response_data = self.telnet.read_until("dubbo>".encode())
        print("response_data==", response_data)

        # 处理响应数据
        data = self._deal_response_data(response_data)
        return data

    @staticmethod
    def _deal_response_data(response_data):
        """处理响应数据"""
        return response_data.decode().split()[0]

    @staticmethod
    def _deal_args(args):
        """处理参数"""
        args_str = ""
        for arg in args:
            args_str += json.dumps(arg) + ","
        return args_str[:-1]

    def close(self):
        """关闭连接对象"""
        if self.telnet:
            self.telnet.close()
            self.telnet = None

    def __del__(self):
        """销毁对象时，自动关闭连接"""
        self.close()
