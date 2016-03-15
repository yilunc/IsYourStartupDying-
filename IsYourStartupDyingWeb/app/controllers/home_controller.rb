class HomeController < ApplicationController
  def index
    @companies = Company.all
    @users = User.all
  end
end
