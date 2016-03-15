Rails.application.routes.draw do
  devise_for :users
  root "home#index", as: :home
  post "classify", to: 'classify#run_classify', as: :classify
end
