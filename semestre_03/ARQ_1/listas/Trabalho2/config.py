from argparse import ArgumentParser

import m5
from m5.objects import *

# Politicas de substituição da cache
POLITICAS = {
    'FIFO': FIFORP(),
    'LFU': LFURP(),
    'LRU': LRURP(),
    'MRU': MRURP(),
    'RANDOM': RandomRP(),
    'WEIGHTED_LRU': WeightedLRURP()
}

# Cria classes das Caches
class L1Cache(Cache):
    '''Valores padrão da cache L1'''
    size = '32KiB'

    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, rp: str):
        super().__init__()

        self.replacement_policy = POLITICAS[rp]
        

    def connectBus(self, bus):
        '''
        Conecta a cache ao barramento da memória
        '''
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        '''
        Conecta a cache a CPU
        Definido por uma subclasse!
        '''
        raise NotImplementedError


class L1ICache(L1Cache):
    '''Cache L1 de Instruções'''

    def __init__(self, rp: str):
        super().__init__(rp)

    def connectCPU(self, cpu):
        '''
        Conecta a cache a porta de cache de instruções da CPU
        '''
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    '''Cache L1 de Dados'''

    def __init__(self, rp: str):
        super().__init__(rp)

    def connectCPU(self, cpu):
        '''Concecta a cache a porta de cache de dados da CPU'''
        self.cpu_side = cpu.dcache_port
    

class L2Cache(Cache):
    size = '32KiB'

    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, rp: str):
        super().__init__()
        self.replacement_policy = POLITICAS[rp]

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    
    def conenctMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports



# Lê argumentos da linha de comando
parser = ArgumentParser()

parser.add_argument("--binary")
parser.add_argument("--replacement_policy")

args = parser.parse_args()


# Cria sistema
system = System()

# Configurações do sistema
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '3GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Configurações da memória (ainda não criada)
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('1GB')]

# Cria CPU
system.cpu = AtomicSimpleCPU()

# Cria caches L1
system.cpu.icache = L1ICache(args.replacement_policy)
system.cpu.dcache = L1DCache(args.replacement_policy)

# Associa caches L1 com a CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Cria barramentos
system.l2bus = L2XBar()
system.membus = SystemXBar()

# Conecta cache L1 com o barramento da L2
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Cria L2 e conecta com o barramento com a L1 e com a memória
system.cpu.l2cache = L2Cache(args.replacement_policy)
system.cpu.l2cache.connectCPUSideBus(system.l2bus)
system.cpu.l2cache.conenctMemSideBus(system.membus)

# Cria controle de interrupção
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Cria memória
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram =  ()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Conecta sistema ao barramento
system.system_port = system.membus.cpu_side_ports

# Cria processo
arquivo = args.binary
system.workload = SEWorkload.init_compatible(arquivo)

process = Process()
process.cmd = [arquivo]

system.cpu.workload = process
system.cpu.createThreads()

# Instancia
root = Root(full_system=False, system=system)
m5.instantiate()



# Simula
print("\n\n-=-=-=-=-=- Inicio da Simulação -=-=-=-=-=-")
exit_event = m5.simulate()
print("-=-=-=-=-=-=- Fim da Simulação -=-=-=-=-=-=-\n\n")
print(f"Fim da simulação @ tick {m5.curTick()} causa da saída: {exit_event.getCause()}")
