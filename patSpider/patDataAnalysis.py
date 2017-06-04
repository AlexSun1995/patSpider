import json
import matplotlib.pyplot as plt
import pickle

def total_submit_data(items):
    '''
    :param items: all the data of pat type:list of dic
    :return: (cnt_submit, cnt_pass)
    '''
    cnt_submit = 0
    cnt_pass = 0
    for item in items:
        cnt_submit += int(item['submit_times'])
        cnt_pass += int(item['pass_times'])
    print 'total submit times: %d, total pass times: %d' %(cnt_submit, cnt_pass)
    print 'rate: %f' %(cnt_pass * 1.0/ cnt_submit)
    return cnt_submit,cnt_pass

def top_k_hard(items, k):
    '''
    :param items: all the data of pat, type: list of dic
    :param k: self defined number, ex: if k = 10, the function will return
    information of top 10 most hard problems
    :return: list(dic)
    '''
    size = len(items)
    if k > size:
        k = size
        print 'since k is too large, now we smaller k to:', k
    new_items = sorted(items, key=lambda x:float(x['pass_rate']))
    # print new_items[0:k]
    return new_items[0:k]

def self_practice_data(items):
    '''
    user: suncun(myself)
    pass_word: ***********
    this function aim to show, number of problems I've passed,
    # of problems tried but not passed yet,# of problems never tried
    :param items: all the data of pat, type: list of dic
    :return:
    '''
    print items
    cnt_pass = 0
    cnt_not_try = 0
    cnt_not_pass = 0
    total_problems = len(items)
    for item in items:
        situation = item['does_pass']
        if situation == 'Not submit':
            cnt_not_try += 1
        elif situation == 'Y':
            cnt_pass += 1
        else:
            cnt_not_pass += 1
    print 'there a totally %d problems, and I\'ve passed %d problems' %(total_problems, cnt_pass)
    print 'tried but not passed %d problems, still %d problems not tried yet' %(cnt_not_pass, cnt_not_try)


if __name__ == '__main__':
    items = {}
    with open('../items_list', 'r') as f:
        items = pickle.load(f)
    # total_submit_data(items)
    # print top_k_hard(items, 10)
    self_practice_data(items)