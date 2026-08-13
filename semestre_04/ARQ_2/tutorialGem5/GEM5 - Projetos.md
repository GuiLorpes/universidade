# Trabalhos de Arquitetura de Computadores: extensões do gem5

## Finalidade

Este catálogo propõe **36 trabalhos práticos**, distribuídos pelos seis tópicos da disciplina. Cada proposta exige alterar o código-fonte do gem5 ou acrescentar um componente, uma política, uma métrica ou um mecanismo novo — não apenas executar configurações já existentes.

O público é formado por estudantes do segundo ano de Ciência da Computação que dominam Python, C e C++. Cada tema foi delimitado para ser realizável por uma dupla ou trio em aproximadamente **três meses**, incluindo estudo do código, implementação, testes, experimentos e relatório.

## Regras gerais sugeridas

- A entrega deve conter *fork* ou repositório com *commits*, instruções de compilação e execução, código documentado e pelo menos um script Python de configuração.
- O grupo deve criar um microbenchmark em C/C++ quando ele for necessário para evidenciar o mecanismo implementado.
- Toda proposta deve ser comparada contra uma **linha de base**: a versão original do gem5 ou uma política padrão equivalente.
- Os experimentos devem ser reprodutíveis: informar versão/commit do gem5, ISA, modelo de CPU, frequência, caches, memória, *workload*, número de repetições e comandos.
- O relatório deve separar corretamente: desempenho do programa simulado, estatísticas microarquiteturais e custo de simulação no hospedeiro.
- Recomenda-se começar em modo **SE** e com `build/X86/gem5.opt` ou `build/ARM/gem5.opt`. Trabalhos que usam Ruby ou GPU podem exigir uma configuração e compilação específicas.

## Critérios transversais de avaliação sugeridos

| Critério | Peso sugerido |
|---|---:|
| Correção e integração da funcionalidade ao gem5 | 35% |
| Qualidade de engenharia: organização, testes e documentação | 20% |
| Metodologia experimental e reprodutibilidade | 25% |
| Análise crítica dos resultados e apresentação | 20% |

---

# 1. Arquiteturas paralelas

## 1. Escalonador de tarefas *work-stealing* simplificado

**Objetivo.** Estudar balanceamento de carga em aplicações paralelas irregulares.

**O que implementar.** Criar, no ambiente de execução de um benchmark C/C++, uma biblioteca de tarefas com filas por *thread* e roubo de tarefas. Adicionar ao script Python do gem5 contadores de tarefas executadas por núcleo, tentativas de roubo e roubos bem-sucedidos. A biblioteca deve oferecer também uma política estática de referência.

**Como avaliar a implementação.** Executar busca em árvore, processamento de filas com tamanhos heterogêneos ou cálculo de fractal particionado em blocos com custos variáveis, usando 2, 4 e 8 núcleos. Comparar tempo simulado, desequilíbrio (máximo/média de tarefas por núcleo), IPC, faltas de cache e número de roubos entre divisão estática e *work-stealing*.

## 2. Barreira adaptativa por disseminação

**Objetivo.** Comparar o custo de diferentes algoritmos de sincronização coletiva.

**O que implementar.** Implementar em C/C++ uma barreira por disseminação (*dissemination barrier*) e uma barreira centralizada, utilizando atômicos. Acrescentar um objeto de estatísticas no gem5 ou instrumentação no script para registrar quantas barreiras foram alcançadas e o tempo entre chegadas, usando marcas de pseudo-instruções ou regiões de simulação.

**Como avaliar a implementação.** Usar um programa iterativo de relaxação de grade ou integração numérica paralela, variando número de *threads* e trabalho entre barreiras. Medir tempo por iteração, escalabilidade, acessos atômicos e tráfego de coerência. Discutir quando a barreira centralizada deixa de escalar.

## 3. Política de afinidade de *threads* orientada à localidade

**Objetivo.** Explorar como o mapeamento de *threads* em núcleos influencia caches e comunicação.

**O que implementar.** Estender um script de configuração multiprocessada para aceitar políticas de fixação: compacta, espalhada e definida por mapa. Desenvolver uma pequena biblioteca de *pinning* para o workload ou configurar afinidade por processo. Criar estatísticas que associem cada *thread* ao núcleo utilizado e consolidem métricas por núcleo.

**Como avaliar a implementação.** Rodar uma multiplicação de blocos, uma redução paralela e uma aplicação com comunicação entre vizinhos. Comparar 4 e 8 núcleos, medindo tempo simulado, IPC por núcleo, faltas privadas/compartilhadas e desvio padrão do trabalho concluído.

## 4. Fila de trabalho com *backoff* exponencial

**Objetivo.** Reduzir a pressão na memória causada por espera ativa em filas concorrentes.

**O que implementar.** Criar uma fila produtora-consumidora baseada em atômicos com três modos de espera: laço ocupado simples, pausa fixa e *backoff* exponencial. Incluir uma opção no script Python para selecionar o modo e contadores de tentativas de acesso, operações bem-sucedidas e períodos de espera.

**Como avaliar a implementação.** Simular 1–4 produtores e 1–4 consumidores com cargas de produção e consumo controláveis. Medir vazão, tempo de conclusão, acessos à linha de controle da fila, invalidações de cache e justiça entre consumidores. Verificar se o *backoff* melhora cenários com alta contenção sem degradar demasiadamente baixa contenção.

## 5. Detector de desequilíbrio de carga por núcleo

**Objetivo.** Criar observabilidade para identificar paralelismo ineficiente.

**O que implementar.** Adicionar um `SimObject` de estatísticas periódicas que colete, por núcleo, instruções comprometidas, ciclos ociosos e amostras de ocupação em intervalos configuráveis. O objeto deve exportar métricas como IPC médio, máximo, mínimo e coeficiente de variação ao fim da simulação.

**Como avaliar a implementação.** Validar o detector em dois programas: um com divisão uniforme de trabalho e outro deliberadamente desbalanceado. Comparar os indicadores produzidos com a distribuição conhecida de trabalho. Demonstrar o efeito de corrigir o particionamento do segundo programa.

## 6. Redução paralela em árvore com granularidade configurável

**Objetivo.** Investigar o compromisso entre paralelismo, sincronização e localidade.

**O que implementar.** Implementar uma redução de vetor em árvore, com tamanho de bloco configurável e combinação final por etapas. Incluir uma alternativa de contador global atômico. Acrescentar ao script parâmetros para tamanho do problema, blocos e número de *threads*.

**Como avaliar a implementação.** Variar tamanho do vetor, blocos e número de núcleos. Comparar redução em árvore e contador atômico por tempo, aceleração, número de operações atômicas, miss rate de L1/L2 e tráfego de coerência. Identificar uma granularidade próxima do melhor resultado para cada sistema.

---

# 2. Topologias e interconexão

## 7. Topologia em anel bidirecional para Ruby

**Objetivo.** Implementar e estudar uma topologia simples de rede em chip.

**O que implementar.** Criar uma topologia Ruby baseada em anel bidirecional: ligar roteadores em dois sentidos, associar controladores a roteadores e selecionar pesos ou latências coerentes com a distância. Expor parâmetros para número de nós e latência do enlace.

**Como avaliar a implementação.** Comparar anel com malha 2D de mesmo número de nós (4, 8 e 16, quando viável), usando microbenchmarks com compartilhamento e um programa paralelo. Medir latência média da rede, número médio de saltos, ocupação de enlaces, tempo de execução e escalabilidade.

## 8. Topologia *fat-tree* compacta

**Objetivo.** Explorar uma interconexão hierárquica com maior largura de banda próxima à raiz.

**O que implementar.** Adicionar uma topologia Ruby *fat-tree* para 4, 8 ou 16 controladores. Construir níveis de roteadores e enlaces com largura de banda ou número de enlaces maior nos níveis superiores. Documentar as restrições de número de nós aceitas.

**Como avaliar a implementação.** Comparar *fat-tree*, anel e mesh em tráfego uniforme e em um benchmark de compartilhamento de dados. Coletar latência de pacotes, utilização dos enlaces, contenção e desempenho. Avaliar se o benefício da árvore compensa seu maior número de enlaces.

## 9. Roteamento adaptativo mínimo alternativo

**Objetivo.** Reduzir contenção escolhendo entre múltiplos caminhos mínimos.

**O que implementar.** Em uma mesh 2D, modificar a seleção de rota para que, quando houver duas direções mínimas possíveis, a decisão considere ocupação de fila ou número de créditos disponíveis. Manter o algoritmo determinístico XY como opção de referência e preservar ausência de *deadlock*.

**Como avaliar a implementação.** Executar padrões sintéticos de tráfego (uniforme, transposição e *hotspot*) e um workload paralelo. Medir latência média e percentis, vazão saturada, ocupação de buffers e entrega de pacotes. Mostrar casos em que a adaptação ajuda e casos em que ela não ajuda.

## 10. Roteador com prioridade para mensagens críticas

**Objetivo.** Dar tratamento preferencial a classes de tráfego com maior sensibilidade à latência.

**O que implementar.** Estender a arbitragem de saída de um roteador para reconhecer duas classes de mensagem: normal e prioritária. Adicionar parâmetro de ativação, contadores por classe e um mecanismo simples contra inanição, como cota máxima consecutiva de pacotes prioritários.

**Como avaliar a implementação.** Gerar uma mistura de tráfego de baixa latência e tráfego de fundo intensivo. Comparar arbitragem original e prioritária por latência média/p95 de cada classe, vazão total e justiça. Verificar se a classe normal ainda progride.

## 11. Controle de admissão em injeção de pacotes

**Objetivo.** Limitar congestionamento antes que ele se propague pela rede.

**O que implementar.** Adicionar um limite configurável para injeção quando a ocupação da fila local ultrapassar um limiar. Implementar políticas fixa e adaptativa, acompanhadas de estatísticas de pacotes atrasados no injetor e taxa de injeção efetiva.

**Como avaliar a implementação.** Sob tráfego sintético crescente, construir curvas de latência versus carga oferecida. Comparar sem controle, limiar fixo e adaptativo. Reportar ponto de saturação, latência p99 e impacto na vazão.

## 12. Mapeamento consciente de topologia para controladores

**Objetivo.** Aproximar núcleos que se comunicam frequentemente.

**O que implementar.** Criar no script Python um mapeador que recebe uma matriz simples de comunicação entre *threads* ou núcleos e gera a associação desses núcleos aos roteadores de uma mesh. Implementar políticas aleatória, linear e gulosa baseada em maior volume de comunicação.

**Como avaliar a implementação.** Usar comunicação em vizinhança e padrões com dois grupos intensamente comunicantes. Comparar distância média ponderada, número de saltos, latência de rede e tempo da aplicação. Confirmar que a política gulosa não piora excessivamente tráfego uniforme.

---

# 3. Coerência de cache e protocolos

## 13. Estado exclusivo em um protocolo MESI didático

**Objetivo.** Compreender o ganho de evitar invalidação desnecessária antes de uma escrita privada.

**O que implementar.** Partindo de uma configuração Ruby compatível ou de um protocolo educacional, introduzir/ativar o estado `E` (Exclusive) e suas transições principais: leitura sem compartilhadores, escrita em `E` sem mensagem adicional e transição para `S` quando outro núcleo lê a linha. Registrar transições por estado.

**Como avaliar a implementação.** Criar microbenchmarks de inicialização privada, leitura compartilhada e escrita após leitura. Comparar versão sem `E` e MESI por número de mensagens, invalidações, latência de escrita e tempo total. Validar os estados pela depuração de um caso pequeno.

## 14. Contador de mensagens de coerência por causa

**Objetivo.** Tornar mensurável o custo de leituras, invalidações, *writebacks* e respostas de dados.

**O que implementar.** Estender controladores Ruby para classificar e contabilizar mensagens por tipo e origem: pedido de leitura, pedido de escrita, invalidação, reconhecimento, resposta de dados e *writeback*. Exportar estatísticas globais e por controlador.

**Como avaliar a implementação.** Executar workloads de dados privados, dados somente leitura, verdadeira compartilhação e falsa compartilhação. Verificar se o perfil de mensagens coincide com a expectativa de cada padrão. Apresentar mensagens por mil instruções e por operação de sincronização.

## 15. Detector de falsa compartilhação baseado em escrita

**Objetivo.** Identificar linhas que causam invalidações frequentes, embora contenham dados logicamente independentes.

**O que implementar.** Adicionar uma tabela limitada por conjunto associativo nos controladores de cache para registrar, por linha, escritores recentes e número de transferências de posse entre núcleos. Ao ultrapassar um limiar, registrar a linha como candidata a falsa compartilhação. A tabela deve possuir política de substituição simples.

**Como avaliar a implementação.** Validar com dois microbenchmarks: contadores adjacentes em uma mesma linha e contadores separados por *padding*. Medir candidatos detectados, invalidações, transferências de posse e tempo. Verificar falsos positivos em uma carga de verdadeira compartilhação.

## 16. Coerência seletiva para região somente leitura

**Objetivo.** Reduzir mensagens de coerência em dados que não serão modificados durante uma fase.

**O que implementar.** Criar uma pseudo-instrução ou marca de região no workload e um mecanismo no controlador que registre páginas/intervalos como somente leitura durante a região. Escritas devem gerar aviso ou retornar ao tratamento normal. A implementação pode ser limitada a uma tabela de intervalos configurável.

**Como avaliar a implementação.** Usar uma estrutura grande compartilhada para consultas e uma fase posterior de atualização. Comparar modo normal e marcado por número de mensagens de coerência, miss rate, tempo e correção do resultado. Explicitar as limitações: o mecanismo não substitui proteção de memória real.

## 17. Diretório esparso com limite de compartilhadores

**Objetivo.** Estudar o custo de armazenamento de diretórios e o tratamento de linhas muito compartilhadas.

**O que implementar.** Criar uma representação de diretório que armazene até `k` identificadores de compartilhadores por linha. Quando o limite for excedido, usar um estado de difusão (*broadcast*) ou um bit de “muitos compartilhadores”. Expor `k` como parâmetro e manter contadores de transições para esse estado.

**Como avaliar a implementação.** Rodar leitura compartilhada com 2, 4 e 8 núcleos e uma carga mista de leitura/escrita. Comparar diferentes valores de `k` por armazenamento estimado, mensagens de coerência, latência e desempenho. Discutir o equilíbrio entre precisão e custo.

## 18. Política de invalidação preguiçosa em região de sincronização

**Objetivo.** Investigar o adiamento de invalidações até pontos de sincronização bem definidos.

**O que implementar.** Em um protocolo didático restrito, marcar linhas modificadas como potencialmente obsoletas em outros caches e aplicar invalidações ao atingir uma barreira explicitamente marcada. O mecanismo deve permanecer opcional e ser usado somente em microbenchmarks com fases bem delimitadas.

**Como avaliar a implementação.** Usar uma aplicação de fases “produz–barreira–consome”. Comparar invalidação imediata e preguiçosa por mensagens, tempo de barreira, tempo total e consistência dos resultados. O relatório deve explicar claramente em quais programas a técnica seria insegura sem garantias adicionais.

---

# 4. Computadores multinúcleo

## 19. Cache L2 compartilhada com particionamento estático por núcleo

**Objetivo.** Reduzir interferência entre aplicações concorrentes em uma cache compartilhada.

**O que implementar.** Alterar a política de alocação/substituição de uma cache compartilhada para reservar uma quantidade configurável de conjuntos, vias ou cotas por núcleo. Quando a cota do núcleo estiver cheia, a vítima deve preferencialmente pertencer ao mesmo núcleo. Registrar ocupação e despejos por solicitante.

**Como avaliar a implementação.** Executar simultaneamente uma aplicação com grande *working set* e outra sensível a cache. Comparar cache compartilhada convencional e particionada por miss rate por núcleo, IPC, *slowdown* relativo à execução isolada e justiça.

## 20. Particionamento dinâmico de vias da LLC

**Objetivo.** Adaptar a divisão da última cache ao comportamento recente das aplicações.

**O que implementar.** Adicionar um controlador periódico que lê contadores de faltas por núcleo e ajusta cotas de vias dentro de limites mínimo e máximo. A política pode transferir uma via por período da aplicação com menor benefício marginal para a de maior taxa de faltas. Começar por uma versão com dois núcleos.

**Como avaliar a implementação.** Avaliar pares de workloads de pressão distinta sobre cache, comparando particionamento igual, sem partição e dinâmico. Medir misses, IPC, tempo, número de realocações e justiça. Mostrar a evolução das cotas ao longo do tempo.

## 21. Monitor de interferência entre núcleos

**Objetivo.** Identificar quando a execução conjunta prejudica uma aplicação além do esperado.

**O que implementar.** Criar estatísticas de execução isolada e coexecução, ou uma estimativa baseada em amostras de ocupação e faltas de cache. Produzir, ao fim, um indicador de interferência por núcleo, como o aumento relativo de MPKI ou a redução de IPC.

**Como avaliar a implementação.** Executar cada workload sozinho e em pares. Testar combinações memória-intensiva/memória-intensiva, CPU-intensiva/CPU-intensiva e mista. Comparar a classificação produzida pelo monitor com o *slowdown* real observado na coexecução.

## 22. Política de escalonamento por intensidade de memória

**Objetivo.** Evitar coexecutar tarefas que disputam fortemente a hierarquia de memória.

**O que implementar.** Construir um escalonador em nível de experimentação que mede MPKI de uma fase curta e combina tarefas em núcleos conforme uma regra: misturar uma tarefa intensiva em memória com uma intensiva em CPU. O script Python deve automatizar a classificação e a escolha de pares.

**Como avaliar a implementação.** Usar pelo menos quatro workloads com perfis distintos e comparar pareamento aleatório, pior pareamento e pareamento consciente. Reportar tempo de lote, *slowdown* de cada tarefa, MPKI e utilização dos núcleos.

## 23. Prefetcher cooperativo para cache compartilhada

**Objetivo.** Diminuir faltas de dados de fluxo sem poluir excessivamente a LLC.

**O que implementar.** Implementar um prefetcher de *stride* simples na cache compartilhada, com uma pequena tabela indexada por PC ou fluxo de acesso. Incluir limiar de confiança, distância de prefetch configurável e contadores de prefetches emitidos, úteis, inúteis e tardios.

**Como avaliar a implementação.** Rodar um programa de varredura de matrizes e um workload com acesso irregular. Variar distância e limiar de confiança. Comparar MPKI, tempo, largura de banda de memória e precisão/cobertura do prefetcher. Demonstrar um caso de poluição.

## 24. Regulador de largura de banda por núcleo

**Objetivo.** Evitar que um núcleo monopolize o controlador de memória.

**O que implementar.** Adicionar um mecanismo de orçamento de requisições de memória por núcleo em janelas de tempo. Ao esgotar o orçamento, atrasar requisições não críticas até a próxima janela. Implementar modo desligado, cotas iguais e cotas configuráveis.

**Como avaliar a implementação.** Coexecutar uma aplicação de fluxo de memória com uma aplicação sensível à latência. Comparar vazão, latência das requisições, IPC e justiça entre sem regulador e diferentes cotas. Discutir o custo imposto ao aplicativo de maior consumo.

---

# 5. Paralelismo de dados e processadores vetoriais

## 25. Unidade funcional vetorial de soma inteira didática

**Objetivo.** Introduzir a modelagem de execução SIMD dentro do processador.

**O que implementar.** Estender uma ISA/modelo escolhido com uma instrução vetorial educacional de soma de elementos inteiros, ou modelar uma unidade funcional que execute uma operação vetorial já decodificada. A operação deve ter largura configurável (por exemplo, 2, 4 ou 8 elementos) e latência documentada. Fornecer um microbenchmark que acione a operação.

**Como avaliar a implementação.** Validar semanticamente o resultado para vetores pequenos. Comparar implementação escalar e vetorial em soma de arrays ou transformação de imagem simples. Variar largura vetorial e tamanho dos dados, medindo instruções, ciclos, IPC e aceleração.

## 26. Modelo de custo de *gather* vetorial

**Objetivo.** Diferenciar acessos vetoriais contíguos de acessos indiretos e irregulares.

**O que implementar.** Criar uma operação ou unidade de memória vetorial simplificada que execute `gather` de endereços fornecidos por um vetor de índices. Modelar custo proporcional ao número de linhas de cache distintas acessadas, com limite configurável de requisições simultâneas.

**Como avaliar a implementação.** Criar benchmark de leitura contígua, leitura com salto fixo e leitura por índices aleatórios. Comparar ciclos, linhas distintas, faltas de cache e aceleração potencial frente à versão escalar. Mostrar que largura SIMD não implica ganho automático em acessos irregulares.

## 27. Máscaras de predicação vetorial

**Objetivo.** Modelar a execução de operações vetoriais condicionais sem desvio por elemento.

**O que implementar.** Acrescentar suporte didático para uma máscara de elementos ativos em uma operação vetorial aritmética. A unidade deve contabilizar elementos ativos e inativos; o resultado dos inativos deve seguir uma semântica definida e documentada. Criar uma interface mínima no benchmark para construir máscaras.

**Como avaliar a implementação.** Usar filtragem de valores, limiarização de imagem ou ReLU em vetor. Variar a proporção de elementos ativos e comparar versão escalar com desvios, vetorial mascarada e, se disponível, vetorial sem máscara. Medir ciclos, instruções, predição de desvios e utilização efetiva das pistas.

## 28. Política de *tail handling* para vetores de tamanho não múltiplo

**Objetivo.** Avaliar o custo dos elementos residuais em laços vetorizados.

**O que implementar.** Implementar no benchmark/biblioteca duas estratégias: trecho escalar final e última operação vetorial mascarada. Se o modelo vetorial permitir, registrar quantas pistas foram desperdiçadas na cauda. Expor o tamanho do vetor e a largura como parâmetros.

**Como avaliar a implementação.** Varrer tamanhos próximos a múltiplos e não múltiplos da largura vetorial. Comparar ciclos e utilização de pistas das duas estratégias. Identificar em quais tamanhos a máscara reduz custo e em quais seu overhead domina.

## 29. Fila de instruções com agrupamento de operações vetoriais

**Objetivo.** Explorar o ganho de emitir operações de dados independentes para uma unidade vetorial.

**O que implementar.** Em um modelo simplificado de CPU ou em um componente educacional, detectar sequências de operações aritméticas independentes de mesmo tipo e agrupá-las em uma “macro-operação” vetorial até uma largura máxima. Preservar dependências e oferecer chave para desativar o agrupamento.

**Como avaliar a implementação.** Usar kernels de SAXPY, transformação de pixels e uma carga com dependências em cadeia. Comparar instruções emitidas, ciclos, tamanho médio dos grupos e resultado numérico. Demonstrar por que o agrupamento não deve ocorrer na cadeia dependente.

## 30. Extensão de estatísticas de utilização SIMD

**Objetivo.** Quantificar eficiência real de vetorização, e não apenas a presença de instruções vetoriais.

**O que implementar.** Adicionar ao modelo ou ao fluxo de instrumentação contadores para instruções vetoriais, largura nominal, elementos ativos, elementos mascarados e ocupação média. Calcular uma métrica `elementos_ativos / (instruções_vetoriais × largura)`.

**Como avaliar a implementação.** Validar os contadores em três kernels: vetor totalmente cheio, operação mascarada e laço com cauda. Relacionar utilização SIMD com tempo de execução e apresentar um caso em que mais instruções vetoriais não resultam em melhor desempenho.

---

# 6. GPU

## 31. Escalonador de *warps* round-robin e por prontidão

**Objetivo.** Comparar duas políticas de escolha de *warps* em um núcleo GPU.

**O que implementar.** No modelo GPU disponível na instalação, implementar ou adaptar um seletor de *warps* com dois modos: round-robin e *oldest-ready* (ou política por prontidão). Acrescentar estatísticas de emissões por *warp*, ciclos bloqueados por memória e distribuição de espera.

**Como avaliar a implementação.** Executar kernels com alta latência de memória e kernels computacionais. Comparar IPC do núcleo GPU, ocupação, ciclos ociosos, tempo do kernel e justiça de emissão. Verificar que a política por prontidão apresenta benefício principalmente quando há bloqueios variados.

## 32. Coalescimento de acessos globais configurável

**Objetivo.** Estudar como o agrupamento de acessos de *threads* reduz transações de memória na GPU.

**O que implementar.** Implementar ou alterar um coalescedor simplificado que agrupa acessos de um *warp* por segmento/linha de memória de tamanho configurável. Registrar número de acessos individuais, transações geradas e eficiência de coalescimento.

**Como avaliar a implementação.** Criar kernels de acesso contíguo, com salto e aleatório. Variar tamanho de segmento e tamanho de *warp*. Medir transações por carga, latência, largura de banda efetiva e tempo. Confirmar que acesso contíguo exige menos transações.

## 33. Detector de divergência de *warps*

**Objetivo.** Medir a perda de utilização causada por desvios condicionais em SIMT.

**O que implementar.** Adicionar contadores no estágio de execução/controle da GPU para registrar ramos divergentes, caminhos executados, máscaras ativas e eficiência média por *warp*. A métrica deve distinguir ramos uniformes de divergentes.

**Como avaliar a implementação.** Executar kernels com condição uniforme, condição alternada por identificador de *thread* e condição aleatória. Comparar tempo, instruções efetivas, eficiência de *warp* e divergências. Incluir uma versão do kernel reorganizada para reduzir divergência e discutir o efeito.

## 34. Cache compartilhada por bloco com banco e conflitos

**Objetivo.** Modelar o custo de conflitos em memória compartilhada de GPU.

**O que implementar.** Criar ou estender uma memória compartilhada com número configurável de bancos e mapeamento por endereço. Acessos de *threads* de um mesmo *warp* ao mesmo banco devem sofrer serialização conforme uma regra documentada. Coletar conflitos por acesso e atrasos acumulados.

**Como avaliar a implementação.** Usar padrões de acesso sem conflito, com conflito de 2 vias e conflito alto. Variar número de bancos e *padding* da estrutura. Medir conflitos, latência, tempo do kernel e ganho obtido pelo *padding*.

## 35. Limite de ocupação por registradores e memória compartilhada

**Objetivo.** Mostrar como recursos por bloco limitam o número de *warps* residentes.

**O que implementar.** Implementar um calculador de ocupação no modelo/configuração GPU que limita blocos residentes por registradores por *thread*, memória compartilhada por bloco e máximo de *warps*. Expor parâmetros e registrar o motivo que impediu novas alocações.

**Como avaliar a implementação.** Variar artificialmente registradores e memória compartilhada consumidos por kernels. Medir *warps* residentes, capacidade de esconder latência, IPC e tempo. Construir gráfico de ocupação versus desempenho e destacar que ocupação máxima não é sempre o melhor ponto.

## 36. Fila de transferência host–GPU com sobreposição de cópia e kernel

**Objetivo.** Modelar o benefício de sobrepor transferências de dados e computação.

**O que implementar.** Criar um componente de fila simples com comandos de cópia host–dispositivo, execução de kernel e dependências. Implementar dois modos: execução estritamente serial e cópia assíncrona que pode sobrepor com kernel independente. Incluir estatísticas de tempo em cópia, computação e sobreposição.

**Como avaliar a implementação.** Simular várias etapas de processamento de lotes, cada uma com transferência de entrada, kernel e transferência de saída. Variar tamanho do lote e duração do kernel. Comparar tempo total, fração sobreposta e gargalo predominante. Validar que dependências corretas impedem sobreposição indevida.

---

# Orientação para escolha do tema

Os temas **1–6** tendem a exigir mais programação de benchmarks e instrumentação; os temas **7–12** concentram-se em Ruby/Garnet e topologias; os temas **13–18** exigem leitura mais cuidadosa de controladores e protocolos de coerência; os temas **19–24** exploram caches, memória e interferência em sistemas multinúcleo; os temas **25–30** podem ser realizados como extensões didáticas de uma ISA/modelo de execução vetorial; e os temas **31–36** dependem da infraestrutura GPU instalada e devem ser selecionados apenas se ela estiver funcional no ambiente da disciplina.

Para reduzir risco, o professor pode permitir que cada grupo entregue em três marcos:

1. **Semana 3–4:** desenho do mecanismo, leitura de código e experimento de linha de base;
2. **Semana 7–8:** versão funcional mínima, teste de correção e primeiras estatísticas;
3. **Semana 11–12:** campanha experimental, relatório e demonstração.

A comparação com a linha de base é obrigatória, mas não se espera que toda proposta gere melhoria de desempenho. Um resultado negativo é válido quando o mecanismo está correto, a metodologia é sólida e a análise explica as causas do comportamento observado.
