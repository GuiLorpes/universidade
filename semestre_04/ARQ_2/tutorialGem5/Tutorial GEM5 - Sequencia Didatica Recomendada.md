# Tutorial GEM5 — Sequência Didática Recomendada

## Introdução

Esta coleção reúne tutoriais práticos sobre o **gem5**, desde a preparação do ambiente e as primeiras simulações até estudos de arquiteturas paralelas, protocolos de coerência, redes em chip, sistemas operacionais, energia, segurança e aceleradores.

Como os temas têm dependências conceituais e técnicas, não é recomendável executá-los simplesmente pela ordem alfabética. Este roteiro organiza uma progressão em camadas: primeiro aprende-se a executar e observar simulações simples; depois, a modelar processador e memória; em seguida, a construir campanhas experimentais; por fim, investigam-se sistemas paralelos, especializados e completos.

> **Objetivo:** orientar qual tutorial estudar em cada etapa, explicar os pré-requisitos e indicar produtos práticos esperados. A sequência é recomendada para quem inicia no gem5, mas cada trilha também pode ser usada de forma independente por quem já domina os fundamentos.

---

## 1. Visão geral da jornada

A sequência está dividida em oito etapas:

| Etapa | Foco principal | Resultado esperado |
|---|---|---|
| 1 | Ambiente e execução básica | Compilar o gem5 e executar programas em SE e FS |
| 2 | Leitura de resultados e CPU | Interpretar `stats.txt` e comparar modelos de processador |
| 3 | Hierarquia de memória | Dimensionar caches e memória DDR |
| 4 | Método experimental | Construir benchmarks, automatizar campanhas e analisar dados |
| 5 | Paralelismo básico | Simular multiprogramação, multicore e sincronização |
| 6 | Coerência e interconexão | Explorar Ruby, protocolos e topologias de rede |
| 7 | Plataformas e especialização | ARM, SIMD, GPU, big.LITTLE, aceleradores e IA |
| 8 | Estudos avançados de sistema | FS, SO, virtualização, energia, segurança, confiabilidade e NVM |

A recomendação central é manter um repositório próprio com:

- os programas C/C++ usados nos experimentos;
- os scripts Python de configuração do gem5;
- scripts de automação;
- um arquivo de metadados para cada execução;
- tabelas e gráficos produzidos a partir dos diretórios de saída.

Isso torna os resultados reproduzíveis e permite comparar experimentos realizados em momentos diferentes.

---

# Etapa 1 — Fundamentos operacionais

Esta etapa apresenta a instalação, as formas de iniciar simulações e os dois modos fundamentais de operação. Deve ser seguida integralmente por iniciantes.

## 1.1 Download, compilação e estrutura do projeto

### Tutorial
**Tutorial GEM5 - Download e Build.md**

### Por que começar aqui

O tutorial apresenta a obtenção do código-fonte, dependências, compilação para diferentes ISAs e a organização básica do projeto. Também introduz a diferença entre os modos **Syscall Emulation (SE)** e **Full System (FS)**.

### Competências adquiridas

- Compilar o gem5 para uma ISA de interesse, como `X86`, `ARM` ou `RISCV`.
- Identificar binários em `build/<ISA>/`.
- Executar comandos básicos do simulador.
- Reconhecer quando o modo SE é suficiente e quando FS é necessário.

### Marco de conclusão

Execute o binário de teste e registre a versão/commit do gem5 utilizado. Para experimentos acadêmicos, esta informação deve acompanhar todos os resultados.

---

## 1.2 Primeiro programa, SE, FS e estatísticas

### Tutorial
**Tutorial GEM5 - Programa, SE, FS e Stats.md**

### Pré-requisito

Conclusão do tutorial de download e build.

### Por que estudá-lo agora

Ele conecta um programa compilado à execução simulada e mostra como localizar métricas em `stats.txt`. A leitura de estatísticas é necessária em praticamente todos os demais tutoriais.

### Conceitos essenciais

- `--cmd`, argumentos do programa e diretório de saída.
- Eventos de término da simulação.
- `simTicks`, `simSeconds`, `simInsts` e `hostSeconds`.
- IPC e CPI, calculados a partir de instruções e ciclos.

### Marco de conclusão

Execute o mesmo programa em SE e FS, quando a infraestrutura de FS estiver disponível, e compare o custo de preparação, a fidelidade de sistema e as estatísticas observáveis.

---

## 1.3 Detalhamento do modo SE

### Tutorial
**Tutorial GEM5 - Modo SE Detalhado.md**

### Pré-requisito

Primeiro programa em SE concluído.

### Objetivo da posição na sequência

SE é o modo mais eficiente para experimentar microarquitetura quando a execução de um sistema operacional completo não é necessária. Este tutorial consolida a criação de processos e a configuração mínima de um sistema.

### Marco de conclusão

Modifique os argumentos do programa, o clock e o tamanho da memória; valide que a mudança aparece na configuração gerada e afeta a execução conforme esperado.

---

## 1.4 Detalhamento do modo FS

### Tutorial
**Tutorial GEM5 - Modo FS Detalhado.md**

### Pré-requisito

Entendimento de SE e disponibilidade de kernel, disco e recursos compatíveis com a ISA.

### Por que não iniciar por FS

FS adiciona kernel, sistema de arquivos, scripts de inicialização e tempo de boot. Esses elementos ocultam a causa de muitos erros iniciais. Por isso, o modo deve ser estudado depois que SE e `stats.txt` já forem familiares.

### Marco de conclusão

Inicialize uma imagem de sistema, execute o benchmark dentro do sistema convidado e delimite uma região de interesse (ROI) para evitar medir apenas boot e inicialização.

---

## 1.5 Configuração com a API Python

### Tutorial
**Tutorial GEM5 - SE com API Python.md**

### Pré-requisito

Domínio básico de SE e familiaridade introdutória com Python.

### Objetivo

Migrar de linhas de comando e configurações prontas para a construção explícita de plataformas simuladas pela API Python. Esta é a base para personalizar experiências posteriores.

### Marco de conclusão

Crie uma configuração SE própria com processador, memória, barramento e caches; execute um binário e preserve o script junto ao resultado.

---

# Etapa 2 — Processador, execução e desvios

Após saber montar uma simulação simples, o próximo passo é entender as estruturas que determinam a taxa de execução de instruções.

## 2.1 Comparação de modelos de CPU

### Tutorial
**Tutorial GEM5 - Comparacao de Modelos de CPU.md**

### Pré-requisito

Etapa 1 concluída, especialmente a leitura de `stats.txt`.

### Sequência recomendada

Compare modelos de CPU simples e detalhados antes de alterar o pipeline. Isso deixa claro que resultados dependem tanto do workload quanto do nível de abstração escolhido.

### Perguntas de pesquisa

- Quais modelos possuem maior custo de simulação?
- Quando IPC e tempo simulado diferem de forma relevante?
- Que modelos são apropriados para triagem rápida e quais são apropriados para avaliação microarquitetural?

---

## 2.2 Predição de desvios

### Tutorial
**Tutorial GEM5 - Predicao de Desvios.md**

### Pré-requisito

Comparação de modelos de CPU; recomenda-se uma CPU que modele pipeline e especulação adequadamente.

### Objetivo

Avaliar a influência de desvios condicionais na vazão do processador, usando taxa de acerto, penalidade de predição incorreta e IPC.

### Marco de conclusão

Construa uma tabela com preditores, acurácia, número de *mispredictions*, IPC e tempo de execução. Não conclua que o preditor com maior acurácia é sempre melhor sem observar a penalidade e o custo do pipeline.

---

## 2.3 Pipeline superscalar O3

### Tutorial
**Tutorial GEM5 - Pipeline Superscalar O3.md**

### Pré-requisito

Modelos de CPU e predição de desvios.

### Por que vem depois

Parâmetros como largura de busca, despacho, emissão, ROB, filas e unidades funcionais interagem entre si. Sem uma noção anterior de IPC, desvios e gargalos, é fácil interpretar erroneamente os resultados.

### Marco de conclusão

Faça uma varredura de pelo menos dois parâmetros por vez — por exemplo, largura e tamanho do ROB — e identifique o ponto em que ganhos se tornam marginais.

---

## 2.4 Extensões vetoriais SIMD

### Tutorial
**Tutorial GEM5 - Extensoes Vetoriais SIMD.md**

### Pré-requisito

CPU, compilação cruzada para a ISA escolhida e noções de pipeline.

### Objetivo

Relacionar paralelismo no nível de dados, instruções vetoriais, compilador e desempenho. O tutorial deve ser realizado depois do estudo de CPU para distinguir ganhos por vetor de ganhos por mudança na configuração do processador.

---

# Etapa 3 — Hierarquia de memória

Esta etapa cria a base necessária para interpretar misses, tráfego e latências antes de avançar para coerência e redes multicore.

## 3.1 Hierarquia de memória

### Tutorial
**Tutorial GEM5 - Hierarquia de Memoria.md**

### Pré-requisito

Etapa 1 e métricas básicas de CPU.

### Objetivo

Modelar caches privadas e compartilhadas, compreender associatividade, tamanho de linha, capacidade, latência e taxas de miss.

### Ordem de experimentação sugerida

1. Varie tamanho de L1 mantendo o restante fixo.
2. Varie associatividade.
3. Introduza ou altere L2.
4. Compare métricas por nível de cache.
5. Relacione a mudança de misses com IPC e tempo total.

---

## 3.2 Políticas de substituição de cache com cBench

### Tutorial
**Tutorial GEM5 - Politicas de Substituicao de Cache com cBench.md**

### Pré-requisito

Hierarquia de memória e domínio de SE com API Python.

### Objetivo

Avaliar políticas de substituição em caches associativas utilizando workloads do cBench, isolando a política como variável experimental.

### Cuidados metodológicos

- Mantenha cache, CPU, clock e memória constantes entre políticas.
- Execute mais de um benchmark, pois não existe política universalmente superior.
- Analise misses de instrução e dados, não apenas o tempo total.

---

## 3.3 Memória DDR

### Tutorial
**Tutorial GEM5 - Memoria DDR.md**

### Pré-requisito

Hierarquia de memória e interpretação de latências.

### Objetivo

Estudar controladores e parâmetros de DRAM, identificando efeitos de largura de barramento, taxa de transferência, filas, bancos e padrões de acesso.

### Marco de conclusão

Compare pelo menos um workload com boa localidade e outro com maior pressão de memória. Um parâmetro de DRAM não deve ser avaliado apenas em um programa.

---

## 3.4 Memória persistente e NVM

### Tutorial
**Tutorial GEM5 - Memoria Persistente e NVM.md**

### Pré-requisito

Memória DDR e noções de latência/escrita.

### Objetivo

Comparar memória volátil convencional e NVM, investigando assimetria entre leitura e escrita, largura de banda e impacto de políticas de acesso.

---

## 3.5 Falhas de memória e tolerância a erros

### Tutorial
**Tutorial GEM5 - Falhas de Memoria e Tolerancia a Erros.md**

### Pré-requisito

Hierarquia de memória e modelo de memória.

### Objetivo

Investigar confiabilidade, injeção de falhas e estratégias de detecção/correção. Deve ser feito depois de compreender a configuração normal, pois é necessário separar o efeito da falha de falhas de configuração ou do benchmark.

---

# Etapa 4 — Método experimental, benchmarks e automação

Estes tutoriais transformam execuções isoladas em uma campanha científica reproduzível. Idealmente, devem ser concluídos antes de estudos extensos de multicore, NoC ou energia.

## 4.1 Criação de benchmark próprio

### Tutorial
**Tutorial GEM5 - Criacao de Benchmark Proprio.md**

### Pré-requisito

SE, compilação e leitura de estatísticas.

### Objetivo

Projetar um benchmark controlado, documentar seu comportamento esperado e validar que ele estressa o componente pretendido.

### Regra importante

Evite usar apenas o resultado final correto como validação. Confirme também o perfil de acesso, a quantidade de trabalho e a estabilidade das métricas entre repetições.

---

## 4.2 Automação de campanhas e visualização

### Tutorial
**Tutorial GEM5 - Automacao de Campanhas e Visualizacao.md**

### Pré-requisito

Benchmark próprio ou conjunto de benchmarks definido.

### Objetivo

Automatizar varreduras de parâmetros, extrair estatísticas e produzir tabelas e gráficos. Esta prática reduz erros manuais e favorece comparações justas.

### Marco de conclusão

Gere uma tabela consolidada contendo configuração, benchmark, métricas e caminho da execução. Todo gráfico deve poder ser regenerado a partir dos dados brutos.

---

## 4.3 Análise energética com McPAT

### Tutorial
**Tutorial GEM5 - Analise Energetica com McPAT.md**

### Pré-requisito

Automação, comparação de CPU e hierarquia de memória.

### Por que estudar depois da automação

A estimativa energética exige traduzir configuração e estatísticas do gem5 para parâmetros aceitos pelo McPAT. Uma campanha automatizada torna a integração menos suscetível a inconsistências.

### Métricas recomendadas

- Potência dinâmica e estática.
- Energia total.
- Energia por instrução.
- Relação desempenho/energia e energia-atraso, quando aplicável.

---

## 4.4 Checkpoints e restauração

### Tutorial
**Tutorial GEM5 - Checkpoints e Restauracao.md**

### Pré-requisito

SE ou FS funcional; familiaridade com regiões de interesse.

### Objetivo

Separar aquecimento e inicialização da fase medida, acelerar campanhas e alternar entre modelos de CPU quando apropriado.

### Boa prática

Documente exatamente quando o checkpoint foi criado e mantenha essa condição idêntica entre configurações comparadas.

---

# Etapa 5 — Paralelismo, multicore e sincronização

Nesta etapa, o estudante passa de programas de um núcleo para compartilhamento de recursos, escalabilidade e comunicação entre threads.

## 5.1 Multiprogramação no modo SE

### Tutorial
**Tutorial GEM5 - Multiprogramacao no Modo SE.md**

### Pré-requisito

SE detalhado, API Python e métricas básicas.

### Objetivo

Executar múltiplos processos e observar competição por CPU, caches e memória. É uma ponte mais simples entre sistemas de um núcleo e aplicações paralelas.

---

## 5.2 Simulação multicore e escalabilidade

### Tutorial
**Tutorial GEM5 - Simulacao Multicore e Escalabilidade.md**

### Pré-requisito

Multiprogramação e hierarquia de memória.

### Objetivo

Avaliar *speedup*, eficiência paralela, desequilíbrio de carga e pressão em recursos compartilhados.

### Métricas fundamentais

Para tempo serial \(T_1\) e tempo com \(N\) núcleos \(T_N\):

\[
S_N = \frac{T_1}{T_N}, \qquad E_N = \frac{S_N}{N}.
\]

O aumento no número de núcleos só deve ser interpretado com essas métricas e com estatísticas de cache/memória.

---

## 5.3 Falsa compartilhação em programas paralelos

### Tutorial
**Tutorial GEM5 - Falsa Compartilhacao em Programas Paralelos.md**

### Pré-requisito

Multicore e noções de linhas de cache.

### Objetivo

Distinguir dados logicamente independentes de dados fisicamente colocados na mesma linha de cache. O estudo mostra por que *padding* e organização de estruturas podem melhorar desempenho sem alterar o algoritmo.

---

## 5.4 Contenção em locks, barreiras e atômicos

### Tutorial
**Tutorial GEM5 - Contencao em Locks Barreiras e Atomicos.md**

### Pré-requisito

Multicore e falsa compartilhação.

### Objetivo

Medir o efeito de primitivas de sincronização em escalabilidade, invalidações e tráfego. Compare regiões críticas curtas/longas e diferentes números de threads.

### Interpretação esperada

Um lock pode preservar a correção e, ao mesmo tempo, limitar fortemente o *speedup*. O resultado deve relacionar tempo em espera, tráfego de coerência e tamanho da região serial.

---

# Etapa 6 — Coerência, redes e arquiteturas paralelas escaláveis

Esta é a trilha central para o estudo de arquiteturas paralelas. Recomenda-se seguir a ordem apresentada, pois ela evolui de conceitos de coerência para comunicação e políticas de rede.

## 6.1 Coerência de cache com Ruby

### Tutorial
**Tutorial GEM5 - Coerencia de Cache com Ruby.md**

### Pré-requisito

Hierarquia de memória, multicore e linhas de cache.

### Objetivo

Introduzir Ruby e a modelagem detalhada de coerência. Antes de comparar protocolos, assegure-se de entender os componentes, controladores e estatísticas do sistema Ruby.

---

## 6.2 Protocolos MSI, MESI e MOESI no Ruby

### Tutorial
**Tutorial GEM5 - Protocolos MSI MESI e MOESI no Ruby.md**

### Pré-requisito

Coerência com Ruby.

### Objetivo

Comparar estados e transições de protocolos, além do tráfego gerado por leituras e escritas compartilhadas. Use benchmarks que realmente exerçam compartilhamento; programas sem comunicação entre threads pouco revelam sobre coerência.

---

## 6.3 Coerência por diretório versus snooping

### Tutorial
**Tutorial GEM5 - Coerencia por Diretorio versus Snooping.md**

### Pré-requisito

MSI/MESI/MOESI e noções de escalabilidade multicore.

### Objetivo

Contrastar difusão (*broadcast*) e controle baseado em diretório, analisando custos de metadados, mensagens e crescimento do sistema.

---

## 6.4 Interconexão multicore e NoC

### Tutorial
**Tutorial GEM5 - Interconexao Multicore e NoC.md**

### Pré-requisito

Multicore, Ruby e fundamentos de coerência.

### Objetivo

Introduzir redes de interconexão entre núcleos, caches e memória. Esta é a base prática para os tutoriais de topologia, posicionamento, hierarquia e QoS.

---

## 6.5 Topologias de rede on-chip

### Tutorial
**Tutorial GEM5 - Topologias de Rede on-Chip.md**

### Pré-requisito

Interconexão multicore e Ruby.

### Objetivo

Comparar mesh, torus, ring e crossbar em termos de distância, contenção, latência, vazão e escalabilidade.

### Boa prática experimental

Ao comparar topologias, mantenha a quantidade de núcleos, controladores e workload constante. Se a topologia exigir diferentes mapeamentos, documente-os como parte da configuração.

---

## 6.6 Posicionamento de controladores de memória na NoC

### Tutorial
**Tutorial GEM5 - Posicionamento de Controladores de Memoria na NoC.md**

### Pré-requisito

Topologias de NoC e memória DDR.

### Objetivo

Avaliar como a posição dos controladores altera a quantidade de saltos, latência de acesso e desigualdade entre núcleos. É importante estudar depois das topologias para não confundir efeito de localização com efeito da própria rede.

---

## 6.7 Topologias hierárquicas para muitos núcleos

### Tutorial
**Tutorial GEM5 - Topologias Hierarquicas para Muitos Nucleos.md**

### Pré-requisito

Topologias básicas e posicionamento de memória.

### Objetivo

Modelar clusters e redes em múltiplos níveis, comparando-as a uma rede plana. O foco é entender em que escala a hierarquia reduz custo, e quando ela passa a introduzir gargalos entre clusters.

---

## 6.8 Qualidade de serviço na interconexão

### Tutorial
**Tutorial GEM5 - Qualidade de Servico na Interconexao.md**

### Pré-requisito

NoC, topologias e automação de campanhas.

### Objetivo

Estudar priorização, justiça e isolamento de tráfego com workloads concorrentes. Esta avaliação requer mais de uma classe de aplicação e deve considerar tanto médias como caudas de latência.

---

## 6.9 Sistemas NUMA, afinidade e localidade

### Tutorial
**Tutorial GEM5 - Sistemas NUMA Afinidade de Memoria e Localidade.md**

### Pré-requisito

Multicore, memória DDR, NoC e posicionamento de controladores.

### Objetivo

Analisar acessos locais/remotos e políticas de posicionamento de dados. Este tutorial integra conceitos de software, comunicação e memória, sendo adequado ao final da trilha de arquiteturas paralelas.

---

## 6.10 Consistência de memória: SC, TSO e modelos relaxados

### Tutorial
**Tutorial GEM5 - Consistencia de Memoria SC TSO e Modelos Relaxados.md**

### Pré-requisito

Coerência de cache, sincronização e arquitetura multicore.

### Objetivo

Distinguir coerência — acordo sobre uma linha de cache — de consistência — ordem visível das operações de memória. Por envolver semântica de ISA, compilador e sincronização, este deve ser tratado após a compreensão do sistema de coerência.

---

# Etapa 7 — Plataformas heterogêneas e computação especializada

Esta etapa explora sistemas em que os recursos não são homogêneos: diferentes ISAs, diferentes tipos de núcleo e aceleradores.

## 7.1 Sistemas embarcados ARM

### Tutorial
**Tutorial GEM5 - Sistemas Embarcados ARM.md**

### Pré-requisito

Build, SE/FS e API Python.

### Objetivo

Aplicar os fundamentos a uma plataforma ARM, considerando ISA, compilação cruzada, dispositivos e restrições comuns em sistemas embarcados.

---

## 7.2 Sistemas heterogêneos big.LITTLE

### Tutorial
**Tutorial GEM5 - Sistemas Heterogeneos big.LITTLE.md**

### Pré-requisito

ARM, modelos de CPU, multicore e escalabilidade.

### Objetivo

Estudar núcleos com desempenho e consumo diferentes. Compare políticas de alocação de trabalho e não apenas o desempenho bruto: a motivação de big.LITTLE inclui eficiência energética.

---

## 7.3 Simulação de GPUs

### Tutorial
**Tutorial GEM5 - Simulacao de GPUs.md**

### Pré-requisito

Multicore, hierarquia de memória e noções de paralelismo massivo.

### Objetivo

Introduzir a modelagem de GPU e a interação entre alto paralelismo, memória e processador hospedeiro. O estudante deve diferenciar claramente threads de CPU de grupos de execução típicos de GPU.

---

## 7.4 Aceleradores personalizados

### Tutorial
**Tutorial GEM5 - Aceleradores Personalizados.md**

### Pré-requisito

API Python, memória e interconexão; recomenda-se GPU ou SIMD como referência de especialização.

### Objetivo

Modelar um bloco dedicado, sua interface com o sistema e os compromissos de latência, largura de banda e sincronização.

---

## 7.5 Workloads de inteligência artificial

### Tutorial
**Tutorial GEM5 - Workloads de Inteligencia Artificial.md**

### Pré-requisito

Hierarquia de memória, SIMD, GPU ou aceleradores, conforme o experimento escolhido.

### Objetivo

Avaliar cargas com alta intensidade computacional e/ou de memória, estudando localidade, paralelismo de dados e adequação entre workload e plataforma.

---

# Etapa 8 — Sistema completo e avaliações avançadas

A etapa final integra hardware e software em estudos de sistema, com maior custo de configuração e simulação.

## 8.1 Sistemas operacionais e escalonamento

### Tutorial
**Tutorial GEM5 - Sistemas Operacionais e Escalonamento.md**

### Pré-requisito

FS detalhado, multicore e regiões de interesse.

### Objetivo

Investigar a influência do escalonador, migração de tarefas e competição por recursos. As medições devem separar comportamento da aplicação, do kernel e do boot.

---

## 8.2 Virtualização em Full System

### Tutorial
**Tutorial GEM5 - Virtualizacao em Full System.md**

### Pré-requisito

FS, sistemas operacionais e arquitetura da ISA alvo.

### Objetivo

Avaliar a execução de ambientes virtualizados, distinguindo overhead de virtualização, custo de E/S e comportamento das aplicações convidadas.

---

## 8.3 DVFS e gerenciamento de frequência

### Tutorial
**Tutorial GEM5 - DVFS e Gerenciamento de Frequencia.md**

### Pré-requisito

Modelos de CPU, automação e, preferencialmente, análise energética.

### Objetivo

Avaliar compromissos entre frequência, desempenho e consumo. Uma análise correta deve discutir tempo de execução e energia, não apenas uma dessas dimensões.

---

## 8.4 Segurança de arquitetura

### Tutorial
**Tutorial GEM5 - Seguranca de Arquitetura.md**

### Pré-requisito

Pipeline, caches, coerência e/ou FS, conforme o cenário de segurança escolhido.

### Objetivo

Estudar como estruturas microarquiteturais podem afetar isolamento e comportamento observável. Mantenha a abordagem em experimentos controlados e defensivos, priorizando medição e mitigação.

---

# 9. Trilhas por objetivo

Além da sequência completa, a coleção pode ser percorrida por objetivo de pesquisa.

## 9.1 Trilha curta: primeiros experimentos microarquiteturais

1. Download e Build.
2. Programa, SE, FS e Stats.
3. Modo SE Detalhado.
4. SE com API Python.
5. Comparação de Modelos de CPU.
6. Hierarquia de Memória.
7. Automação de Campanhas e Visualização.

**Produto final:** uma campanha reproduzível comparando duas configurações de CPU ou cache.

## 9.2 Trilha de memória e caches

1. Fundamentos operacionais.
2. Hierarquia de Memória.
3. Políticas de Substituição de Cache com cBench.
4. Memória DDR.
5. Memória Persistente e NVM.
6. Falhas de Memória e Tolerância a Erros.
7. Análise Energética com McPAT.

**Produto final:** estudo de compromisso entre desempenho, misses, latência, energia e confiabilidade.

## 9.3 Trilha de arquiteturas paralelas e coerência

1. SE com API Python.
2. Hierarquia de Memória.
3. Simulação Multicore e Escalabilidade.
4. Falsa Compartilhação.
5. Contenção em Locks, Barreiras e Atômicos.
6. Coerência de Cache com Ruby.
7. Protocolos MSI, MESI e MOESI.
8. Diretório versus Snooping.
9. Interconexão Multicore e NoC.
10. Topologias de Rede on-Chip.
11. Posicionamento de Controladores de Memória.
12. Topologias Hierárquicas.
13. Qualidade de Serviço na Interconexão.
14. Sistemas NUMA.
15. Consistência de Memória.

**Produto final:** uma comparação de escalabilidade que explique desempenho por meio de sincronização, coerência, tráfego de rede e localidade de memória.

## 9.4 Trilha de sistemas completos

1. Download e Build.
2. Programa, SE, FS e Stats.
3. Modo FS Detalhado.
4. Checkpoints e Restauração.
5. Sistemas Operacionais e Escalonamento.
6. Virtualização em Full System.
7. Sistemas Embarcados ARM ou big.LITTLE.

**Produto final:** experimento em FS com ROI bem definida, checkpoint e análise de métricas relevantes ao sistema.

## 9.5 Trilha de plataformas especializadas

1. Comparação de Modelos de CPU.
2. Hierarquia de Memória.
3. Extensões Vetoriais SIMD.
4. Sistemas Embarcados ARM.
5. Sistemas Heterogêneos big.LITTLE.
6. Simulação de GPUs.
7. Aceleradores Personalizados.
8. Workloads de Inteligência Artificial.

**Produto final:** análise de mapeamento de workload em CPU, vetor, GPU ou acelerador.

---

# 10. Projeto integrador sugerido

Ao terminar a sequência, desenvolva um estudo integrador: **escalabilidade de um workload paralelo intensivo em memória em uma arquitetura manycore**.

## Pergunta de pesquisa

Como a combinação de protocolo de coerência, topologia de NoC, posicionamento dos controladores de memória e política de sincronização afeta desempenho, tráfego e energia?

## Desenho experimental mínimo

| Dimensão | Alternativas iniciais |
|---|---|
| Núcleos | 4, 8, 16 |
| Organização | caches privadas + último nível compartilhado ou distribuído |
| Coerência | dois protocolos compatíveis disponíveis na configuração Ruby |
| Rede | mesh e torus, ou mesh e topologia hierárquica |
| Memória | controladores concentrados e distribuídos |
| Software | versão com contenção/falsa compartilhação e versão otimizada |
| Métricas | tempo, IPC, speedup, eficiência, misses, mensagens, hops, latência e energia |

## Procedimento

1. Valide o benchmark em um núcleo.
2. Faça o *baseline* multicore com configuração fixa.
3. Varie a organização de dados para eliminar falsa compartilhação acidental.
4. Varie a política de sincronização.
5. Compare protocolos de coerência.
6. Compare topologias com a mesma quantidade de controladores.
7. Altere somente o posicionamento dos controladores.
8. Estime energia para as configurações finalistas.
9. Automatize a extração de métricas e gere gráficos com barras de erro ou repetição quando aplicável.
10. Discuta limites de validade: modelo de CPU, versão do gem5, workload, tamanho de entrada e parâmetros fixados.

---

# 11. Checklist antes de avançar de etapa

Antes de iniciar tópicos mais avançados, confirme:

- [ ] Sei recompilar o gem5 e registrar a versão usada.
- [ ] Sei compilar o benchmark para a ISA simulada.
- [ ] Sei executar uma configuração SE e localizar `config.ini`, `config.json` e `stats.txt`.
- [ ] Sei distinguir tempo de simulação, tempo de hospedeiro, instruções, ciclos, IPC e CPI.
- [ ] Sei alterar uma variável por vez e preservar as demais constantes.
- [ ] Sei automatizar várias execuções e consolidar seus resultados.
- [ ] Sei usar uma região de interesse ou checkpoint quando inicialização/boot puder contaminar a medição.
- [ ] Sei justificar a escolha de workload, CPU, cache, rede e métricas.
- [ ] Sei distinguir um resultado observado de uma explicação causal sustentada por estatísticas.

---

# Conclusão

A coleção foi organizada para que os estudos avançados sejam consequência direta de fundamentos sólidos. O caminho mais eficiente é dominar primeiro **SE, API Python, métricas e memória**; depois avançar para **multicore, coerência e NoC**; e somente então integrar **sistema operacional, heterogeneidade, energia, segurança e confiabilidade**.

A sequência não impede explorações pontuais. Porém, ao seguir as dependências indicadas, cada novo experimento passa a reutilizar uma base validada, com hipóteses claras, configurações rastreáveis e interpretações mais confiáveis.