class CompaniesController < ApplicationController
  # t.string :name
  # t.string :status
  # t.string :market
  # t.string :country
  # t.string :city
  # t.integer :funding_value
  # t.integer :funding_rounds
  # t.string :first_round_date
  # t.string :last_round_date

  def index
    if current_user
      @user_email = current_user.email
      @companies = current_user.companies
    else
      @companies = Company.all
    end
  end

  def new
    @company = Company.new
  end

  def create
    @company = Company.new params[:company]
    @company.user = current_user
    @company.save
    redirect_to action: 'index'
  end
end
