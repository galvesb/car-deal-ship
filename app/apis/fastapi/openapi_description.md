Bem-vindo(a) ao guia de referência para a API de cardealship da Plataforma Seller.

# Objetivo

O propósito é viabilizar a definição e evolução do processo de _cardealship_ (ou qualquer outro processo da organização)
garantindo a sua execução, controle e consistência.

# Manipulação de Datas/Horas

Em nossas requisições e respostas, se um determinado valor for do tipo data (_date_); então, o mesmo será representado como
uma `string`.

## Formato

Todas as datas retornadas estarão no formato [ISO-8601-1](https://pt.wikipedia.org/wiki/ISO_8601) com fuso
horário UTC, e precisão de milissegundos.

|Formato | `YYYY-MM-DDThh:mm:ss.mmmZ` |
|--------|----------------------------|
|Exemplo | `2022-12-31T23:59:59.999`  |

# Referências

- [PMU - APIs Rest](https://magazine.atlassian.net/wiki/spaces/Maganets/pages/1541505043/PMU+-+APIs+Rest)
- [Design Doc](https://magazine.atlassian.net/wiki/spaces/Maganets/pages/2870772133/Design+Doc+-+cardealship+Plataforma+Seller)