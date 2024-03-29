# Projeto de Redes de Computadores

Transferência de arquivos via `socket` usando protocolo TCP.

## Como executar

O presente programa pode ser executado tanto em sistema operacional Linux quanto no Windows 11. O programa **não** foi testado no WSL.

Para executá-lo garanta que está usando uma versão do Python maior ou igual a 3.10.5 (não testamos versões menores que essa). Agora, navegue até a pasta do projeto e instale as bibliotecas necessárias, utilizando o comando abaixo.

```bash
pip install -r requirements.txt
```

As bibliotecas externas utilizadas foram as descritas abaixo. Foram utilizadas apenas para a GUI do cliente.

-   CTkMessagebox==2.5
-   CTkTable==1.1
-   customtkinter==5.2.2
-   darkdetect==0.8.0
-   packaging==24.0
-   pillow==10.2.0
-   python-tkdnd==0.2.1
-   ttkwidgets==0.13.0

Para executar a aplicação do **cliente** use o comando abaixo.

```bash
python src/app.py
```

Para executar a aplicação do **servidor** use o seguinte comando.

```bash
python src/server.py
```
