# Tutorial GEM5 — Coerência de Cache com Ruby

## Introdução
Ruby é o subsistema detalhado de memória do gem5. Ele permite modelar protocolos de coerência, controladores, redes e diretórios para estudar compartilhamento de dados em máquinas multicore.

## Objetivo
Executar um programa paralelo com dois protocolos Ruby disponíveis na instalação e analisar o custo de coerência causado por dados compartilhados.

## Pré-requisitos
- gem5 compilado para a ISA escolhida;
- suporte Ruby habilitado no build;
- um binário multithread compilado para a ISA alvo;
- conhecimento básico de modo SE e API Python.

## Conceitos
Em caches privados, diferentes núcleos podem guardar cópias da mesma linha. O protocolo de coerência mantém essas cópias consistentes. Escritas em uma linha compartilhada podem gerar invalidações, requisições ao diretório e mensagens de rede.

## Prática

### Etapa 1 — Localizar protocolos e exemplos

```bash
find configs -type f | grep -Ei 'ruby|mesi|moesi'
find src/mem/ruby -maxdepth 3 -type d | head -40
```

Use somente protocolos que estejam presentes na sua árvore. Nomes comuns incluem variantes MESI, MOESI e protocolos para topologias específicas, mas a disponibilidade varia por versão.

### Etapa 2 — Criar a carga paralela
Crie `contador_compartilhado.c`:

```c
#include <pthread.h>
#include <stdio.h>
#define N 100000
long contador = 0;
void *trabalhar(void *arg) {
    for (long i = 0; i < N; i++) __atomic_fetch_add(&contador, 1, __ATOMIC_RELAXED);
    return NULL;
}
int main(void) {
    pthread_t a, b;
    pthread_create(&a, NULL, trabalhar, NULL);
    pthread_create(&b, NULL, trabalhar, NULL);
    pthread_join(a, NULL); pthread_join(b, NULL);
    printf("contador = %ld\n", contador);
    return contador != 2L * N;
}
```

Compile para a ISA alvo. Para x86 em um hospedeiro x86:

```bash
gcc -O2 -pthread contador_compartilhado.c -o contador_compartilhado
```

### Etapa 3 — Executar uma referência sem Ruby
Use a configuração SE já validada para produzir uma referência funcional. Registre núcleos, caches e comando.

### Etapa 4 — Adaptar uma configuração Ruby SE
Copie um exemplo Ruby SE fornecido pela sua versão e configure:

- `num_cpus = 2`;
- o binário `contador_compartilhado` em ambos os contextos necessários;
- caches privados e diretório conforme o protocolo;
- uma topologia de rede definida pelo exemplo.

Evite montar controladores Ruby manualmente no primeiro experimento: use o script oficial como base, pois a ligação entre sequenciadores, portas e rede depende do protocolo.

### Etapa 5 — Executar protocolos comparáveis

```bash
mkdir -p resultados/ruby/protocolo_a resultados/ruby/protocolo_b
build/X86/gem5.opt configs/exemplo_ruby_se.py \
  --outdir=resultados/ruby/protocolo_a --num-cpus=2 \
  --cmd=./contador_compartilhado --protocol=<ProtocoloA>
```

Repita com `<ProtocoloB>`, preservando processador, frequência, tamanho de cache, topologia e carga. Caso o protocolo seja selecionado no build ou no script, siga a interface do exemplo.

### Etapa 6 — Extrair estatísticas

```bash
grep -Ei 'simSeconds|simTicks|Ruby|directory|request|response|inv|cache' \
  resultados/ruby/protocolo_a/stats.txt | head -120
```

Observe principalmente miss de caches, transações do diretório, invalidações, mensagens de rede e latência, conforme os contadores expostos.

## Análise
Compare tempo total e tráfego de coerência. Um protocolo com mais mensagens não é necessariamente pior: o resultado depende do padrão de escrita, compartilhamento e topologia. Para distinguir custo de coerência de custo computacional, crie uma versão em que cada thread atualiza um contador privado e compare-a à versão compartilhada.

## Boas práticas
- Valide que `contador = 200000` é impresso.
- Não compare protocolos com tamanhos de cache ou redes diferentes.
- Documente protocolo, topologia e número de controladores.

## Exercícios
1. Aumente o número de threads e núcleos para quatro.
2. Compare contador compartilhado versus contadores privados.
3. Discuta a relação entre invalidações, tempo e escalabilidade.