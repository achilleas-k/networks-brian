from brian import *
import time

# Parameters
area=20000*umetre**2
Cm=(1*ufarad*cm**-2)*area
gl=(5e-5*siemens*cm**-2)*area
El=-60*mV
EK=-90*mV
ENa=50*mV
g_na=(100*msiemens*cm**-2)*area
g_kd=(30*msiemens*cm**-2)*area
VT=-63*mV
# Time constants
taue=5*ms
taui=10*ms
# Reversal potentials
Ee=0*mV
Ei=-80*mV
we=6*nS # excitatory synaptic weight (voltage)
wi=67*nS # inhibitory synaptic weight

start_time=time.time()
# The model
eqs=Equations('''
dv/dt = (gl*(El-v)+ge*(Ee-v)+gi*(Ei-v)-g_na*(m*m*m)*h*(v-ENa)-g_kd*(n*n*n*n)*(v-EK))/Cm : volt
dm/dt = alpham*(1-m)-betam*m : 1
dn/dt = alphan*(1-n)-betan*n : 1
dh/dt = alphah*(1-h)-betah*h : 1
dge/dt = -ge*(1./taue) : siemens
dgi/dt = -gi*(1./taui) : siemens
alpham = 0.32*(mV**-1)*(13*mV-v+VT)/(exp((13*mV-v+VT)/(4*mV))-1.)/ms : Hz
betam = 0.28*(mV**-1)*(v-VT-40*mV)/(exp((v-VT-40*mV)/(5*mV))-1)/ms : Hz
alphah = 0.128*exp((17*mV-v+VT)/(18*mV))/ms : Hz
betah = 4./(1+exp((40*mV-v+VT)/(5*mV)))/ms : Hz
alphan = 0.032*(mV**-1)*(15*mV-v+VT)/(exp((15*mV-v+VT)/(5*mV))-1.)/ms : Hz
betan = .5*exp((10*mV-v+VT)/(40*mV))/ms : Hz
''')

P=NeuronGroup(4000,model=eqs,\
              threshold=EmpiricalThreshold(threshold=-20*mV,refractory=3*ms),\
              implicit=True,freeze=True,compile=False)
Pe=P.subgroup(3200)
Pi=P.subgroup(800)
Ce=Connection(Pe,P,'ge',weight=we,sparseness=0.02)
Ci=Connection(Pi,P,'gi',weight=wi,sparseness=0.02)
# Initialization
P.v=El+(randn(len(P))*5-5)*mV
P.ge=(randn(len(P))*1.5+4)*10.*nS
P.gi=(randn(len(P))*12+20)*10.*nS

# Record the number of spikes and a few traces
Me=PopulationSpikeCounter(Pe)
Mi=PopulationSpikeCounter(Pi)
trace=StateMonitor(P,'v',record=[1,10,100])

print "Network construction time:",time.time()-start_time,"seconds"
print "Simulation running..."
run(1*msecond)
start_time=time.time()

run(1000*msecond)
duration=time.time()-start_time
print "Simulation time:",duration,"seconds"
print Me.nspikes,"excitatory spikes"
print Mi.nspikes,"inhibitory spikes"

plot(trace.times/ms,trace[1]/mV)
plot(trace.times/ms,trace[10]/mV)
plot(trace.times/ms,trace[100]/mV)
show()

