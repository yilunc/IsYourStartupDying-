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

  def home
  end

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
    if @company.valid?
      @company.user = current_user
      @company.classify
      @company.save
      redirect_to action: 'index'
    else
      ##TODO flash error
      redirect_to :back
    end
  end

  def show
    @company = Company.find(params[:id])
  end

  private

  def convert_company_params
    company_params = params[:company]

    if company_params[:name] == nil
      company_params[:name] = ""
    end

    if company_params["first_round_date(2i)"].to_i < 10
      first_round_month = "0#{company_params["first_round_date(2i)"]}"
    else
      first_round_month = company_params["first_round_date(2i)"]
    end
    if company_params["first_round_date(3i)"].to_i < 10
      first_round_day = "0#{company_params["first_round_date(3i)"]}"
    else
      first_round_day = company_params["first_round_date(3i)"]
    end
    if company_params["last_round_date(2i)"].to_i < 10
      last_round_month = "0#{company_params["last_round_date(2i)"]}"
    else
      last_round_month = company_params["last_round_date(2i)"]
    end
    if company_params["last_round_date(3i)"].to_i < 10
      last_round_day = "0#{company_params["last_round_date(3i)"]}"
    else
      last_round_day = company_params["last_round_date(3i)"]
    end

    {
      :name => company_params[:name],
      :status => company_params[:status],
      :market => company_params[:market],
      :country => company_params[:country],
      :city => company_params[:city],
      :funding_value => company_params[:funding_value],
      :funding_rounds => company_params[:funding_rounds],
      :first_round_date => "#{company_params["first_round_date(1i)"]}-#{first_round_month}-#{first_round_day}",
      :last_round_date => "#{company_params["last_round_date(1i)"]}-#{last_round_month}-#{last_round_day}"
    }
  end
end
