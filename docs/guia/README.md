# Guia de aprendizado: React construindo o Comanda

Você vai aprender React construindo o frontend de um sistema de pedidos de verdade. O backend (Django) já está pronto e testado, então toda a sua energia vai para o React.

## Como usar

1. Faça **uma lição por dia**, na ordem. As lições 06 e 07 podem levar dois dias.
2. Leia a lição inteira antes de começar a programar.
3. **Digite o código você mesmo.** Não copie e cole os trechos de exemplo: digitar faz memorizar, e errar a digitação ensina a ler mensagens de erro.
4. Quando terminar, avise o Claude. Ele revisa o seu código e explica o que melhorar e por quê.
5. Faça os ajustes e **faça o commit você mesmo**. O código é seu, e o histórico do GitHub mostra isso.
6. No fim de cada lição há perguntas de entrevista. Tente responder em voz alta antes de ler a resposta.

A próxima lição é escrita depois que você termina a anterior, partindo do código que você escreveu.

## As lições

| # | Lição | O que você aprende |
|---|---|---|
| 00 | [Ambiente e Docker](00-ambiente.md) | Docker, Compose, rodar a API e o front |
| 01 | [Primeiros componentes](01-primeiros-componentes.md) | JSX, componentes, props, listas e `key`, Tailwind |
| 02 | Buscando o cardápio | TanStack Query (`useQuery`), carregando/erro, tipos da API |
| 03 | Modal do produto | `useState`, formulários controlados, eventos, estado derivado |
| 04 | Carrinho | Context, `useReducer`, ações, imutabilidade |
| 05 | Enviando o pedido | `useMutation`, React Router (parâmetros, navegação) |
| 06 | Tempo real | `useEffect` e limpeza, `useRef`, hook `useWebSocket`, reconexão |
| 07 | KDS | composição de componentes, `setInterval` em hook, áudio, estilos condicionais |
| 08 | Testes | Vitest, Testing Library, testes de reducer e de hook |
| 09 | Deploy e portfólio | variáveis de ambiente, build, Vercel, README, currículo |

## Formato de cada lição

- **Objetivo:** o que você vai construir.
- **Conceitos:** a teoria necessária, do zero, com exemplos pequenos.
- **Passo a passo:** o que fazer, em ordem. O código dos componentes é seu; os exemplos só mostram sintaxe nova.
- **Como saber se funcionou:** o que testar.
- **Erros comuns:** o que costuma dar errado e como resolver.
- **Na entrevista:** perguntas que caem sobre o assunto, com respostas explicadas.
