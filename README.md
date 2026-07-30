## Deploy
To start server you need to type commend (in main folder):

docker compose up

You may be forced to use sudo if you do it on Linux.

If you want to force rebuild of container (for examle: after some change in code):

docker compose up --build

You may also add -d, if you don't worry, about logs.

docker compose up --build -d

## Backend

After deploying Docker, server will be ready on [localhost:8000](http://localhost:8000/subjects/). Nothing else is requred to work.

## Database

Databese to work need docker to work.

Databese is permanent and indepenedent from Docker. It means, values stays, after docker go down. It also mean you have innitialise it, before using it. Look at database/help.txt for futere intsructions.