Hey Programmer 👋🏻,


I am Tushar Vilas Gharge 👨🏻, created this YourBank (National Bank) project backend with python programming language with FastAPI  Framework. Project contains some main features of banking System as

   •	Creating bank account
   
   •	Deposit money
   
   •	Withdraw money
   
   •	Transfer money
   
   •	Bank statement
   
How to start project :


****Step  1**: Direct to virtual env path of the project with below command :**

     .\venv\Scripts\activate

**** Step 2**: Then install the all project requirement with help of below command:**
 
       pip install -r requirements.txt

****Step 3**: start the server:**

      uvicorn app.main:app --reload


Backend of project is connect with postgres database and envrinment variables are used as below

          DATABASE_HOSTNAME=localhost
          DATABASE_PORT=5432
          DATABASE_PASSWORD= <Database Passoword>
          DATABASE_NAME=postgres
          DATABASE_USERNAME=postgres
          SECRET_KEY=09d2ergesgfdg34erftgrvcv5e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
          ALGORITHM=HS256
          ACCESS_TOKEN_EXPIRE_MINUTES=300


  
 All APIS docs using swagger Ui:

 ![image](https://github.com/TusharGharge/National_bank/assets/57088502/38a9e22c-24ea-49c8-ac42-74d75f0a148b)


**How project works:**
 This project is implemented with core features of  Bank using fastapi.

**1)	Users :**
**Create user**:

While implementation of Authentication for this project we use **JWT TOKEN ** . This is post method Api required input as below feild:

  {
    "email":"tushargharge05@gmail.com",
    "password":"Hello@world",
    "name":"Tushar Gharge",
    "phone_number":"1234567893"
}

****![image](https://github.com/TusharGharge/National_bank/assets/57088502/67f99fc3-60c4-4f94-8dcc-9787d2c51850)

**2) Authentication:**
   Login : 
   
   This is post method Api, which mainly help us to login user in application .required input feild as below:
   ![image](https://github.com/TusharGharge/National_bank/assets/57088502/82b961ea-322e-4581-b96a-e7bfe365fb91)

  it's return access_token and token_type as output which is mainly use at frontend for session storage and for backend as authentication for all other apis.

**3) Bank Feature:**

   1) Create Account:

      After Login, User required to create bank account to perform other features of application, it's required the Pan_card number as input with JWT token value:
     ![image](https://github.com/TusharGharge/National_bank/assets/57088502/f9f4215f-39f3-4d2f-aa34-5fb087a2aa88)


      once user provide the valid pan number return "user account has been created " as response. We create user bank account with 0 balance.

  2) Balance:

      This API provide remaining balance of user account. This is get method required the attribute is user authenticated JWT Token which is generated after login of user:

     ![image](https://github.com/TusharGharge/National_bank/assets/57088502/827c1b1b-e13e-4a6c-b45a-2032f653afb3)

      As we createding O Balance account it's return balance as 0 and account holder id.

 3) Deposite:

      This is Put Method API, mainly foused on deoposit money in user account, required the amount to deposit and JWT Token.

      Test cases:
    
      if yours amount is less then 500 it's marked as error in system and provided accurate response to user .

      ![image](https://github.com/TusharGharge/National_bank/assets/57088502/fa975a97-2085-4881-b49a-3a797f798f32)

      once user provide value more then 500 it's provide response as despoit successful.

      ![image](https://github.com/TusharGharge/National_bank/assets/57088502/30dd7f67-81d0-4ec8-a1ba-1909ab9a35a2)

4) Withdraw:

     This is Put method API, Which help us to withdraw amount from user bank account required field is amount and JWT Token.

   ![image](https://github.com/TusharGharge/National_bank/assets/57088502/6f064c54-31a4-4b43-ae11-d5860f91a3e4)

5) Transfer:

    This is Put Method API, Help us to transfer money to user account to reciver account of same data base. required the feilds are amount and bank account number with JWT Token.
     **How it's works:**
    ** 1) Check Account:**
   
     Once user hit the api, it's check the user account is present or not.

     ![image](https://github.com/TusharGharge/National_bank/assets/57088502/9b124435-792e-47c2-be6f-7ddb1049c59c)

      if user account is not present them it's written message.

     **2) Insufficient fund :**

     This test case check where entered values in greater than sender account balance.
   
     ![image](https://github.com/TusharGharge/National_bank/assets/57088502/586469e3-e1bc-4cd3-b5f6-4b0e076c7c0a)

     if error occured , return as "Insufficient fund".

   ** 3) Transfer sucessful:**
   
    if entered account and amount test case run successfully , we are able to transfer amount to desire account.
   
    ![image](https://github.com/TusharGharge/National_bank/assets/57088502/6c652b60-80b8-4c38-8998-e33dfc0ea7c6)

   ** 4) Statement:**

   This is Get Method Api, reuired user Authentication to return response. This Api return all transaction of user from account creation to all other apis success failed status.

   ![image](https://github.com/TusharGharge/National_bank/assets/57088502/a76a2144-cf09-4f5a-97f1-d76209c05504)

  ##############################################################################################################################################################################

  DEMO VIDEO:

  
   


    

https://github.com/TusharGharge/National_bank/assets/57088502/78c550ea-6039-4dc5-af0b-3f6062a74af6


##############################################################################################################################################################################

Thank you for the reading 🧑🏻, I am open to work with you. DM me over here https://www.linkedin.com/in/tushargharge/. 


Bye 👋🏻.


      
  
        

  



       
      

