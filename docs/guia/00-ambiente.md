# Lição 00: Ambiente e Docker

## Objetivo

Rodar as três peças do projeto na sua máquina (banco, API e frontend), entender o papel de cada uma e mexer no cardápio pelo painel de administração.

Ao final, você vai ter três coisas funcionando ao mesmo tempo:

```
Docker ─ PostgreSQL (porta 5432)
           ↑
Django ─ API (porta 8000)  ←──  React ─ frontend (porta 5173)
```

## Conceitos

### Docker aplicado ao projeto

Você já instalou o Docker. Agora veja como ele é usado aqui. Abra o arquivo `docker-compose.yml` na raiz do projeto:

```yaml
services:
  db:                          # nome do serviço; poderia ter outros (redis, api...)
    image: postgres:17         # IMAGEM: o "molde" oficial do Postgres, versão 17
    environment:               # variáveis de ambiente que a imagem lê ao iniciar
      POSTGRES_USER: comanda   #   cria este usuário
      POSTGRES_PASSWORD: comanda
      POSTGRES_DB: comanda     #   e este banco
    ports:
      - "5432:5432"            # PORTA: "porta do seu PC : porta dentro do container"
    volumes:
      - dados_postgres:/var/lib/postgresql/data   # VOLUME: onde os dados ficam guardados
    healthcheck:               # como o Docker sabe se o banco já está pronto
      test: ["CMD-SHELL", "pg_isready -U comanda"]
      interval: 5s

volumes:
  dados_postgres:              # declara o volume
```

Dois conceitos novos aparecem aqui:

- **Porta (`ports`)**: o container é isolado, como uma caixa fechada. `"5432:5432"` abre um buraco na caixa: quem acessar `localhost:5432` no seu PC chega na porta 5432 de dentro do container. É por isso que o Django consegue falar com o banco.
- **Volume (`volumes`)**: um container pode ser apagado e recriado a qualquer momento, e tudo que estiver só dentro dele some junto. O volume é uma pasta guardada **fora** do container, gerenciada pelo Docker. Os dados do banco ficam nele e sobrevivem quando o container é recriado.

### Ambiente virtual do Python (`.venv`)

Cada projeto Python precisa de versões específicas de bibliotecas (Django 6, DRF...). Se tudo fosse instalado no Python "global" do Windows, projetos diferentes entrariam em conflito. O **ambiente virtual** é uma cópia isolada do Python só para este projeto, na pasta `api\.venv`.

Por isso os comandos usam `.venv\Scripts\python` em vez de só `python`: é o Python do projeto, com as bibliotecas do projeto.

É a mesma ideia do `node_modules` do JavaScript, que guarda as bibliotecas de cada projeto dentro da própria pasta.

### Vite e `npm run dev`

O navegador não entende TypeScript nem JSX (aquele HTML dentro do JavaScript que você vai ver na lição 01). O **Vite** é a ferramenta que converte tudo isso para JavaScript comum.

- `npm run dev` sobe um servidor de desenvolvimento em `http://localhost:5173`. Quando você salva um arquivo, a página atualiza sozinha (é o *hot reload*).
- `npm run build` gera a versão final e otimizada na pasta `dist/`. É ela que vai para produção.

### Por que existe CORS

O frontend roda em `localhost:5173` e a API em `localhost:8000`. Para o navegador, portas diferentes significam **origens diferentes**.

A regra de segurança se chama **política de mesma origem** (*same-origin policy*): por padrão, o JavaScript de um site não pode ler respostas vindas de outra origem. Sem ela, um site malicioso aberto numa aba poderia ler dados de outro site em que você está logado.

O **CORS** (*Cross-Origin Resource Sharing*) é o jeito de o servidor **abrir uma exceção** a essa regra: a API responde com um cabeçalho dizendo "eu aceito ser lida por `http://localhost:5173`". No projeto, isso está em `CORS_ALLOWED_ORIGINS`, dentro de `api/config/settings.py`.

Guarde isso: quando aparecer um erro de CORS no console, o problema quase nunca está no código do React. É a API que não autorizou aquela origem.

## Passo a passo

Abra o **Docker Desktop** antes de começar e espere a baleia indicar "Engine running".

1. **Suba o banco.** No PowerShell, dentro da pasta `comanda`:
   ```powershell
   docker compose up -d --wait
   docker compose ps
   ```
   O `-d` roda em segundo plano e o `--wait` espera o banco ficar pronto. O `ps` deve mostrar `comanda-db-1` com status `healthy`.

2. **Prepare a API.** O ambiente virtual e as dependências já foram instalados. Rode:
   ```powershell
   cd api
   .venv\Scripts\python manage.py migrate
   .venv\Scripts\python manage.py seed_cardapio
   ```
   O `migrate` cria as tabelas. O `seed_cardapio` cadastra o cardápio de exemplo. Se ele disser "Cardápio já existe", está tudo certo: ele não duplica nada.

3. **Crie o seu usuário do painel de administração:**
   ```powershell
   .venv\Scripts\python manage.py createsuperuser
   ```
   Escolha um nome de usuário e uma senha. O e-mail pode ficar em branco.

4. **Suba a API:**
   ```powershell
   .venv\Scripts\python manage.py runserver
   ```
   Deixe este terminal aberto. Abra no navegador:
   - `http://localhost:8000/api/cardapio/`: o cardápio em JSON. É exatamente isso que o React vai consumir.
   - `http://localhost:8000/admin/`: entre com o usuário que você criou.

5. **Mexa no cardápio pelo admin.** Em *Produtos*, abra o X-Burger, mude o preço e salve. Recarregue `/api/cardapio/` e veja o preço novo. Depois volte ao preço original.

6. **Suba o frontend.** Abra **outro** terminal na pasta `comanda`:
   ```powershell
   cd web
   npm run dev
   ```
   Abra `http://localhost:5173`. Deve aparecer "Comanda" e a frase "Ambiente pronto".

7. **Rode os testes do frontend.** Em um terceiro terminal:
   ```powershell
   cd web
   npm run test:run
   ```

8. **Explore a pasta `web/`.** Abra no VS Code e identifique:
   - `index.html`: a única página HTML. O React "desenha" tudo dentro da `<div id="root">`.
   - `src/main.tsx`: o ponto de entrada. Ele liga o React a essa `div`.
   - `src/App.tsx`: o primeiro componente. É ele que você vai mudar na lição 01.
   - `src/index.css`: uma linha só, `@import "tailwindcss";`, que ativa o Tailwind.
   - `vite.config.ts`: a configuração do Vite e dos testes.
   - `package.json`: as dependências e os comandos (`dev`, `build`, `test`...).

## Como saber se funcionou

- [ ] `docker compose ps` mostra o banco como `healthy`.
- [ ] `/api/cardapio/` mostra 4 categorias em JSON.
- [ ] O preço que você mudou no admin aparece no JSON.
- [ ] `http://localhost:5173` mostra a página "Comanda".
- [ ] `npm run test:run` mostra `1 passed`.

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| `error during connect` ou `The system cannot find the file specified` | Docker Desktop fechado | Abra o Docker Desktop e espere "Engine running" |
| `port is already allocated` na porta 5432 | Já existe outro Postgres instalado no Windows usando essa porta | Pare o serviço "postgresql" em *Serviços* do Windows, ou troque a porta do compose para `"5433:5432"` e rode a API com `$env:DATABASE_URL='postgres://comanda:comanda@localhost:5433/comanda'` |
| `connection refused` ao rodar `migrate` | O banco ainda não subiu | Rode `docker compose up -d --wait` de novo |
| `No module named django` | Usou `python` em vez de `.venv\Scripts\python` | Use sempre o Python do `.venv` |
| `Missing script: "dev"` | Rodou `npm` fora da pasta `web` | Entre em `web` com `cd web` |

Para desligar tudo no fim do dia: `Ctrl+C` nos terminais da API e do front, e `docker compose stop` para o banco. Os dados continuam salvos no volume.

## Na entrevista

**"O que é um container e qual a diferença para uma máquina virtual?"**
Um container empacota a aplicação com as dependências dela e roda isolado, mas compartilha o núcleo (kernel) do sistema operacional da máquina. Uma máquina virtual simula um computador inteiro, com sistema operacional próprio. Por isso o container é muito mais leve: sobe em segundos e ocupa megabytes, não gigabytes.

**"Para que serve o Docker Compose?"**
Para descrever num arquivo só todos os serviços de que o projeto precisa (banco, cache, API...) e subir tudo com um comando. No meu projeto ele sobe o PostgreSQL, então qualquer pessoa roda o projeto sem instalar banco na máquina.

**"Se o container for apagado, os dados do banco se perdem?"**
Não, se houver um volume. O volume guarda os dados fora do container. É o que eu uso no `docker-compose.yml` do projeto.

**"O que é CORS e por que o navegador bloqueia a requisição?"**
O navegador aplica a política de mesma origem: o JavaScript de um site não pode ler respostas de outra origem (domínio, porta ou protocolo diferente). Isso impede que um site malicioso leia dados de outros sites usando a sessão do usuário. CORS é o mecanismo pelo qual o servidor libera origens específicas, por meio de cabeçalhos HTTP como `Access-Control-Allow-Origin`. Por isso o erro de CORS se corrige no servidor, não no front. No meu projeto, isso é o `CORS_ALLOWED_ORIGINS` no Django.

**"Qual a diferença entre `npm run dev` e `npm run build`?"**
O `dev` sobe um servidor de desenvolvimento com recarregamento automático e sem otimização, feito para programar. O `build` gera arquivos estáticos otimizados (minificados e agrupados) em `dist/`, que é o que vai para produção.
