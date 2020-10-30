# TelegramBot-BookingWithTimeslot

Telegram bot for booking/reservation system using python.
<br>

![20-10-30-17-39-38_1](https://user-images.githubusercontent.com/64152220/97693310-372ee400-1a5e-11eb-8bc9-447e9ea98bb8.gif)  ![list](https://user-images.githubusercontent.com/64152220/97693784-e966ab80-1a5e-11eb-8624-dda6a5e14776.gif)  ![withdraw](https://user-images.githubusercontent.com/64152220/97693894-0f8c4b80-1a5f-11eb-99e7-ab0253e90e74.gif)  ![help](https://user-images.githubusercontent.com/64152220/97694847-66465500-1a60-11eb-85e1-ef5220000e88.gif)

## Technology used
- Telegram (interface)
- Firebase Firestore (database)
- Heroku (optional server)

## Steps To Recreate
#### 1. Clone this project repository.
#### 2. Install required packages in ```requirements.txt```.
- In the project directory terminal, run command:
  
        $ pip install -r requirements.txt
#### 3. Create Telegram bot Token.
- Open Telegram.

- Search for BotFather (pick the one with verified icon).
 
    ![telesearch](https://user-images.githubusercontent.com/64152220/97678799-a3571b00-1a51-11eb-8486-e33d03d162d3.png)

- Enter ```/newBot``` in the chat and then insert bot name.
  
    ![telecommands](https://user-images.githubusercontent.com/64152220/97679236-40b24f00-1a52-11eb-8c20-2f8f15f70810.jpg)

- Copy token given (yellow arrow^^).

- Create new file ```credentials.py``` and insert the following code.
  
        TOKEN = '<your-telegrambot-token>' 

#### 4. Create Firestore database.
- Create a Firebase account https://firebase.google.com (might need to insert billing information but don't worry it's still free).

- Go to Firebase console and click ```add project```.

- Give the project a name.

##### In ```Cloud Firestore``` tab.
- Click ```Create database```.

- Select ```Production Mode``` and click ```Next```.
 
  ![Webp net-resizeimage](https://user-images.githubusercontent.com/64152220/97683979-c84d8d00-1a55-11eb-918b-9da3ec8232e7.png)

- Go to ```Rules``` tab and change the ```false``` to ```true```.
  
![Screenshot (33)_LI](https://user-images.githubusercontent.com/64152220/97685620-53c71e00-1a56-11eb-91aa-0b180e05e34d.jpg)

##### In ```Settings``` tab.

- Go to ```Service Accounts```.

- Click ```Generate New Private Key```.
  
![Webp net-resizeimage (3)](https://user-images.githubusercontent.com/64152220/97688492-70178a80-1a57-11eb-96d0-94e97b88a016.png)

- A file will be downloaded. Rename the file name to ```firebase-adminsdk.json```.

- Insert the file in project directory.

#### 5. Run ```bot.py``` to run the script.
- This script need to be run 24/7 for better user experience.
- To deploy on Heroku, create new file ```Procfile``` (without file extension) and insert the following
  
        worker: python bot.py

## Files explaination

- ```bot.py```: Main script. This file will connect with Telegram API.
- ```firestore_service.py```: This file will connect with FireStore database.
- ```booking.py```: Contains Booking class.
- ```keyboards.py```: Contains keyboard layouts.

## TO DO

- [ ] Better way to delete past booking. Instead of delete when ```/withdraw```, delete daily.
- [ ] Better way to insert list into methods in ```keyboards.py```