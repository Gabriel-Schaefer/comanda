# Comanda: cardápio digital + KDS em tempo real (design)

Data: 2026-09-28
Status: aguardando revisão

## 1. Objetivo

Projeto de portfólio para ganhar experiência real com React, voltado a uma vaga de frontend na Suitable (sistema para food service, Santa Cruz do Sul/RS, React preferencial).

Critérios de sucesso:
- App publicado com link público e repositório no GitHub com README (incluindo GIF da demo).
- O Gabriel consegue explicar cada parte do frontend em entrevista, porque escreveu os componentes.
- Bloco do projeto preenchido no currículo (`Gabriel_Lima_CV_Frontend.tex`).

Prazo: cerca de 2 semanas, com no mínimo 4 h/dia.

## 2. Divisão do trabalho (modo guiado)

- **Claude:** estrutura inicial (scaffold), configuração, backend Django completo, Docker Compose, guias de aprendizado e revisão do código do Gabriel.
- **Gabriel:** todos os componentes, hooks e testes do frontend React, seguindo os guias.
- Nenhuma etapa do frontend é entregue pronta. Os guias dão conceitos, passos e dicas, e trechos de código aparecem só para sintaxe nova.

## 3. Escopo

### Cardápio (cliente, mobile-first): rota `/mesa/:numero`
- Lista categorias e produtos (foto, nome, descrição, preço).
- Modal do produto: quantidade, adicionais (múltipla escolha) e observação.
- Carrinho: listar, alterar quantidade, remover item, ver total, enviar pedido.
- Após enviar, redireciona para `/pedido/:id`, que acompanha o status em tempo real (Recebido → Em preparo → Pronto).

### KDS (cozinha, desktop/tablet): rota `/cozinha`
- Três colunas: **Novos**, **Em preparo**, **Prontos**.
- Cartão do pedido: mesa, itens, adicionais, observações e tempo decorrido (atualiza a cada segundo).
- Um botão por cartão avança o status. Em "Prontos", o botão "Entregue" tira o pedido da tela.
- Pedido novo toca um som e fica em destaque. Pedido com mais de 15 min desde a criação fica vermelho.
- Indicador de conexão ("Conectado" / "Reconectando...").

### Fora do escopo
Login, pagamento, impressão, integração com iFood, multi-restaurante, tela de admin própria (o Django Admin cobre o cadastro do cardápio). Esses itens vão para "Próximos passos" no README.

## 4. Arquitetura

```
[Navegador: React]  --HTTP (REST)-->  [Django + DRF]  -->  [PostgreSQL]
        ^                                   |
        +------ WebSocket (Channels) <------+
```

Monorepo:
```
comanda/
  api/              Django (backend)
  web/              React (frontend)
  docs/guia/        lições de aprendizado
  docker-compose.yml  (PostgreSQL para desenvolvimento)
```

### 4.1 Backend (`api/`)
- Python 3.14 (já instalado), Django na versão estável atual compatível, Django REST Framework, Django Channels, Daphne (servidor ASGI), django-cors-headers, psycopg.
- Configuração por variáveis de ambiente (`DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`).
- Channel layer: `InMemoryChannelLayer`, suficiente para um único processo. Limitação documentada: escalar para vários servidores exige Redis (`channels_redis`).
- Comando `python manage.py seed_cardapio` cria um cardápio de exemplo.

### 4.2 Frontend (`web/`)
- Vite + React + TypeScript, React Router, TanStack Query, Tailwind CSS.
- Carrinho: Context + `useReducer`, sem biblioteca de estado.
- Tempo real: hook próprio `useWebSocket`, sem biblioteca.
- Testes: Vitest + Testing Library.
- URL da API por variável `VITE_API_URL`.

## 5. Modelo de dados

| Modelo | Campos |
|---|---|
| `Categoria` | `nome`, `ordem` |
| `Produto` | `categoria` (FK), `nome`, `descricao`, `preco` (Decimal), `imagem_url` (opcional), `ativo` |
| `Adicional` | `produto` (FK), `nome`, `preco` (Decimal) |
| `Pedido` | `mesa` (int > 0), `status`, `total` (Decimal), `criado_em`, `atualizado_em` |
| `ItemPedido` | `pedido` (FK), `produto` (FK), `nome_produto`, `preco_unitario`, `quantidade`, `observacao` |
| `ItemPedidoAdicional` | `item` (FK), `adicional` (FK), `nome`, `preco` |

`ItemPedido` e `ItemPedidoAdicional` guardam nome e preço copiados no momento do pedido, para que mudar o cardápio depois não altere pedidos antigos.

Status do pedido e transições permitidas (só para frente):
`NOVO → EM_PREPARO → PRONTO → ENTREGUE`

## 6. API REST

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/cardapio/` | Categorias com produtos ativos e seus adicionais |
| POST | `/api/pedidos/` | Cria pedido |
| GET | `/api/pedidos/{id}/` | Detalhe de um pedido |
| GET | `/api/pedidos/ativos/` | Pedidos com status NOVO, EM_PREPARO ou PRONTO, do mais antigo ao mais novo |
| PATCH | `/api/pedidos/{id}/status/` | Avança o status |

Corpo do `POST /api/pedidos/`:
```json
{
  "mesa": 5,
  "itens": [
    { "produto_id": 3, "quantidade": 2, "adicionais": [7, 8], "observacao": "sem cebola" }
  ]
}
```

Regras:
- `total`, `preco_unitario` e preços de adicionais são **calculados no servidor**. Preços enviados pelo cliente são ignorados.
- Validações (400): lista de itens vazia; `mesa` menor que 1; `quantidade` fora de 1–20; produto inexistente ou inativo; adicional que não pertence ao produto; observação com mais de 200 caracteres.
- `PATCH .../status/` com corpo `{"status": "EM_PREPARO"}`. Transição fora da ordem retorna **409 Conflict**.
- A criação do pedido é atômica (`transaction.atomic`).

## 7. Tempo real (WebSocket)

| Rota | Quem conecta | Recebe |
|---|---|---|
| `ws/cozinha/` | KDS | `pedido_criado`, `pedido_atualizado` |
| `ws/pedidos/{id}/` | tela do cliente | `pedido_atualizado` daquele pedido |

Formato da mensagem: `{"tipo": "pedido_criado" | "pedido_atualizado", "pedido": { ...mesmo formato do GET /api/pedidos/{id}/ } }`.

- Os avisos saem com `transaction.on_commit`, ou seja, só depois que o banco confirmou a gravação.
- O WebSocket é somente de recebimento. Toda escrita passa pela API REST.
- Ao (re)conectar, o frontend recarrega os dados via REST (invalidando a query do TanStack Query) para não perder mensagens enviadas enquanto estava desconectado.
- Reconexão com espera crescente (1 s, 2 s, 4 s... até 30 s).

## 8. Tratamento de erros (frontend)
- Toda tela com dados remotos tem estados de carregando, erro (com botão "tentar de novo") e vazio.
- Erro ao enviar pedido mantém o carrinho intacto e mostra a mensagem da API.
- Mesa inválida na URL (`/mesa/abc`) mostra uma tela de erro.
- 409 no KDS (outra tela já mudou o status) recarrega a lista.

## 9. Testes
- **Backend (pytest-django):** cálculo do total, cada validação do POST, transições válidas e 409, `/ativos/` filtrando corretamente, consumers do WebSocket recebendo os avisos (`channels.testing.WebsocketCommunicator`).
- **Frontend (Vitest + Testing Library), escritos pelo Gabriel:** reducer do carrinho (testes unitários puros), componente do cartão do KDS (renderização e clique), hook de tempo decorrido (timers falsos).

## 10. Plano de aprendizado (`docs/guia/`)

Cada lição segue o formato: Objetivo · Conceitos · Passo a passo · Como saber se funcionou · Erros comuns · Na entrevista.

| # | Lição | Conceitos de React |
|---|---|---|
| 00 | Ambiente e Docker | Docker, Compose, rodar API e front |
| 01 | Primeiros componentes | JSX, componentes, props, listas e `key`, Tailwind |
| 02 | Buscando o cardápio | TanStack Query (`useQuery`), loading/erro, tipos TS da API |
| 03 | Modal do produto | `useState`, formulários controlados, eventos, estado derivado |
| 04 | Carrinho | Context, `useReducer`, ações, imutabilidade |
| 05 | Enviando o pedido | `useMutation`, React Router (params, navegação) |
| 06 | Tempo real | `useEffect` e limpeza, `useRef`, hook `useWebSocket`, reconexão |
| 07 | KDS | composição de componentes, `setInterval` em hook, áudio, estilos condicionais |
| 08 | Testes | Vitest, Testing Library, testes de reducer e hook |
| 09 | Deploy e portfólio | variáveis de ambiente, build, Vercel, README, currículo |

Ritmo esperado: cerca de uma lição por dia (lições 06 e 07 podem levar dois dias).

## 11. Deploy
- Frontend: Vercel.
- Backend: serviço web no Render rodando Daphne (suporta WebSocket). O plano gratuito "dorme" e a primeira requisição leva cerca de 30 s (documentado no README).
- Banco: PostgreSQL gerenciado gratuito (Render ou Neon). A escolha fica para a lição 09, conferindo os limites dos planos gratuitos nessa data.
