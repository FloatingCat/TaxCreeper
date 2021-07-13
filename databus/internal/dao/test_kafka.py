from databus.internal.dao.kafka_producer import KafkaProducerIns


def test_producer():
    ts = KafkaProducerIns()
    su_list = []
    # 发送三条消息
    for i in range(1, 3):
        print(i)
        res = ts.send('kafka_demo', 'count_num', str(i), 0)
        su_list.append(res)

    print(su_list)

