<h1 align="center">Naiper Bot</h1>

Versão do Python: 3.10.4

# O que é o Naiper?
Naiper é um bot de música para o discord escrito em Python com algumas funções adicionais.

# Como Utilizar
Você precisa criar uma aplicação no site
[Discord Developer Portal](https://discord.com/developers/applications/).

## Configuração do Token

Após a criação da sua aplicação no passo acima, você deve mudar os nomes dos arquivos citados abaixo e configurar o token e id's no arquivo "config.json" que já possui a estrutura necessária, caso contrário, você vai ter problemas na execução.
<hr>

## Arquivos

Arquivo "/modulos/example_guild.json" -> "/modulos/guild_ids.json"

Arquivo "/music/example_last_song.json" -> "/music/last_song.json"

Arquivo "/music/playlist_example.json" -> "/music/playlist.json"

<br/>

Todos os arquivos citados acima devem ter a seguinte estrutura:
```
{

}
```
Arquivo "/utils/example_config.json" -> "/utils/config.json"

<hr>

## Token e Id's
Para pegar os id's do seu servidor, você deve habilitar a função "Desenvolvedor" nas configurações do discord.
<hr>

## Inicialização

Após realizar todas as mudanças necessárias, chegou a hora de iniciar o bot. Para isso, é necessário apenas executar o arquivo dentro de uma IDE (ou usar o comando a seguir para executar com um CMD).

```
python3 main.py
```
<hr>

## Contato

[Discord Naiper Bot](https://discord.gg/BVApt3WGPf)

Dev: MagicSadWorld#6807