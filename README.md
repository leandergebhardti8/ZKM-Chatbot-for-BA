## Deploy on Prod

# Rasa
Rasa is an open source machine learning framework for building contextual AI assistants and chatbots.
Rasa has two main modules:

NLU for understanding user messages
Core for holding conversations and deciding what to do next
Rasa X is a tool that helps you build, improve, and deploy AI Assistants that are powered by the Rasa framework. Rasa X includes a user interface and a REST API.

## Getting Started

This is an setup for a configuration of a chatbot with rasa. Data is used for the zkm-chatbot project.

### Prerequisites

What things you need to install the software

=======

# Rasa
Rasa is an open source machine learning framework for building contextual AI assistants and chatbots.
Rasa has two main modules:

NLU for understanding user messages
Core for holding conversations and deciding what to do next
Rasa X is a tool that helps you build, improve, and deploy AI Assistants that are powered by the Rasa framework. Rasa X includes a user interface and a REST API.

## Getting Started

This is an setup for a configuration of a chatbot with rasa. Data is used for the zkm-chatbot project.

### Prerequisites

What things you need to install the software

>>>>>>> 1972fa0f6d8772f690dbbda83f47d0e837ea8197
=======
### 1.  Access server
- on a new terminal run: 
>>>>>>> 52d89014f3d7e1084e093d97d0e8ebf3d44fff1d
```
ssh integr8@193.197.170.102
Integr8RASA_Chatbot
```
Changes since rasa 2.4.3
- rasax root folder:
```
cd /etc/rasa
```
- uses docker-compose to build containers:
- 
| Service	| Images	| Container Name |Dockerfile |
| ------------- | -------------- |-------------- |-------------- |
| rasa-x	| eersada/docker_hub_repo:rasax-zkm-01  |rasa_rasa-x_1 |/etc/rasa/Dockerfile_rasax|
| rasa production  | eersada/docker_hub_repo:production-zkm-03 |rasa_rasa-production_1  | /etc/rasa/Dockerfile_production|
| rasa worker | eersada/docker_hub_repo:production-zkm-03  |rasa_rasa-worker_1 |/etc/rasa/Dockerfile_rasax|
| client | /etc/rasa/client   | rasa_client_1| - |
| action server | eersada/docker_hub_repo:action-zkm-02   | rasa_app_1 | /etc/rasa/Dockerfile_action|

- rebuild action Docker-Image:
Incase changes are made in action server, the docker image needs to be rebuilt.
Steps:
- go to rasax root folder:
```
cd /etc/rasa
```
- replace Dockerfile with Dockerfile_action
```
cp Dockerfile_action Dockerfile
```
- build Docker Image of action server (Image name of action server : eersada/docker_hub_repo:action_zkm-02)
```
sudo docker build . -t eersada/docker_hub_repo:action_zkm-02
```
- Login to docker hub
```
cat password.txt | docker login --username eersada --password-stdin
```
- Push the Docker Image to Docker hub
```
docker push eersada/docker_hub_repo:action-zkm-02
```
- Restart docker-compose and new action Image will be loaded
```
docker-compose up -d
```
- In case Docker Image of production or rasax needs to be rebuilt, you just need to replace the Image name accordingly, you can find the corresponding information on the table above

- To rebuild client image
```
cd /etc/rasa
docker-compose build client
```
- go to chatbot root folder:
```
cd /etc/zkm-chatbot
```

### 2.  Merge changes to prod
- in the servers root folder type following arguments one by one:
```
sudo git checkout prod
sudo git pull origin master
sudo git merge master
** solve conflicts **
sudo git push origin prod
```
### 3.  Training and restart server
- Visit: https://chatbot8.zkm.de/train
- Then restart the serve


### Domain
The domain defines the universe your assistant lives in: what user inputs it should expect to get, what actions it should be able to predict, how to respond, and what information to store. The domain for our assistant is saved in a file called `domain.yml`:
```
cat domain.yml
```
For bot responses use names as follow:
```
utter_someName
```
sudo sh restart_server_f.sh
```
## Setup

#### Template for utterances

-  General example
```
utter_someName:
- text: "utter text"
  buttons:
    - payload: Payload button 1
      title: title button 1
    - payload: Payload button 2
      title: title button 2
  custom:
    - video: ""
      img: ""
      subtitle: ""
      delay: numberOfSeconds (default: 0)
      contact: bool (default: false)
      links:
        - payload: "link"
          title: "titleOfLink"
        - payload: "secondLink"
          title: "titleOfSecondLink"
```
utter_someName
```

#### Template for utterances

-  General example
```
utter_someName:
- text: "utter text"
  buttons:
    - payload: Payload button 1
      title: title button 1
    - payload: Payload button 2
      title: title button 2
  custom:
    - video: ""
      img: ""
      subtitle: ""
      delay: numberOfSeconds (default: 0)
      contact: bool (default: false)
      links:
        - payload: "link"
          title: "titleOfLink"
        - payload: "secondLink"
          title: "titleOfSecondLink"
```

#### Available tags for templates
These tags are specifically for this project, not rasa defaults.
To modify them take a look at `/channels/socketio.py` file.

#### Available tags for templates
These tags are specifically for this project, not rasa defaults.
To modify them take a look at `/channels/socketio.py` file.

* img
```
### credentials
```
* img
    custom:
      img: "url to the image" 	//default: ""
      subtitle: [String] 		//"text for copyrights"
```
Text
```
    custom:
      text: "simple text" 	//default: "" 
```
Contact
```
    custom:
      contact: bool 		//default: False
```
Go back button
```
    custom:
      withGoBack: bool 		//default: False 
```
Allow User typing
```
    custom:
      allowTyping: bool 	//default: True 
```
Feedback
```
    custom:
      feedback: bool 		//default: False
```
Delay
```
    custom:
      delay: numberOfSeconds 	//default: 0, Changing it wont affect text messages(they stay at it's default 
```
2), 
                                          just whatever is inside the custom tag (contact forms, video, img, etc.)

Links
 ```
    custom:
      links: 
        - payload: "link"           		//this is the link itself
          title: "titleOfLink"      		//A descriptive title for the link
          description: ""
          type: "link"					//options (link, email, phone) default link
        - payload: "secondLink"
          title: "titleOfSecondLink" 
 ```
Slider with >2 options to choose from
```
    custom:
      interval:
      - title: [String] "title of the option on the slider" 						//default: ""
        payload: [String] "define the name of the option which should be selected" 	//example: /opt1 (default: "")
```
        
Slider to choose (guess) a value
```
    custom: 
      slider:
      - min: [Integer] defines slider minimum                   	//default: 0
        max: [Integer] defines slider maximum                   	//default: 100
        unit: [String] "append Units on slider min & max"       	//default: "" | example: 'kg'
        interval: [Integer] slider interval                     	//default: 1 | example: 0.5
        mode: [String] 'slider mode'                            	//options ('exact', 'lower', 'bigger', 'between' (!!!solution_min & solution_max required!!!), 'any')
        solution: [Integer] value of solution                   	//example: 11.5
        solution_min: [Integer] defines minimum of solution range 	//used for between slider mode
        solution_max: [Integer] defines maximum of solution range 	//used for between slider mode
```
Quote 
```
    custom: 
      quote:
      - quotetext: [String] "text displayed in quote module"     	//default: ""
        quoteimage: [URL] "url to image"                         	//default: ""
        subtitle: [String] "text for copyrights"
        author: [String] "author name (date)"                    	//default: "" | example: "Kurd Alsleben, 1962"
```        
Pop Up Bio (Modal)
```
    custom:
      modal:
        img: [URL] "url to image"                                				//default: ""
        subtitle: [String] "text for copyrights"
        title: [Sgring] "title of the button to open modal (Artist name)"      	//default: "" | example: "Cord Passow")
      text: [String] "text displayed inside the modal itsel"     				//default: ""
```            
Guide Intro
```
    custom: 
      intro:
        text: [String] "text displayed in intro"                 				//default: ""
        img: [URL] "url to image displayed inside intro bubble"  				//default: ""
        subtitle: [String] "text for copyrights"
```    
Chatbot Icons
``` 
    custom:
      sphereTextContent: [Bezeichnung des Icons] "Regenbogen" / [utf8 text] "1960"
      sphereColor: [Farbe] "blue"
```

#### Helpful links for configuration
```
rasa docs: https://rasa.com/docs/rasa/

https://towardsdatascience.com/a-beginners-guide-to-rasa-nlu-for-intent-classification-and-named-entity-recognition-a4f0f76b2a96
```

### Important commands
1. Train a model:
```
rasa data validate  * To check if everything is alrigth with the data
rasa train

because of the huge amount of data, there is a small dataset (nlu, stories) on ./data/dev for quick testing  
to train it use:  
python train.py --dev  
from root directory  
```

2. To work with the client
```
open 3 terminals, command + t to open an additional terminal

1)In a terminal -> executes rasa server (previous: --cors "*" might lead to connection issue)
rasa run 
2)In a terminal -> executes rasa actions server
rasa run actions --actions actions
3)In a terminal -> execute client
cd client && npm run serve
```

### endpoints
http://chatbot8.zkm.de/

for chatbot
http://chatbot8.zkm.de/chatbot

for training
http://chatbot8.zkm.de/train
Have to soft restart the server.

### Better intent recognition
```
It is possible to increase the intent recognition in general. By:

1- All intents have to have 3 or more examples
2- important entities have to be specify in all examples

3- Avoid having intents with similar examples

What intents are similar can be found out by running the nlu_test script
it will return a collection of in the follwing form:

    {
        "intent": "veranstaltung_eintritt", >>>>>>>> expected intent
        "intent_prediction": {  >>>>>> intent that the bot actually predicted
            "confidence": 0.9999339580535889,
            "name": "eintrittspreise",  
            "story": "eintrittspreise -> - action_query_entrance"
        },
        "story": "veranstaltung_eintritt -> - utter_veranstaltung_eintritt", >>>>> the follow up answer to the intent.
        "text": "Ticketpreise" -> text that the bot use to predict
    },
    
What this means is when the bot passed the text "Ticketpreise" he expected to get intent "veranstaltung_eintritt", but got confused and got
the intent "eintrittspreise" with a 0.99 confidence (pretty high).
    
if two intents are similar try to convert them into one.

if two intents are similar, but can't have the same answer, convert them into one and differentiate with entities in the stories

// NOTE this trick might be outdated with the comming rasa version 2
example 
intent: ticketpreise
Preise [workshops](preisetype)
Preise [Museum](preisetype)  // slot has to be of type categorical 

then add two stories
## ticketpreise
* ticketpreise
    slot{"preisetype": "workshops"}
    - ticketpreise_workshops

## ticketpreise
* ticketpreise
    slot{"preisetype": "Museum"}
    - ticketpreise_museum
```

## duckling server

## production server

```
soft server restart -> when havent change any chatbot code
sudo sh restart_server.sh

hard server restart -> removes every container and builds bot again
sudo sh restart_server_f.sh

get new export.json
sudo sh getExport.sh

Have fun
Train
sudo sh train.sh
```

## Deployment (Dev env)
### Backend
 1) Heroku deploy
 ```
	 heroku git:remote --app zkm-chatbot -r heroku
 ```
 2) Login in heroku container
 ```
	 heroku container:login
 ```
 3) Push to server
 ```
	 heroku container:push web --app zkm-chatbot
 ```
 4) Put server live
 ```
	 heroku container:release web --app zkm-chatbot
 ```

 ### Frontend
1)  for client deployment.
 ```
	 cd client && npm run build
 ```
 it generates an app.js file, that can be found in `client/dist/js`

 2) upload new app.js to ZKM aws s3 bucket on `chatbot/js` folder
 link to bucket: https://s3.console.aws.amazon.com/s3/buckets/zkm-chatbot?region=eu-central-1&tab=objects
 old app.js has to be deleted

 3) select uploaded app.js, click on actions and then make public

## troubleshooting

1. cors policy problems with engineio
    its probably a versioning problem of some packages
    do: (`rasa version==1.2.3`)
	```
	    pip3 uninstall python-engineio
	    pip3 uninstall python-socketio
	    pip3 install python-engineio==3.8.1
	    pip3 install python-socketio==4.2.0
	```
2. Invalid yml (domain.yml not found, etc.)

	 - Use Visual Studio Code Plugin with Extension ID: 
		```
			redhat.vscode-yaml
		```
	- Or Visit:
http://www.yamllint.com/    #website that allows to check yml integrity, tells where errors are
		```
			rasa data validate  #rasa command to check yml integrity
		```
## Authors
INTEGR8 dev team
=======
>>>>>>> 52d89014f3d7e1084e093d97d0e8ebf3d44fff1d
