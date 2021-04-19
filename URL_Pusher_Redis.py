from src.controller.url_pusher import url_put
if __name__=='__main__':
    print('put in amount [602] [962]')
    index_1,index_2=map(int,input().split(' '))
    url_put(index_1,index_2)