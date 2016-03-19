class Company < ActiveRecord::Base
  # t.string :name
  # t.string :status
  # t.string :market
  # t.string :country
  # t.string :city
  # t.integer :funding_value
  # t.integer :funding_rounds
  # t.string :first_round_date
  # t.string :last_round_date

  belongs_to :user
  validates :market, presence: true
  validates :country, presence: true
  validates :city, presence: true
  validates :funding_value, presence: true
  validates :funding_rounds, presence: true
  validates :first_round_date, presence: true
  validates :last_round_date, presence: true

  def classify
    self.classify_result = `cd ..; python classify_startup.py \'#{self.name}\' \'#{self.status}\' \'#{self.market}\' \'#{self.country}\' \'#{self.city}\' #{self.funding_value} #{self.funding_rounds} #{self.first_round_date} #{self.last_round_date}`
  end
end
