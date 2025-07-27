from datetime import datetime

class ShishaLog:
    def __init__(self, user_id, date, shop_name, main_flavor, sub_flavor, comment):
        self.user_id = user_id
        self.date = date if date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.shop_name = shop_name
        self.main_flavor = main_flavor
        self.sub_flavor = sub_flavor
        self.comment = comment

    def __repr__(self):
        return f"<ShishaLog(user_id={self.user_id}, date={self.date}, shop_name='{self.shop_name}', main_flavor='{self.main_flavor}', sub_flavor='{self.sub_flavor}', comment='{self.comment}')>"