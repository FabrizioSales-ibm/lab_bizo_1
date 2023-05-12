# TLC_and_KSW API microservices and tools

### O Dockerfile é usado para criar Builds reproduzíveis para o seu aplicativo. Um fluxo de trabalho comum é fazer com que sua automação de CI/CD execute o comando "docker image build" como parte de seu processo de criação. Após a criação das imagens, elas serão enviadas para um central registry, onde poderão ser acessadas por todos os ambientes que precisam executar instâncias desse aplicativo. A imagem personalizada para o registro público do Docker, eh o Docker Hub, onde pode ser consumido por outros desenvolvedores e operadores.

## O Dockerfile contem as instrucoes necessarias linha por linha para criar uma imagem do Docker. Abaixo a explicacao das TAG'S dentro do Dockerfile
- FROM: Indica a imagem de origem (deve ser a primeira linha).
- MAINTAINER: Descricao do responsavel pela imagem.
- RUN: Executa um determinado comando dentro da imagem (criará um layer a cada RUN)
- CMD: Proposito de executar um comando final na imagem
- ENTRYPOINT: Binario que será executado após a incialização do container.
- EXPOSE: A porta que a imagem possui para uma determinada porta TCP / UDP (PortaHost:PortaContainer)
- ADD: Adiciona um arquivo empacotado (tar) no destino, link (url) ou arquivo.
- ENV: Informa variaveis de ambiente ao container.
- VOLUME: Permite a utilização de um ponto de montagem.
- USER: Determina qual o usuario será utilizado na imagem. (default root)

Tips: O arquivo deve seguir o padrao de iniciar com a letra "D" em maiusculo.

### para criar a imagem a partir do Dockerfile
```sh
$docker build --tag python-docker .
```
### Para reiniciar, parar e iniciar o container faca o stop/start/restart + container; ou o docker-run para executar o container junto com a variavel de ambiente AMBIENTEPROXY. Pode colocar no Dockerfile tb com ENV 
```sh
$docker run --publish 3000:5000 -e AMBIENTEPROXY=api-qas.xxxxxx.com.br python-docker
 
$docker stop/start/restart 7a7
```

### acessando os containers. Suprimindo o parametro "-a", voce visualiza apenas os containers em execucao.
```sh
$docker ps -a
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS                      PORTS                                                                       NAMES
7a7f52547e40        python-docker       "python3 serviceGAN_…"   About an hour ago   Up 3 seconds                 0.0.0.0:3000->5000/tcp   nice_ellis
```
### executar comandos na imagem
```sh
$docker exec -it 7a7 bash           

root@7a7f52547e40:/app# ls -l
total 24
-rw-r--r-- 1 root root  192 Jun  1 21:27 Dockerfile
-rw-r--r-- 1 root root  449 Jun  1 21:27 requirements.txt
-rw-r--r-- 1 root root 7054 Jun  1 21:43 serviceGAN_1.py
```

### visualizando os logs do container. Informando apenas os 3 primeiros bytes, voce tem acesso ao log
```sh
$docker logs 7a7

* Serving Flask app 'serviceGAN_1' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
serviceGAN_1.py:53: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if httpNode3.headers['Content-Type'] is 'application/json':
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:5000/ (Press CTRL+C to quit)
 * Restarting with stat......
```


### para vizualizar as imagens
```sh
$docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
python-docker          latest              9b933cfe700b        About an hour ago   215MB
python                 3.8-slim-buster     f2c36f6f6523        8 days ago          114MB
```

 
### para limpar as imagens iniciadas e paradas
```sh
$docker system prune
```
 
### visualizar memoria, container e cpu usada
```sh
$docker stats
```

### visualizar as configuracoes da imagem 
 $docker inspect 7a7
 
### remover o container do docker
```sh
$docker ps -a
$docker rm 7a7
```
 
### remover a imagem 
```sh
$docker images
$docker rmi 7a7
```

## Criando clusters Kubernetes
### Crie o cluster Kubernetes no console do IBM Cloud e defina com qual cluster Kubernetes o kubectl se comunica

### Faça o login na IBM Cloud e logo após crie o cluster
```sh
$ibmcloud login -sso
$ibmcloud target -g Default
$ibmcloud ks cluster create classic --name iks-mycluster-app
$ibmcloud ks cluster ls
 Nome                ID                     Estado      Criado          Trabalhadores   Local   Versão        Nome do Grupo de Recursos   Provedor   
iks-mycluster-app    cbttpu1f0a2fcgh7m35g   deploying   8 minutes ago 1   ams03   1.23.9_1539   Default                     classic  

 Nome                ID                     Estado   Criado           Trabalhadores   Local    Versão        Nome do Grupo de Recursos   Provedor   
iks-mycluster-app    cbttpu1f0a2fcgh7m35g   normal   15 minutes ago 1    ams03   1.23.9_1539   Default                     classic   
```
### Faça download e inclua o arquivo de configuração kubeconfig para o seu cluster em seu kubeconfig existente em ~/.kube/config ou no último arquivo na variável de ambiente KUBECONFIG. Toda vez que você efetua login na CLI do IBM Cloud® Kubernetes Service para trabalhar com clusters, deve-se executar esses comandos para configurar o caminho para o arquivo de configuração do cluster como uma variável de sessão. O Kubernetes CLI usa essa variável para encontrar um arquivo de configuração local e certificados que são necessárias para se conectar ao cluster no IBM Cloud.
```sh
$ibmcloud ks cluster config -c iks-mycluster-app
$kubectl config current-context
```

### Crie uma implementação. As implementações são usadas para gerenciar pods, que incluem instâncias conteinerizadas de um app. O comando a seguir implementa o app em uma única pod ao referir-se à imagem que você construiu em seu registro privado ou publico.
```sh
$kubectl create deployment iks-mycluster-deployment --image=sampabizo/microservicepython 
```

### Torne o app acessível ao mundo expondo a implementação como um serviço NodePort
```sh
$kubectl expose deployment/iks-mycluster-deployment --type=NodePort --port=5000 --name=iks-mycluster-service --target-port=5000
```

### Voce pode criar os objetos através do arquivos de manifestos Kubernetes definidos em YAML ou JSON ao invés dos comandos acima.
```sh
$kubectl apply -f iks-mycluster-deployment.yaml
$kubectl apply -f iks-mycluster-service.yaml
```

### Agora que todo o trabalho de implementação está pronto, é possível testar seu app
```sh
$ kubectl describe service iks-mycluster-service

Name:                     iks-mycluster-service
Namespace:                default
Labels:                   app=iks-mycluster-deployment
Annotations:              <none>
Selector:                 app=iks-mycluster-deployment
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       172.21.13.235
IPs:                      172.21.13.235
Port:                     <unset>  5000/TCP
TargetPort:               5000/TCP
NodePort:                 <unset>  30559/TCP
Endpoints:                172.30.180.77:5000
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>


$ ibmcloud ks worker ls --cluster iks_mycluster_app

ID                                                       IP Público       IP Particular   Tipo   Estado   Status   Zona    Versão   
kube-cbttpu1f0a2fcgh7m35g-iksmycluste-default-000000c6   159.122.186.62   10.144.194.14   free   normal   Ready    mil01   1.23.9_1541   
```

## IMPORTAR o CURL no postman
### as API's utilizadas para teste são todas que iniciam por BFF
curl --location --request GET 'http://159.122.186.62:30559/calc?operand1=888&operand2=21&operator=%2B'

curl --location --request POST 'http://159.122.186.62:30559/calc' \
--header 'Content-Type: application/json' \
--data-raw '    {
        "a": 22,
        "b": 2,
        "op": "+"
    }'


:+1:
