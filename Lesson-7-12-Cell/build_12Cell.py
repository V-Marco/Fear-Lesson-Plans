from bmtk.builder import NetworkBuilder
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
from bmtk.utils.sim_setup import build_env_bionet
import numpy as np
import sys
import synapses
import random

seed = 967
random.seed(seed)
np.random.seed(seed)

synapses.load()
syn = synapses.syn_params_dicts()

# Initialize our network

net = NetworkBuilder("biophysical")

num_inh = [1]

num_exc = [1]

##################################################################################
###################################BIOPHY#########################################

net.add_nodes(N=5, pop_name='PyrA',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:Cell_A',
              morphology=None)

net.add_nodes(N=3, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:Cell_C',
              morphology=None)
net.add_nodes(N=2, pop_name='OLM',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:SOM_Cell_old',
              morphology=None)

net.add_nodes(N=2, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)

##################################################################################
###################################External Networks##############################

# print("Internal nodes built")

print("making {} exc_stim nodes".format(np.sum(num_exc)))

# External excitatory inputs
tone = NetworkBuilder('tone')
tone.add_nodes(N=1,
               pop_name='tone',
               potential='exc',
               model_type='virtual')

print("making {} inh_stim nodes".format(np.sum(num_inh)))
# External inhibitory inputs
shock = NetworkBuilder('shock')
shock.add_nodes(N=1,
                pop_name='shock',
                potential='exc',
                model_type='virtual')
#backgrounds
backgroundPN_A = NetworkBuilder('bg_pn_a')
backgroundPN_A.add_nodes(N=5,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

backgroundPN_C = NetworkBuilder('bg_pn_c')
backgroundPN_C.add_nodes(N=3,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

backgroundPV = NetworkBuilder('bg_pv')
backgroundPV.add_nodes(N=2,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

backgroundOLM = NetworkBuilder('bg_olm')
backgroundOLM.add_nodes(N=2,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')



##################################################################################
###################################Edges##########################################

def one_to_all_shock2OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting shock cell {} to OLM cell {}".format(sid, tid))
    return 1

def one_to_all_shock2PV(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting shock cell {} to PV cell {}".format(sid, tid))
    return 1

def shock2PN(source, target):
    sid = source.node_id
    tid = target.node_id
    if (tid == 0 or tid == 3 or tid == 4 or tid == 6 or tid==7):
        print("connecting shock cell {} to PN {}".format(sid, tid))
        return 1
    else:
        return 0

def tone2PN(source, target):
    sid = source.node_id
    tid = target.node_id
    if (tid == 2 or tid == 4 or tid == 6 or tid == 7):
        print("connecting tone cell {} to PN {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        print("not connecting{}".format(tid))
        tmp_nsyn = 0
    return tmp_nsyn

def tone2PV(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting tone cell {} to PV cell {}".format(sid, tid))
    return 1

def tone2OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting tone cell {} to OLM cell {}".format(sid, tid))
    return 1

def PN2OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting PN cell {} to OLM cell {}".format(sid, tid))
    return 1

def PN2PV(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting PN cell {} to PV cell {}".format(sid, tid))
    return 1

def PV2OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting PV cell {} to OLM cell {}".format(sid, tid))
    return 1

def one_to_one(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting cell {} to {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return 0

    return tmp_nsyn

def pyr_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if (sid != tid):
        print("connecting PN cells {} and {}".format(sid, tid))
    return 1

def PV2PV(source, target):
    sid = source.node_id
    tid = target.node_id
    if (sid != tid):
        print("connecting PV cell {} to PV {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return 0
    return tmp_nsyn

def PV2PN(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting PV cells {} to PN cell {}".format(sid, tid))
    return 3

def OLM2PN(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting OLM cells {} to PN cell {}".format(sid, tid))
    return 2

def BG_to_PN_A(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting BG {} to PN_A{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return 0

    return tmp_nsyn

def BG_to_PN_C(source, target):
    sid = source.node_id
    tid = target.node_id
    tid = (tid-5)
    if sid == tid:
        print("connecting BG {} to PN_C{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return 0

    return tmp_nsyn

def BG_to_PV(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 10
    if sid == tid:
        print("connecting BG {} to pv{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return 0

    return tmp_nsyn

def BG_to_OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 8
    if sid == tid:
        print("connecting BG {} to olm{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return 0

    return tmp_nsyn

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='OLM'),
              connection_rule=one_to_all_shock2OLM,
              syn_weight=1.0,
              target_sections=['basal'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='shock2INT12.json',
              model_template=syn['shock2INT12.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=one_to_all_shock2PV,
              syn_weight=1.0,
              target_sections=['basal'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='shock2INT12.json',
              model_template=syn['shock2INT12.json']['level_of_detail'])


# Create connections between Tone --> Pyr cells
conn = net.add_edges(source=tone.nodes(), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=tone2PN,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='tone2PN.json',
              model_template=syn['tone2PN.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9

#net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='OLM'),
#              connection_rule=tone2OLM,
#              syn_weight=3.0,
#              target_sections=['somatic'],
#              delay=0.1,
#              distance_range=[10.0, 11.0],
#              dynamics_params='tone2INT.json',
#              model_template=syn['tone2INT.json']['level_of_detail'])

conn = net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=tone2PV,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='tone2INT.json',
              model_template=syn['tone2INT.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float]) # places syn on basal at 0.9

# Create connections between Pyr --> Pyr cells
conn = net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=pyr_connection,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PN2PN.json',
              model_template=syn['PN2PN.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9

conn = net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=pyr_connection,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PN2PN.json',
              model_template=syn['PN2PN.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9


conn = net.add_edges(source=net.nodes(pop_name=['PyrA', 'PyrC']), target=net.nodes(pop_name='OLM'),
              connection_rule=PN2OLM,
              syn_weight=1,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PN2SOM.json',
              model_template=syn['PN2SOM.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float]) # places syn on basal at 0.9

# Create connections between Pyr --> PV cells
conn = net.add_edges(source=net.nodes(pop_name=['PyrA', 'PyrC']), target=net.nodes(pop_name='PV'),
              connection_rule=PN2PV,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PN2PV.json',
              model_template=syn['PN2PV.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float]) # places syn on basal at 0.9


# Create connections Int --> Int cells

net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PV'),
              connection_rule=PV2PV,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PV2PV.json',
              model_template=syn['PV2PV.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='OLM'),
              connection_rule=PV2OLM,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PV2SOM.json',
              model_template=syn['PV2SOM.json']['level_of_detail'])

# Create connections Int --> Pyr cells
net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=PV2PN,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PV2PN.json',
              model_template=syn['PV2PN.json']['level_of_detail'])

conn = net.add_edges(source=net.nodes(pop_name='OLM'), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=OLM2PN,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='SOM2PN.json',
              model_template=syn['SOM2PN.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.6), dtypes=[np.int32, np.float]) # places syn on apic at 0.6

conn = net.add_edges(source=backgroundPN_A.nodes(), target=net.nodes(pop_name='PyrA'),
              connection_rule=BG_to_PN_A,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='BG2PNA.json',
              model_template=syn['BG2PNA.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9

conn = net.add_edges(source=backgroundPN_C.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=BG_to_PN_C,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='BG2PNC.json',
              model_template=syn['BG2PNC.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9

conn = net.add_edges(source=backgroundOLM.nodes(), target=net.nodes(pop_name='OLM'),
              connection_rule=BG_to_OLM,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='BG2OLM.json',
              model_template=syn['BG2OLM.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float]) # places syn on basal at 0.9

conn = net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=BG_to_PV,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='BG2PV.json',
              model_template=syn['BG2PV.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float]) # places syn on basal at 0.9

# Build and save our networks

net.build()
net.save(output_dir='network')

tone.build()
tone.save_nodes(output_dir='network')

shock.build()
shock.save_nodes(output_dir='network')

backgroundPN_A.build()
backgroundPN_A.save_nodes(output_dir='network')

backgroundPN_C.build()
backgroundPN_C.save_nodes(output_dir='network')

backgroundPV.build()
backgroundPV.save_nodes(output_dir='network')

backgroundOLM.build()
backgroundOLM.save_nodes(output_dir='network')

t_sim = 232500  # early extinction time is 232500 sensitization time is 40000
print("stim time is set to %s" % t_sim)


#build_env_bionet(base_dir='./',
#                 network_dir='./network',
#                 tstop=t_sim, dt=0.1,
#                 report_vars=['v'],
#                 spikes_inputs=[('tone', './12_cell_inputs/tone_spikes.csv'),
#                                ('shock', './12_cell_inputs/shock_spikes.csv'),
#                                ('bg_pn', '12_cell_inputs/bg_pn_spikes.h5'),
#                                ('bg_pv', '12_cell_inputs/bg_pv_spikes.h5'),
#                                ('bg_olm', '12_cell_inputs/bg_olm_spikes.h5')],
#                 components_dir='biophys_components',
#                 config_file='config.json',
#                 compile_mechanisms=False)

psg = PoissonSpikeGenerator(population='tone')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=2,    # 1 spike every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/tone_background.h5')

print('Number of background spikes for tone: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_pn_a')
psg.add(node_ids=range(5),  # need same number as cells
        firing_rate=6,    # 1 spike every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pn_a_spikes.h5')

print('Number of background spikes for PN_A: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_pn_c')
psg.add(node_ids=range(3),  # need same number as cells
        firing_rate=2,    # 1 spike every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pn_c_spikes.h5')

print('Number of background spikes for PN_C: {}'.format(psg.n_spikes()))


psg = PoissonSpikeGenerator(population='bg_pv')
psg.add(node_ids=range(2),  # need same number as cells
        firing_rate=7.7,    # 8 spikes every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pv_spikes.h5')

print('Number of background spikes for PV: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_olm')
psg.add(node_ids=range(2),  # need same number as cells
        firing_rate=8.5,    # 8 spikes every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_olm_spikes.h5')

print('Number of background spikes for OLMM: {}'.format(psg.n_spikes()))
