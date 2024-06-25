# PizzaDelivery_App

ROUTES TO IMPLEMENT

AUTHENTICATION:
.../auth/signup
.../auth/jwt/create         (signin)
.../auth/jwt/refresh        (refresh the access token)
.../auth/jwt/verify        (verify the validity of token)

ORDERS:
.../orders/                 (GET & POST orders)
.../orders/<int:pk>         (GET & POST)
.../orders/<int:pk>         (PUT & DELETE)

ORDER_STATUS:
.../orders/update-status/<int:pk>       (PUT)  (Only SuperUser)

USER ORDERS:
.../users/<userID>/orders       (GET all user orders)
.../users/<userID>/orders/<int:pk>       (GET a specific user's order)


#  HOW TO AUTHENTICATE ON POSTMAN:
1) .../auth/jwt/create         (for signin)
2) copy access token 
3) in the headers key :"Authentication", it's value is :"Bearer <paste the access token>"
4) then you can access the CRUD Api Operations, and add the data as JSON in Body




