# Tutorial GEM5 — Interconexão Multicore e NoC

## Introdução
Em sistemas multicore, a interconexão transporta requisições entre núcleos, caches, diretórios e memória. Quando Ruby é usado, a rede on-chip pode ser modelada com maior detalhe, permitindo estudar latência, tráfego e congestionamento.

## Objetivo
Comparar duas topologias de rede disponíveis na instalação do gem5 usando uma carga paralela que compartilha dados.

## Pré-requisitos
- suporte Ruby funcional;
- binário multithread para a ISA simulada;
- exemplo Ruby SE compatível com topologias de rede.

## Conceitos
Uma topologia determina como roteadores e controladores são conectados. Redes simples podem reduzir o número de saltos em sistemas pequenos; uma malha (*mesh*) tende a escalar melhor fisicamente. A métrica central não é apenas tempo: também são relevantes hops, latência de rede e utilização dos enlaces.

## Prática

### Etapa 1 — Descobrir topologias suportadas

```bash
find configs src/mem/ruby -iname '*topology*' -o -iname '*mesh*' -o -iname '*crossbar*'
```

Anote os nomes aceitos pelo script de referência. Não assuma que todas as topologias existem na sua versão.

### Etapa 2 — Usar uma carga com comunicação
Use o programa `contador_compartilhado` do tutorial de coerência ou uma aplicação paralela com barreiras. A carga deve executar corretamente com quatro threads.

### Etapa 3 — Preparar a configuração
Parta do exemplo Ruby SE e defina quatro CPUs. Fixe protocolo, frequência, cache, memória e entrada. Deixe apenas a topologia variar.

Exemplo de argumentos, sujeitos à interface do script:

```bash
--num-cpus=4 --network=<rede> --topology=<topologia>
```

### Etapa 4 — Executar duas topologias

```bash
for topo in Crossbar Mesh_XY; do
  dir="resultados/noc/${topo}"
  mkdir -p "$dir"
  build/X86/gem5.opt configs/exemplo_ruby_se.py \
    --outdir="$dir" --num-cpus=4 --topology="$topo" \
    --cmd=./contador_compartilhado
done
```

Substitua os nomes pelo conjunto confirmado na Etapa 1.

### Etapa 5 — Coletar os dados

```bash
grep -Ei 'simSeconds|network|link|router|hop|latency|util' \
  resultados/noc/Mesh_XY/stats.txt | head -150
```

Crie uma tabela:

| Topologia | Tempo | Latência média | Hops médios | Utilização máxima |
|---|---:|---:|---:|---:|
| Crossbar | | | | |
| Mesh | | | | |

Os nomes das estatísticas de rede são específicos do modelo.

## Análise
Uma rede mesh pode apresentar mais hops médios que uma crossbar, especialmente em poucos nós, mas representa uma organização mais escalável. Se a utilização máxima de certos enlaces for alta e a latência aumentar com a carga, há indícios de congestionamento. Repita com 2, 4 e 8 núcleos, mantendo a carga por núcleo controlada.

## Boas práticas
- Compare topologias com o mesmo mapeamento de controladores quando possível.
- Valide a dimensão da mesh para o número de nós.
- Separe resultados de aplicações computacionais e aplicações intensivas em comunicação.

## Exercícios
1. Execute uma campanha com 2, 4 e 8 núcleos.
2. Compare uma entrada pequena e outra grande.
3. Relacione utilização de enlaces e tempo simulado.