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

  def classify
    self.class = `cd ..; python classify_startup.py \'#{self.name}\' \'#{self.status}\' \'#{self.market}\' \'#{self.country}\' \'#{self.city}\' #{self.funding_value} #{self.funding_rounds} #{self.first_round_date} #{self.last_round_date}`
  end
end
