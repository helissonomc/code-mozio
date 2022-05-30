# code-mozio
---
This project was deployed on AWS service [EC2](https://aws.amazon.com/pt/ec2/?trk=63a7a335-cea1-4409-aee6-e5f58957564a&sc_channel=ps&sc_campaign=acquisition&sc_medium=ACQ-P|PS-GO|Brand|Desktop|SU|Websites|Solution|BR|EN|Text&s_kwcid=AL!4422!3!531081609831!b!!g!!%2Bamazon%20%2Bweb%20%2Bhosting%20%2Bservice&ef_id=CjwKCAjws8yUBhA1EiwAi_tpEYNPRh69Gxhix6bS7dhVomhaigdFBx-iA9Q9NgZPixu-q9gWKJ73MhoCclYQAvD_BwE:G:s&s_kwcid=AL!4422!3!531081609831!b!!g!!%2Bamazon%20%2Bweb%20%2Bhosting%20%2Bservice)


## Technologies used:
* Python
* [Django](https://www.djangoproject.com/)
* [Django Restframework](https://www.django-rest-framework.org/)
* [Docker](https://www.docker.com/)
* Postgis
* AWS EC2

## The Application
 
The application can be devided in two main model:
* Provider: This model is used as the default User, it is resposible for the authentication and crud of user.
  * Route for token authentication: `/api/user/token/`;
  * Route to create new Provider: `/api/user/create/`;
  * Route to get, update, delete Provider `api/user/me/`
* ServiceArea: This model stores the polygons of the Provider.
  * Route to get ServiceArea `/api/servicearea/servicearea-list/` + query params `latitude` and `longitude`
  * Route to delete, update ServiceArea `/api/servicearea/servicearea-detail/{id}/`. Ps:.Only autheticated provider can change theirs ServiceArea.
  * Route to create ServiceArea `/api/servicearea/servicearea-list/`
    ```
    Example Payload
    {
      "name": "Test Service Area",
      "price": "2.00",
      "polygon": [
          {"lat": "-2", "lng": "0"},
          {"lat": "0", "lng": "1"},
          {"lat": "1", "lng": "1"},
          {"lat": "1", "lng": "0"},
          {"lat": "-2", "lng": "0"}
      ]
    }
    ```
 ## Postgis
 This tool was used because it suports operations with polygons and it makes esier to the developer to build applications and it gives us super fast queries.
 ## Documentation
 The documentation of the aply is available in :
 https://code-mozio.44.196.169.7.nip.io/api/docs/
 
 ## Locally
 To Execute locally, just create a `.env` in the respository root and then execute
 ```
  docker-compose up --build
 ```
 
 ## Tests
 All tests implemented here was successfull. All the code followed the pep8 and to avoid mistakes in the library `flake8` was used to the pep8 be correct;
