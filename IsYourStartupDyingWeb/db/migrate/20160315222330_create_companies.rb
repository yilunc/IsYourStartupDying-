class CreateCompanies < ActiveRecord::Migration
  def change
    create_table :companies do |t|
      t.string :name
      t.string :status
      t.string :market
      t.string :country
      t.string :city
      t.integer :funding_value
      t.integer :funding_rounds
      t.string :first_round_date
      t.string :last_round_date
      t.integer :class
      t.references :user

      t.timestamps null: false
    end
  end
end
