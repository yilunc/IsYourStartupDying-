Rails.application.routes.draw do
  devise_for :users
  root 'companies#home'
  get '/index', to: "companies#index"
  resources :companies
end
