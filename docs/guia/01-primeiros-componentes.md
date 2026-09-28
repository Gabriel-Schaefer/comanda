# Lição 01: Primeiros componentes

## Objetivo

Montar a tela do cardápio com as categorias e os cartões de produto, estilizada com Tailwind e boa de usar no celular. Nesta lição os dados ficam **fixos num arquivo**; a API entra na lição 02.

Resultado esperado (esboço):

```
┌──────────────────────────────┐
│ Comanda                      │
│                              │
│ Lanches                      │
│ ┌──────────────────────────┐ │
│ │ [foto]  X-Burger         │ │
│ │         Pão brioche...   │ │
│ │         R$ 28,90  +extras│ │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ │ [foto]  X-Salada   ...   │ │
│ └──────────────────────────┘ │
│ Porções                      │
│ ...                          │
└──────────────────────────────┘
```

## Conceitos

### Componente

Um componente é **uma função que retorna o que deve aparecer na tela**. O nome começa com letra maiúscula.

```tsx
function Saudacao() {
  return <p>Olá!</p>
}
```

Para usar, você escreve o nome como se fosse uma tag HTML: `<Saudacao />`. A tela inteira é uma árvore de componentes, uns dentro dos outros, como peças de Lego. O `App.tsx` que você já tem é um componente.

### JSX

Aquele "HTML dentro do JavaScript" se chama **JSX**. Parece HTML, mas tem diferenças importantes:

| HTML | JSX | Por quê |
|---|---|---|
| `class="..."` | `className="..."` | `class` é palavra reservada do JavaScript |
| `<img>` | `<img />` | toda tag precisa ser fechada |
| texto fixo | `{expressao}` | chaves inserem qualquer valor JavaScript |

```tsx
const nome = 'Gabriel'
const itens = 3

return (
  <div className="p-4">
    <p>Olá, {nome}!</p>
    <p>Você tem {itens * 2} pontos.</p>
  </div>
)
```

Regra importante: o componente retorna **um único elemento raiz**. Para devolver vários elementos sem criar uma `div` extra, envolva-os em `<>...</>` (chamado *Fragment*).

Comparando com os templates do Django, que você já conhece:

| Django template | JSX |
|---|---|
| `{{ produto.nome }}` | `{produto.nome}` |
| `{% for p in produtos %}...{% endfor %}` | `{produtos.map(p => ...)}` |
| `{% if p.ativo %}...{% endif %}` | `{p.ativo && ...}` |

### Props

**Props** são os parâmetros de um componente. É assim que um componente pai passa dados para o filho. Com TypeScript, você declara o formato das props num tipo:

```tsx
type SaudacaoProps = {
  nome: string
  idade: number
}

function Saudacao({ nome, idade }: SaudacaoProps) {
  return <p>{nome} tem {idade} anos.</p>
}

// uso:
<Saudacao nome="Ana" idade={30} />
```

Repare: texto vai entre aspas (`nome="Ana"`); qualquer outro valor vai entre chaves (`idade={30}`).

Props são **somente leitura**: o filho nunca altera as props que recebeu. Se o dado precisa mudar, quem muda é o pai (isso é assunto da lição 03).

### Listas com `.map()` e a `key`

Para mostrar uma lista, você transforma cada item de um array em um elemento JSX com `.map()`:

```tsx
const frutas = [
  { id: 1, nome: 'Maçã' },
  { id: 2, nome: 'Banana' },
]

return (
  <ul>
    {frutas.map((fruta) => (
      <li key={fruta.id}>{fruta.nome}</li>
    ))}
  </ul>
)
```

A prop `key` é **obrigatória** em listas. Ela é um identificador único e estável de cada item. O React usa a `key` para saber qual item é qual quando a lista muda (item adicionado, removido ou reordenado) e atualizar só o que mudou.

Use o `id` que veio do banco. **Evite o índice do array** (`key={indice}`): se um item for removido do meio da lista, os índices de todos os seguintes mudam, e o React confunde os itens.

### Renderização condicional

Para mostrar algo só em certas condições:

```tsx
{produto.adicionais.length > 0 && <span>+ extras</span>}

{produto.imagem_url ? <img src={produto.imagem_url} alt="" /> : <div>sem foto</div>}
```

- `condicao && <Elemento />`: mostra o elemento só se a condição for verdadeira.
- `condicao ? <A /> : <B />`: escolhe entre dois elementos.

Cuidado com o `&&` e números: `{lista.length && <p>...</p>}` mostra um `0` na tela quando a lista está vazia. Compare explicitamente: `lista.length > 0 && ...`.

### Tailwind CSS em 2 minutos

Em vez de escrever CSS num arquivo separado, você aplica **classes utilitárias** direto no `className`. Cada classe faz uma coisa só:

| Classe | Efeito |
|---|---|
| `p-4`, `px-4`, `py-2` | espaçamento interno (padding) |
| `mt-2`, `mb-4` | espaçamento externo (margin) |
| `text-sm`, `text-xl`, `font-bold` | tamanho e peso do texto |
| `text-stone-600`, `bg-white` | cores de texto e fundo |
| `rounded-lg`, `shadow-sm`, `border` | borda arredondada, sombra, borda |
| `flex`, `gap-3`, `items-center` | layout em linha |
| `grid`, `grid-cols-1`, `md:grid-cols-2` | layout em grade |
| `w-24`, `h-24`, `object-cover` | tamanho e ajuste de imagem |

O prefixo `md:` significa "a partir de telas médias". Então `grid-cols-1 md:grid-cols-2` mostra uma coluna no celular e duas no computador. Esse é o jeito *mobile-first*: você escreve primeiro para o celular e depois ajusta para telas maiores.

Com a extensão **Tailwind CSS IntelliSense** do VS Code, o editor sugere as classes enquanto você digita. Vale instalar.

### Formatando dinheiro

O JavaScript já sabe formatar moeda brasileira:

```ts
new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(28.9)
// "R$ 28,90"
```

### `import type`

Quando você importa **só um tipo** (que existe apenas no TypeScript e some depois de compilado), use `import type`:

```ts
import type { Produto } from '../tipos'
```

O projeto está configurado para exigir isso, e o editor avisa se você esquecer.

## Passo a passo

Crie as pastas conforme precisar. A estrutura ao final desta lição:

```
web/src/
  tipos.ts
  dados/cardapioExemplo.ts
  utils/formatarPreco.ts
  componentes/CartaoProduto.tsx
  componentes/SecaoCategoria.tsx
  paginas/Cardapio.tsx
  App.tsx
```

### 1. Os tipos da API: `src/tipos.ts`

Este arquivo descreve o formato dos dados que a API devolve. Como ele é o "contrato" com o backend, está pronto abaixo. Digite-o (não copie e cole) e tente entender cada linha:

```ts
export type Adicional = { id: number; nome: string; preco: number }

export type Produto = {
  id: number
  nome: string
  descricao: string
  preco: number
  imagem_url: string
  adicionais: Adicional[]
}

export type Categoria = { id: number; nome: string; produtos: Produto[] }

export type StatusPedido = 'NOVO' | 'EM_PREPARO' | 'PRONTO' | 'ENTREGUE'

export type ItemPedido = {
  id: number
  nome_produto: string
  preco_unitario: number
  quantidade: number
  observacao: string
  adicionais: { nome: string; preco: number }[]
}

export type Pedido = {
  id: number
  mesa: number
  status: StatusPedido
  total: number
  criado_em: string
  atualizado_em: string
  itens: ItemPedido[]
}

export type EventoPedido = {
  tipo: 'pedido_criado' | 'pedido_atualizado'
  pedido: Pedido
}
```

Duas coisas novas de TypeScript:
- `Adicional[]` significa "array de Adicional".
- `'NOVO' | 'EM_PREPARO' | ...` é uma **união de literais**: o status só pode ser um desses textos. Se você escrever `'PRONTOO'`, o editor acusa o erro.

Os tipos de pedido (`Pedido`, `EventoPedido`...) só serão usados nas próximas lições. Já estão aqui para o arquivo ficar completo.

### 2. Dados de exemplo: `src/dados/cardapioExemplo.ts`

1. Com a API rodando, abra `http://localhost:8000/api/cardapio/`.
2. Crie o arquivo e exporte uma constante `cardapioExemplo` do tipo `Categoria[]`, colando o JSON como valor. Aqui pode colar: o objetivo não é digitar dados.

```ts
import type { Categoria } from '../tipos'

export const cardapioExemplo: Categoria[] = [ /* cole o JSON aqui */ ]
```

Se algum campo não bater com o tipo, o editor sublinha em vermelho. Isso é o TypeScript conferindo o contrato.

### 3. `src/utils/formatarPreco.ts`

Escreva e exporte uma função `formatarPreco(valor: number): string` que devolve o valor no formato `R$ 28,90`. Use o `Intl.NumberFormat` dos Conceitos.

Dica: crie o formatador **uma vez**, fora da função, e só chame `.format(valor)` dentro dela. Criar o formatador tem custo, e a função vai ser chamada muitas vezes.

### 4. `src/componentes/CartaoProduto.tsx`

Um componente que recebe **um produto** pelas props e mostra:
- à esquerda, a foto: se `imagem_url` estiver vazia, um quadrado cinza (`bg-stone-200`) no lugar;
- o nome, em destaque;
- a descrição, menor e em cinza (as descrições são curtas, mas a classe `line-clamp-2` corta em duas linhas se precisar);
- o preço formatado com `formatarPreco`;
- um selo "+ extras" **só** se o produto tiver adicionais.

Tipo das props: `{ produto: Produto }`. Exporte com `export function CartaoProduto(...)`.

Por enquanto o cartão não é clicável. O clique entra na lição 03.

### 5. `src/componentes/SecaoCategoria.tsx`

Recebe **uma categoria** e mostra:
- o nome da categoria como título (`<h2>`);
- os cartões de todos os produtos dela, com `.map()` e `key={produto.id}`, numa grade de uma coluna no celular e duas em telas médias.

### 6. `src/paginas/Cardapio.tsx`

A página junta tudo:
- um cabeçalho com o título **"Comanda"** num `<h1>` (o teste existente procura por esse título);
- uma `SecaoCategoria` para cada categoria de `cardapioExemplo`, também com `key`.

Deixe o conteúdo com largura máxima e centralizado (`max-w-3xl mx-auto`), para não esticar demais no computador.

### 7. Use a página no `App.tsx`

Troque o conteúdo do `App` para renderizar só `<Cardapio />`.

### 8. Rode o teste

```powershell
cd web
npm run test:run
```

Ele continua passando se o `<h1>Comanda</h1>` estiver na página. Se você mudou o título, ajuste o teste em `App.test.tsx`.

### 9. Commit

Você ainda está dentro da pasta `web` (do passo 8), então o caminho é só `src`:

```powershell
git add src
git commit -m "feat(web): tela do cardápio com dados de exemplo"
```

## Como saber se funcionou

- [ ] Aparecem as 4 categorias e os 9 produtos.
- [ ] Os preços estão no formato `R$ 28,90`.
- [ ] O selo "+ extras" aparece só nos produtos com adicionais (X-Burger sim, Água Mineral não).
- [ ] Nenhum aviso sobre `key` no console do navegador (F12 → Console).
- [ ] No modo celular do DevTools (F12 → ícone de celular, ou `Ctrl+Shift+M`), com largura de 375 px, tudo fica legível e sem rolagem para os lados.
- [ ] `npm run test:run` passa, e `npm run build` termina sem erros de tipo.

## Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Aviso `Each child in a list should have a unique "key" prop` | Faltou `key` no elemento de dentro do `.map()` | Coloque `key={item.id}` no elemento mais externo retornado pelo `.map()` |
| Nada aparece, sem erro | `.map()` com chaves `{}` e sem `return` | Use `map((p) => ( ... ))` com parênteses, ou escreva `return` dentro das chaves |
| Estilo não aplica | Escreveu `class` em vez de `className` | Troque por `className` |
| Erro `is a type and must be imported using a type-only import` | Importou tipo sem `import type` | Use `import type { Produto } from ...` |
| Aparece um `0` solto na tela | `lista.length && ...` com lista vazia | Use `lista.length > 0 && ...` |
| `Cannot find module '../tipos'` | Caminho relativo errado | Confira quantos `../` precisa a partir da pasta do arquivo |

## Na entrevista

**"O que são props?"**
São os dados que um componente pai passa para um componente filho, como parâmetros de uma função. São somente leitura: o filho não altera as props. Para mudar um dado, o pai muda o próprio estado e o React renderiza o filho de novo com as props novas. Isso é o fluxo de dados de mão única do React.

**"Por que o React pede `key` em listas, e por que não usar o índice?"**
A `key` identifica cada item entre uma renderização e outra, para o React atualizar só o que mudou em vez de recriar a lista inteira. O índice muda quando itens são inseridos, removidos ou reordenados, e aí o React associa o estado de um item ao item errado. Por exemplo, um campo de texto digitado "pula" para a linha de baixo. Por isso uso um id estável, como o do banco.

**"Qual a diferença entre componente e elemento?"**
O componente é a função (a "receita"), como `CartaoProduto`. O elemento é o que a função retorna ou o que você escreve no JSX, como `<CartaoProduto produto={p} />`: um objeto que descreve o que deve aparecer na tela. O React usa os elementos para montar e atualizar a página.

**"O que é JSX e o que ele vira depois de compilado?"**
É uma sintaxe parecida com HTML dentro do JavaScript. Ela não roda no navegador: o compilador (aqui, o Vite) transforma cada tag numa chamada de função que cria elementos, algo como `jsx('p', { children: 'Olá' })`. Por isso dá para usar qualquer expressão JavaScript entre chaves.

**"Por que usar TypeScript no frontend?"**
Porque ele descreve o formato dos dados e acusa erros antes de rodar: um campo com o nome errado, um status que não existe, uma prop esquecida. No meu projeto os tipos espelham a resposta da API; se o backend mudar um campo, o editor mostra todos os lugares do front que precisam de ajuste.
