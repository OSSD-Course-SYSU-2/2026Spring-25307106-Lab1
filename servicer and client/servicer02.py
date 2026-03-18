import socket
import threading
import time

MENU = { 
    '汉堡': 3,
    '披萨': 2,
    '薯条': 1,
    '可乐': 1
}

def start_tcp_server():
    # 创建socket接口
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定ip地址
    tcp_server.bind(('192.168.1.12', 8080))

    # 设置监听数
    tcp_server.listen(3)
    print('餐厅营业中...')

    try:
        while True:

            # 连接客户端
            conn, addr = tcp_server.accept()

            # 处理客户需求
            threading.Thread(target=tcp_hurdle_server, args=(conn, addr)).start()

    except KeyboardInterrupt:
        print('tcp服务器关闭')
    finally:
        # 释放资源
        tcp_server.close()


def tcp_hurdle_server(conn, addr):

    try:
        print(f'{addr}进店, hello')

        #提供菜单
        menu_text = '====欢迎光临====\n菜单:\n1: 汉堡\n2: 沙拉\n3: 披萨\n4: 可乐'
        conn.send(menu_text.encode('utf-8'))

        # 接收点餐信息
        need = conn.recv(1024).decode('utf-8')
        print(f'{addr}点餐{need}')

        # 处理点餐信息
        food_list = [food.strip() for food in need.split(',')]
        total_time = 0
        for food in food_list:
            if food in MENU:
                total_time += MENU[food]
                food_sleep = MENU[food]
                print(f'制作{food}花费{food_sleep}秒')
                time.sleep(food_sleep)

        # 发送信息
        conn.send(f"您的餐品已制作完成,花费{total_time}秒,请享用".encode('utf-8'))

    except Exception as e:
        print(f'链接错误:{e}')
    finally:
        conn.close()

if __name__ == '__main__':
    start_tcp_server()
