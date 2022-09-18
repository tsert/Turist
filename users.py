from datetime import datetime


class User:
    """
    Пользовательский класс
    """
    user_data = {}

    def __init__(self, user_id):
        self.user_id = user_id
        self.current_command = None
        self.city = None
        self.city_id = None
        self.hotels_num = None
        self.photos_num = None
        self.sort = 'PRICE'
        self.check_in = datetime
        self.check_out = datetime
        self.price_min = None
        self.price_max = None
        self.min_distance_from_center = None
        self.max_distance_from_center = None
        self.total_hotels = None
        self.hotels = None
        self.photos = None
        self.results = ''
