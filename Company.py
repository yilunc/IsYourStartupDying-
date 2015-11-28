class Company(object):
    def __init__(self, name, status, market, country, city, funding_value, funding_rounds, funding_per_date):
        self._name = name;
        self._status = status;
        self._market = market;
        self._country = country;
        self._city = city;
        self._funding_value = int(funding_value);
        self._funding_rounds = int(funding_rounds);
        self._funding_per_date = int(funding_per_date)

    def getName(self):
        return self._name;

    def getStatus(self):
        return self._status;

    def getMarket(self):
        return self._market;

    def getCountry(self):
        return self._country;

    def getCity(self):
        return self._city;

    def getFunding_value(self):
        return self._funding_value;

    def getFunding_rounds(self):
        return self._funding_rounds;

    def getFunding_per_date(self):
        return self._funding_per_date;

