# Tutorial GEM5 — Virtualização em Full System

## Introdução
Virtualização requer suporte da ISA, do kernel e do hypervisor. O gem5 pode ser usado para investigar plataformas que executam sistemas completos, mas a viabilidade de um experimento de virtualização depende estritamente dos recursos modelados pela ISA e pela versão instalada.

## Objetivo
Validar uma plataforma FS capaz de iniciar um hypervisor e medir o custo de uma carga simples em execução nativa e virtualizada, quando o suporte estiver disponível.

## Pré-requisitos
- build FS para uma ISA com extensões de virtualização suportadas pela configuração escolhida;
- kernel, imagem de disco e hypervisor compatíveis;
- uma carga de usuário pequena dentro da imagem;
- tempo de simulação e armazenamento suficientes.

> **Importante:** não presuma suporte completo a KVM, Xen, QEMU ou a todas as extensões de virtualização. Confirme a compatibilidade na documentação da sua versão e nos exemplos existentes antes de iniciar a campanha.

## Conceitos
O hypervisor cria uma camada adicional entre sistema operacional convidado e hardware. O custo pode incluir transições de privilégio, emulação de dispositivos, gerenciamento de memória e interrupções. Uma comparação correta exige que a mesma carga e recursos sejam usados nos dois cenários.

## Prática

### Etapa 1 — Verificar suporte

```bash
find configs src -type f | grep -Ei 'virt|virtual|kvm|xen' | head -80
```

Consulte também a documentação da plataforma. Se não houver uma configuração oficialmente suportada, trate o objetivo como estudo de viabilidade, não como experimento pronto.

### Etapa 2 — Validar o sistema nativo
Inicialize uma imagem FS sem hypervisor e execute uma carga, por exemplo `sha256sum` sobre um arquivo de tamanho fixo. O script de inicialização deve registrar o resultado e terminar a simulação com `m5 exit`.

```sh
sha256sum /dados/entrada.bin > /tmp/hash.txt
m5 exit
```

### Etapa 3 — Preparar o cenário virtualizado
Parta da imagem nativa validada. Instale ou habilite o hypervisor e prepare o convidado. Use a mesma carga, arquivo de entrada, número de vCPUs e limites de memória. Registre versões do kernel e do hypervisor.

### Etapa 4 — Criar dois scripts de inicialização
- **Nativo:** executa a carga diretamente no SO hospedeiro.
- **Virtualizado:** inicializa o convidado, executa a mesma carga nele e sinaliza término de forma controlada.

Defina um critério inequívoco de fim; iniciar o hypervisor não é suficiente para comprovar que a carga foi executada.

### Etapa 5 — Executar

```bash
for cenario in nativo virtualizado; do
  build/<ISA>/gem5.opt configs/plataforma_fs.py \
    --outdir="resultados/virtualizacao/${cenario}" \
    --disk-image="${cenario}.img" --kernel=vmlinux
 done
```

Substitua `<ISA>` e os argumentos pela configuração validada.

### Etapa 6 — Coletar métricas

```bash
grep -Ei 'simSeconds|simTicks|numCycles|ipc|cpi|interrupt|tlb' \
  resultados/virtualizacao/nativo/stats.txt | head -120
```

Verifique também os logs de console para confirmar a conclusão e a igualdade do resultado do `sha256sum`.

## Análise
Estime o overhead:

\[
Overhead(\%)=100\times\frac{T_{virtualizado}-T_{nativo}}{T_{nativo}}
\]

Atribua diferenças apenas a virtualização depois de conferir que imagens, carga, frequência, memória e condição de término são equivalentes. Boot e inicialização podem dominar execuções curtas; se o foco for a carga, use checkpoints após o boot ou cargas suficientemente longas.

## Boas práticas
- Não interprete uma falha de boot como resultado de desempenho.
- Armazene logs de console junto a cada `stats.txt`.
- Execute mais de uma entrada para reduzir conclusões dependentes de um único caso.

## Exercícios
1. Compare duas durações de carga.
2. Meça o impacto de uma carga de E/S, se os dispositivos forem suportados.
3. Separe tempo de boot e tempo da aplicação com checkpoints.