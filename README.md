# Comanda

Cardápio digital com acompanhamento de pedidos e tela de cozinha (KDS) em tempo real, feito para restaurantes e lanchonetes.

> Projeto em construção. A demonstração e o GIF entram aqui quando o frontend estiver pronto.

## O que é

- **Cardápio (cliente):** o cliente abre `/mesa/5` pelo QR code da mesa, escolhe produtos e adicionais, envia o pedido e acompanha o status ao vivo (Recebido → Em preparo → Pronto).
- **KDS (cozinha):** a cozinha vê os pedidos chegando na hora, em colunas por status, com tempo decorrido e alerta de atraso, e avança cada pedido com um clique.

## Arquitetura

```
[Navegador: React]  --HTTP (REST)-->  [Django + DRF]  -->  [PostgreSQL]
        ^                                   |
        +------ WebSocket (Channels) <------+
```

- Toda gravação passa pela API REST. O WebSocket só leva avisos do servidor para as telas.
- Os avisos saem depois que o banco confirma a gravação (`transaction.on_commit`).
- Ao reconectar, o frontend recarrega os dados pela API para não perder nenhum aviso.

## Tecnologias

| Parte | Tecnologias |
|---|---|
| Frontend | React, TypeScript, Vite, React Router, TanStack Query, Tailwind CSS, Vitest, Testing Library |
| Backend | Python, Django, Django REST Framework, Django Channels, Daphne, pytest |
| Banco e infraestrutura | PostgreSQL, Docker Compose |

## Como rodar localmente

Pré-requisitos: Docker Desktop, Python 3.12+ e Node 20+.

```powershell
# 1. Banco de dados
docker compose up -d --wait

# 2. API (primeira vez: criar o ambiente e instalar dependências)
python -m venv api\.venv
api\.venv\Scripts\python -m pip install -r api\requirements.txt

cd api
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py seed_cardapio
.venv\Scripts\python manage.py runserver

# 3. Frontend (em outro terminal)
cd web
npm install
copy .env.example .env
npm run dev
```

- API: http://localhost:8000/api/cardapio/
- Admin (cadastro do cardápio): http://localhost:8000/admin/ (crie um usuário com `python manage.py createsuperuser`)
- Frontend: http://localhost:5173

## API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/cardapio/` | Categorias com produtos ativos e seus adicionais |
| POST | `/api/pedidos/` | Cria pedido (o preço é calculado no servidor) |
| GET | `/api/pedidos/{id}/` | Detalhe de um pedido |
| GET | `/api/pedidos/ativos/` | Pedidos novos, em preparo e prontos, do mais antigo ao mais novo |
| PATCH | `/api/pedidos/{id}/status/` | Avança o status (`NOVO → EM_PREPARO → PRONTO → ENTREGUE`); fora da ordem retorna 409 |

| WebSocket | Quem conecta | Recebe |
|---|---|---|
| `ws/cozinha/` | KDS | `pedido_criado`, `pedido_atualizado` |
| `ws/pedidos/{id}/` | Tela do cliente | `pedido_atualizado` daquele pedido |

## Testes

```powershell
cd api; .venv\Scripts\python -m pytest     # backend
cd web; npm run test:run                   # frontend
```

## Decisões e limitações

- **Preço calculado no servidor:** o cliente envia só produtos, quantidades e adicionais. Preços enviados pelo navegador são ignorados.
- **Cópia do preço no pedido:** cada item guarda nome e preço do momento da compra. Mudar o cardápio depois não altera pedidos antigos.
- **Status só avança:** duas telas da cozinha clicando ao mesmo tempo não fazem o pedido pular etapa (`select_for_update` + resposta 409).
- **Um único servidor:** os avisos em tempo real usam `InMemoryChannelLayer`, que funciona com um processo. Para rodar vários servidores, o próximo passo é trocar por Redis (`channels_redis`).

## Próximos passos

Login da equipe, pagamento online, impressão de comanda, integração com iFood e suporte a vários restaurantes.

## Aprendizado

Este projeto foi construído como estudo de React. O roteiro das lições está em [`docs/guia/`](docs/guia/README.md).
