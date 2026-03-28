class Weather:
    def __init__(
        self,
        rain: bool = False,
        fog: bool = False,
        high_wind: bool = False
    ):
        self.rain = rain
        self.fog = fog
        self.high_wind = high_wind
