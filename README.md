# hatebu with ng

~~~
docker build -t hatebu_with_ng .
docker run -d --restart always -v hateng:/data --name hateng -p 80:5000 -p 8081:5001 -e MYDOMAIN='http://<domain_name>/' hatebu_with_ng:latest
~~~
