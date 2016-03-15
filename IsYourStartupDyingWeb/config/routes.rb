Rails.application.routes.draw do
  devise_for :users
  root 'companies#index'
end
