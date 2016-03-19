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
    @company = Company.new convert_company_params
    @company.user = current_user
    @company.classify()
    @company.save
    redirect_to action: 'index'
  end

  private

# "name"=>"",
#  "status"=>"",
#  "market"=>"",
#  "country"=>"",
#  "city"=>"",
#  "funding_value"=>"",
#  "funding_rounds"=>"",
#  "first_round_date(1i)"=>"2016",
#  "first_round_date(2i)"=>"3",
#  "first_round_date(3i)"=>"19",
#  "last_round_date(1i)"=>"2016",
#  "last_round_date(2i)"=>"3",
#  "last_round_date(3i)"=>"19"
  def convert_company_params
    company_params = params[:company]

    if company_params[:name] == nil
      company_params[:name] = ""
    end

    {
      :name => company_params[:name],
      :status => company_params[:status],
      :market => company_params[:market],
      :country => company_params[:country],
      :city => company_params[:city],
      :funding_value => company_params[:funding_value],
      :funding_rounds => company_params[:funding_rounds],
      :first_round_date => "#{company_params["first_round_date(1i)"]}-#{company_params["first_round_date(2i)"]}-#{company_params["first_round_date(3i)"]}",
      :last_round_date => "#{company_params["last_round_date(1i)"]}-#{company_params["last_round_date(2i)"]}-#{company_params["last_round_date(3i)"]}"
    }
  end
end
