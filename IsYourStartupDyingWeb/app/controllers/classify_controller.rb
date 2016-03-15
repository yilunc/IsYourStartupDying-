class ClassifyController < ApplicationController
  def run_classify
    name= params[:name]
    status = params[:status]
    market = params[:market]
    country = params[:country]
    city = params[:city]
    funding_value = params[:funding_value]
    funding_rounds = params[:funding_rounds]
    first_round_date = params[:first_round_date]
    last_round_date = params[:last_round_date]
    @result = `cd .. ; python classify_startup.py \'#{name}\' \'#{status}\' \'#{market}\' \'#{country}\' \'#{city}\' #{funding_value} #{funding_rounds} #{first_round_date} #{last_round_date}`.to_i
  end
end
