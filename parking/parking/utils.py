import pprint
import re


class DotDict(object):
    """
    Creates objects that behave much like a dictionaries, but allow nested
    key access using object '.' (dot) lookups.
    """
    def __init__(self, d):
        for k in d:
            if isinstance(d[k], dict):
                self.__dict__[k] = DotDict(d[k])
            elif isinstance(d[k], (list, tuple)):
                l = []
                for v in d[k]:
                    if isinstance(v, dict):
                        l.append(DotDict(v))
                    else:
                        l.append(v)
                self.__dict__[k] = l
            else:
                self.__dict__[k] = d[k]

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__.get(name, None)
        return None

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__.get(name, None)
        return None

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __repr__(self):
        return pprint.pformat(self.__dict__)


class Utils:
    @staticmethod
    def engishize(text):
        if not text:
            return None
        text = text.lower()
        src = '۱۲۳۴۵۶۷۸۹۰كايآ٠١٢٣٤٥٦٧٨٩'
        trg = '1234567890کایا0123456789'
        repl = str.maketrans(src, trg)
        text = text.translate(repl)
        text = text.strip()
        return text

    @staticmethod
    def convert_to_persian_number(number):
        '''
    تبدیل عدد انگلیسی به فارسی
        :param number:
        :return:
        '''
        num_dic = {'0': '۰'
            , '4': '۴'
            , '8': '۸'
            , '3': '۳'
            , '9': '۹'
            , '6': '۶'
            , '2': '۲'
            , '1': '۱'
            , '7': '۷'
            , '5': '۵'
                   }
        return num_dic.get(number)

    @staticmethod
    def num_to_persian(numbers, with_sign=False):
        '''
    اعداد از انگلیسی به فارسی تبدیل می‌کند
        :return:
        '''
        persian_nums = ''
        numbers = str(numbers)
        for num in numbers:
            if num.isdigit():
                persian_nums += Utils.convert_to_persian_number(num)
            else:
                persian_nums += num
        negative_sign_idx = persian_nums.find('-')
        if negative_sign_idx >= 0:
            persian_nums = '%s%s' % (persian_nums[negative_sign_idx + 1:], '-' if with_sign else '')
        return persian_nums

    @staticmethod
    def convert_to_english_number(number):
        '''
    تبدیل عدد فارسی به انگلیسی
        :param number:
        :return:
        '''
        num_dic = {
                '۰': '0'
                ,  '۴': '4'
                , '۸': '8'
                ,  '۳': '3'
                ,  '۹': '9'
                ,  '۶': '6'
                ,  '۲': '2'
                ,  '۱': '1'
                ,  '۷': '7'
                ,  '۵': '5'
                }
        return num_dic.get(number)

    @staticmethod
    def num_to_eng(nums, just_numbers=False):
        eng_nums = ''
        nums = str(nums)
        for num in nums:
            if num in ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']:
                eng_nums += Utils.convert_to_english_number(num)
            else:
                eng_nums += num
        negative_sign_idx = eng_nums.find('-')
        if negative_sign_idx >= 0:
            eng_nums = '%s%s' % (eng_nums[negative_sign_idx+1:], '-')
        return eng_nums if not just_numbers else re.sub('[^0-9]', '', eng_nums)
