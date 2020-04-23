import arrow
from faker import Faker

fake = Faker("zh_CN")


class Constant:
    # 接口用例中用到的时间格式
    # 当前分钟
    @staticmethod
    def current_minute():
        return arrow.now().format('YYYY-MM-DD HH:mm')

    # 下一小时
    @staticmethod
    def next_hour():
        return arrow.now().shift(hours=1).format('YYYY-MM-DD HH:mm')

    # 当天
    @staticmethod
    def today():
        return arrow.now().format('YYYY-MM-DD')

    # 明天
    @staticmethod
    def tomorrow():
        return arrow.now().shift(days=1).format('YYYY-MM-DD')

    # 当月 当月开始的第一天 2019-08-01
    @staticmethod
    def month():
        return arrow.now('local').floor('month').format('YYYY-MM-DD')

    # Unix时间戳
    @staticmethod
    def unix_format_now():
        return arrow.now().timestamp

    @staticmethod
    # 当天0点的时间戳
    def unix_today():
        t = arrow.now().shift().format('YYYY-MM-DD')
        return arrow.get(t, tzinfo=arrow.now().tzinfo).timestamp

    # 前一天的时间戳 跟进记录不允许创建当前时间之后的
    @staticmethod
    def unix_format_yesterday():
        return arrow.now().shift(days=-1).timestamp

    # 明天0点的时间戳
    @staticmethod
    def unix_format_tomorrow():
        t = arrow.now().shift(days=1).format('YYYY-MM-DD')
        return arrow.get(t, tzinfo=arrow.now().tzinfo).timestamp

    # 人名
    @staticmethod
    def people_name():
        return fake.name()

    # 手机号
    @staticmethod
    def phone():
        return fake.phone_number()

    # 颜色
    @staticmethod
    def color():
        return fake.color_name()

    # 三位随机数
    @staticmethod
    def numerify():
        return fake.numerify()
