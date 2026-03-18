import socket
import time
import threading
def tcp_connect(menu):
    # 创建socket接口
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 链接服务器
        tcp_client.connect(('192.168.1.12', 8080))
        # 获取菜单
        menu_text = tcp_client.recv(1024)
        print(menu_text.decode('utf-8'))
        # 点餐
        print('=====不同菜品编号请用","分开, 重复点餐就再输入一遍对应编号=====')
        choose = input('请输入菜品编号: ').strip().split(',')
        # 转换为菜品名称
        num_lst = [int(x) for x in choose]
        lst = [menu[num] for num in num_lst]
        print(f"\n您点了:{','.join(lst)}")
        print('厨师开始制作...')
        # 发送点餐信息
        tcp_client.send(','.join(lst).encode('utf-8'))
        # 获取完成讯息
        ok = tcp_client.recv(1024).decode("utf-8")
        print(ok)
    except ConnectionRefusedError:
        print(f'请求失败')
    finally:
        tcp_client.close()
if __name__ == '__main__':
    menu = {1:'汉堡', 2:'披萨', 3:'薯条', 4:'可乐'}
    tcp_connect(menu)