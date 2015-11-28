class Company(object):
    def __init__(self, name, status, market, country, funding_value, funding_rounds):
        self._name = name;
        self._status = status;
        self._market = market;
        self._country = country;
        self._funding_value = int(funding_value);
        self._funding_rounds = int(funding_rounds);

    def getName(self):
        return self._name;

    def getStatus(self):
        return self._status;

    def getMarket(self):
        return self._market;

    def getCountry(self):
        return self._country;

    def getFunding_value(self):
        return self._funding_value;

    def getFunding_rounds(self):
        return self._funding_rounds;

