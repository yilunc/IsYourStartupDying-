class Company(object):
    def __init__(self, name, status, market, country, city, founded, \
    relationships, invest_rounds, first_invest, last_invest, \
    funding_rounds, funding_total, first_funding, last_funding):

        if relationships is None:
            relationships = 0;
        if funding_total is None:
            funding_total = 0;

        self._name = name;
        self._status = status;
        self._market = market;
        self._country = country;
        self._city = city;
        self._founded = founded;
        self._relationships = relationships;
        self._invest_rounds = invest_rounds;
        self._first_invest = first_invest;
        self._last_invest = last_invest;
        self._funding_rounds = funding_rounds;
        self._funding_total = float(funding_total);
        self._first_funding = first_funding;
        self._last_funding = last_funding;
        self._successful = None

    @property
    def name(self):
        return self._name;

    @property
    def status(self):
        return self._status;

    @property
    def market(self):
        return self._market;

    @property
    def country(self):
        return self._country;

    @property
    def city(self):
        return self._city;

    @property
    def founded(self):
        return self._founded;

    @property
    def relationships(self):
        return self._relationships;

    @property
    def invest_rounds(self):
        return self._invest_rounds;

    @property
    def first_invest(self):
        return self._first_invest;

    @property
    def last_invest(self):
        return self._last_invest;

    @property
    def funding_rounds(self):
        return self._funding_rounds;

    @property
    def funding_total(self):
        return self._funding_total;

    @property
    def first_funding(self):
        return self._first_funding;

    @property
    def last_funding(self):
        return self._last_funding

    @property
    def successful(self):
        return self._successful

    @successful.setter
    def successful(self, result):
        if(type(result) == type(True)):
            self._successful = result

    def get_numerical_points(self):
        return (self.founded, self.relationships, self.invest_rounds, \
        self.first_invest, self.last_invest, self.funding_rounds, \
        self.funding_total, self.first_funding, self.last_funding)
