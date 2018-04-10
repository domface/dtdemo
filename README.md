
> demo for DT project

> you must have docker installed to run the project locally

## Pull all Node Libraries



- Make sure your have node.js installed locally. 
- After installing node, in the project root directory,
``` bash
$ cd ./www/dt
$ npm install 
$ npm run build
```
- This will create a prod ready Vue.js app.





## Build With Docker

- Go back to the project root and set up your docker environment:
``` bash

$ docker-compose build
$ docker-compose up -d

```
- in your /etc/hosts file add the line

``` bash

0.0.0.0 test-dt.jawn.it



```
Point your browser to http://test-dt.jawn.it

Enjoy!
