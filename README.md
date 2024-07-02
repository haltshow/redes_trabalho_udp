# Redes_Projeto

**1- Motivação / Objetivo**

Optamos por usar o protocolo UDP para o streaming de tela ao vivo com o objetivo de explorar suas características específicas que o tornam ideal para aplicações como transmissão de mídia em tempo real. A escolha do UDP em vez do TCP se deve à sua menor sobrecarga de controle de fluxo e latência reduzida, o que é crucial para garantir uma transmissão contínua e rápida de dados. Nosso foco é demonstrar como o UDP facilita uma comunicação direta e eficiente entre clientes e servidor, especialmente importante quando a velocidade é prioritária em relação à precisão na entrega de cada pacote.


**2- Descrição**


O cliente streamer irá iniciar uma transmissão da sua tela em tempo real. Os outros clientes, ao se conectarem, irão visualizar a mesma tela e o mesmo frame, abaixo segue o passo a passo do que ocorrerá com detalhadamente com a aplicação:


Captura de Tela: O usuário iniciará um servidor que captura constantemente a sua tela do desktop.
Transmissão via UDP: Os pacotes de vídeo são enviados através do protocolo UDP.
Recepção pelos Clientes: Vários clientes podem se conectar ao servidor simultaneamente e receber os pacotes de vídeo. Cada cliente decodifica e exibe os quadros conforme eles chegam, permitindo que todos visualizem a mesma tela em tempo real.

Essa abordagem de streaming ao vivo ilustra como o protocolo UDP pode ser eficiente para aplicações em tempo real, permitindo que vários usuários visualizem simultaneamente a tela compartilhada por um único servidor, com um foco maior na velocidade de transmissão do que na garantia de entrega absoluta de cada pacote.

**3- Objetivo didático**
Protocolo UDP: O Protocolo UDP é um dos principais protocolos de comunicação na Internet. Diferentemente do TCP, que garante a entrega de pacotes e a ordem correta deles, o UDP é um protocolo "sem conexão" e "não confiável", ou seja, ele não garante que os pacotes chegarão ao destino ou que chegarão na ordem correta. Esse comportamento é ideal para aplicações que podem tolerar perda de dados e que requerem alta performance, como o streaming de vídeo em tempo real.
O uso do UDP para streaming de vídeo é ideal em situações onde a latência precisa ser minimizada e a perda ocasional de pacotes não é crítica.





**4- Pré-requisitos de Uso**
Python - Necessário instalar o python no computador para rodar os scripts do projeto. Ex: python server.py, python streamer.py, python cliente.py


Pip Install - Comando para instalar as dependências necessárias para rodar o projeto. O projeto contém o arquivo requirements.txt com todas as dependências. Basta rodar o seguinte comando: pip install requirements.txt


