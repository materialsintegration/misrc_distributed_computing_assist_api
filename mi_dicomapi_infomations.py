#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群用の情報保持クラス
'''

import uuid

# 情報格納場所
class CalcInfomation(object):
    '''
    保持する情報
    '''

    def __init__(self):
        '''
        初期化
        '''

        self.accept_id = None
        self.accept_id = str(uuid.uuid4())

    def is_accept_id(self, accept_id):
        '''
        この受付番号か？
        '''

        if self.accept_id is None:
            return False

        if self.accept_id == accept_id:
            return True
        
        return False

