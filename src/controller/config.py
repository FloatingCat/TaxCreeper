import multiprocessing

redis_config = {
    'host': '39.97.175.209',
    'port': 6379,
    'decode_responses': True,
    'password': 'x74rtw05'
}
processing_config = {
    'core_amount': multiprocessing.cpu_count(),
    'max_alloc': 2,
    'min_alloc': 2
}
