

from escpos.printer import Usb
from encodings import CodecRegistryError


text = """
CAN-BUS systems also play an important role in both modern factory automa-
tion processes and testing facilities. Since CAN design is based on distributed 
control principles, it has been effectively used in manufacturing facilities to connect 
the essential control systems dispersed throughout a plant. Through the use of 
human machine interfaces (HMIs), operator inputs can be translated into instruc-
tions that a programmable logic controller (PLC) dispatches onto the BUS, allowing 
the remote operation of equipment ranging from sensors to actuators. This process 
allows the testing of new input parameters prior to execution on specific equipment 
and is a viable option for increasing process safety [27]. Use of CAN on assembly 
lines as a quality check is also becoming more common and is especially important 
on a line manufacturing a customizable product. Certain specifications are pro-
grammed for each checkpoint of product assembly, which are then broadcast on the 
CAN between machines to provide quality validation for the operators throughout 
the manufacturing process. CAN-BUS is also a practical option for connecting secu-
rity and environmental control systems across a facility, due to both high bit-rate 
and inexpensive installation.
Aside from the role CAN-BUS plays in system-to-system communication 
within a vehicle, the serial network technology has also been integral in the advent 
of telematics. Telematics is a sector of information technology concerned with 
how data moves between machines over long distances. Incorporating telematics 
technology into a vehicle or fleet of vehicles provides the opportunity to utilize 
collected data outside the scope of an individual machine’s operation by integrating 
it into a server network for wider usage and analysis. While CAN-BUS is not the sole 
technology responsible for telematics, it serves an important role in communicating 
large quantities of data that are eventually converted into valuable information for 
end users.
Currently, CAN-BUS is used in autonomous vehicle development to gather data 
from all electronic control sensors and consolidate it onto a single network. By gath-
ering the data into a unified structure, the overall system controller can easily make 
decisions that affect multiple sub-systems at once. This data availability, combined 
with swift processing, is a key component in the safe operation of autonomous 
vehicles both on the open road and off-road. This centralized system data stream 
allows for advanced control of smart engine sensors, which provide more efficient 
management processes. The data handling capability of smart controllers is still an 
area in need of concentrated improvement. Present research is looking into robust 
solenoids and other embedded sensors to control valve timing, coolant flow rate, 
compression ratio, and other key processes in engine operation [52]. Integrated 
development of these smart controllers with CAN will be crucial to ensuring the 
safety of autonomous vehicle function execution and travel.
Since fuel consumption is primarily dependent on engine speed and torque, it 
is possible to reliably decrease emissions with the application of alternative driving 
techniques optimally suited to specific drive train design and implement load [54]. 
However, the plausibility of deriving accurate efficiency metric assessments is lim-
ited due to present data scarcity. Current methods for Life Cycle Assessment (LCA) 
studies provide unreliable results because average conditions, such as soil texture, 
field shape, soil moisture, implement transfer difference, and engine features, have 
traditionally been utilized in lieu of actual conditions to estimate environmental 
effects [55]. CAN is advantageously positioned to help address both the data defi-
ciency and inadequate LCA techniques, due to its data collection and communication 
strengths. It is possible, for example, that performance metrics could be improved 
through intelligent sensor solutions that can measure slippage and soil compaction at 
the wheels of a vehicle and attached implement [13, 54]. These sensors could com-
municate with sensors in the drivetrain to adjust the effective gearing ratio in real-
time, reducing soil compaction and preserving the long-term viability of the soil.
An example of an instrument that, when paired with CAN-BUS communica-
tion, could be useful in achieving such operational efficiency objectives are inertial 
measurement units (IMUs). An inertial measurement unit functions as a sophis-
ticated accelerometer/gyroscope combination. It boasts near zero drift between 
different operating conditions, and its use of magnetic fields allows it to double as 
an “electronic compass”. The IMU allows for communication across many different 
CAN-BUS networks to help the tractor, or any vehicle, make decisions about how to 
alter the driving style for the terrain to limit “dynamic pitch and roll” through open 
system communication [52]. While this specific system is not currently imple-
mented on tractors and other off-road vehicles, there is room for its introduction in 
the emerging field of agricultural autonomy.
Smart agriculture and digital farming practices have gained popularity in the 
previous decade. These techniques are precursors to a transformative implemen-
tation of information technology in the farming world. Going forward, more 
advanced software systems will use information collected from CAN communica-
tion devices to aid in the optimization of machinery designs and more accurate 
load, use-profile, and duty cycle representations of vehicles and implements [18]. 
Future applications for CAN-BUS technology include IoT, Edge Computing, and 
swarm machinery automation, as well as complex control of electrical and electric-
hybrid machinery.
IoT implementation in the agricultural sector has gained enormous traction in 
recent years, as a result of its high potential for cross-brand interoperability, scal-
ability, and traceability. The different types of IoT tools being applied are continu-
ing to evolve, increasing the overall adaptability and variety of available systems to 
end-users [56]. IoT systems are currently being implemented on vehicles from John 
Deere, Case New Holland (CNH), AGCO, and others. Future IoT device use on agri-
cultural equipment will likely be in conjunction with multiple on-board network 
systems. Local storage or cloud computing will be necessary to store and process 
the vast amount of data created by this potential technology [57]. Data processing 
on-board the vehicle, near the working equipment, is referred to as ‘edge comput-
ing’ [56, 58]. It is highly probable that agricultural vehicles will eventually be able 
to perform a variety of complex, agronomic tasks from a preprogrammed routing 
structure, through the combined utilization of both IoT and EC technologies.
In addition to on-vehicle IoT technologies, it is probable that field embedded 
(or in-situ) IoT sensors will also be able to communicate with larger on-farm 
networks [59]. Several of the previously discussed network configurations are 
possible whole-farm network options. These include cellular (4G, 5G, and beyond), 
Wi-Fi, ZigBee, and UWB. For example, real-time soil moisture can be obtained 
from field-based, connected sensors to create a variable-rate prescription map [60]. 
Utilized in conjunction with mobile soil penetrometer readings, an accurate map of 
soil compaction risk can be created. This could allow farmers to tailor their tillage 
operations to specific areas of the field, as well as control vehicle traffic.
Cutting-edge networking research is also being done with robotic and swarm 
machinery automation [61]. IoT technologies and improved connectivity will allow 
for the introduction of robotic swarm farming techniques. Swarm farming incor-
porates multiple, small-scale robotic platforms that perform farming operations 
autonomously in place of larger, manned agricultural equipment. This farming 
strategy, paired with a predetermined path-planning algorithm optimizing how the 
machines will navigate throughout the field, could allow for near-continuous field 
operation. Additional benefits could include a centralized command center that is 
controlled by a single system manager and a significant reduction in the need for 
skilled labor [62]. The possibility of substituting the modular vehicle design within 
swarm farming for traditional larger equipment will depend on cost, comparative 
system productivity, and accuracy. Farmers will demand a significant return on 
investment and the reliability that they have come to expect from their current 
machinery. A potential difficulty for CAN-based systems is the large bandwidth 
requirement for incoming and streaming data. Another potential challenge involves 
communication protocol differences between traditional CAN-BUS data and more 
memory intensive data collected from advanced machine systems, like perception 
engines and central processor-based codes [63]. Future developments in CAN-BUS 
technology should focus on addressing these weaknesses to improve adaptability to 
upcoming applications.
A major concern in the future of agricultural CAN use, machinery networking, 
and machine system automation is cybersecurity. Although increased digitization,
automation, and precision services have tremendous potential to establish sustain-
ability and profitability in farming systems, the influx of interconnected informa-
tion technology simultaneously opens the market up to new areas of susceptibility, 
security risks, and potential targeted cyber-attacks [58]. Mission-critical systems 
are becoming more reliant on internet connectivity, such as controlling farming 
implements remotely through the ISOBUS with linked management software. Local 
Area Networks (LANs) have become a requirement in smart farming to enable 
system/device access to the data and services that control their functions [64]. This 
increased dependence of agricultural operations on cyber-physical systems has led 
to the development of new, novel threats and challenges that can be analyzed in two 
categories: information technology and agricultural production [58].
From an informational technology standpoint, some of the main threats are 
unauthorized access of resources/databases under use of falsified identity, intercep-
tion of node data transfer, facility damage or downtime, malicious data attacks 
from malware, and compromised control systems to negatively impact decision-
making [58]. Due to the nature of modern networked food systems, targeted or 
accidental disruption of time-sensitive agricultural processes could have a signifi-
cant economic impact on a global scale. The threat of a concentrated hack on the 
agricultural sector has become more tangible with the analysis of cyber-security 
breaches in recent years, such as the 2017 infrastructure meltdown of Maersk ship-
ping [65]. The vulnerability of Wireless Local Area Networks (WLANs) to direct 
cyber-attacks is already a generally recognized problem across all industries [66]. 
Demonstration of the damage potential in a Denial of Service (DoS) attack has 
been shown in the research of Sontowski et al., by disrupting in-field sensors and 
obstructing device network connectivity in smart farm operations [67].
Though the hacking activities of malicious actors is a highlighted concern in 
cyber security, there are also a number of risks associated with agricultural produc-
tion that stem from physical layer vulnerabilities and limited user knowledge. The 
harsh environment in which agricultural equipment is used (including extreme 
weather conditions, dust concentration, and highly variable humidity/temperature 
fluctuation) can cause power failures or sensor damage [64]. Technology signal 
interference from other agricultural equipment, such as the high voltage pulses from 
Solar Insecticidal Lamps (SIL), can also lead to malfunctions and data loss [58].
However, one of the most common threats to cyber security is inadequate adop-
tion of safety procedures by farmers who lack full awareness of device functionality. 
From research conducted by Nikander et al., farmers are often ill-equipped with 
time and resources to build LANs with appropriate network equipment, topology 
expansion planning, and protection software/hardware [64]. This leads to networks 
that are at risk of system losses due to hardware issues and human error. The adop-
tion of countermeasures to security risks, such as authentication & access control, 
cryptography, key management, and intrusion detection systems, is dependent 
on end-users understanding the importance of cybersecurity, and better fail-safe 
mechanisms within hardware [58, 64]. These concerns highlight the importance of 
advancing security protocols in CAN-BUS systems, and it is likely that this will be a 
targeted focus in the future of CAN developments.

•  The establishment of international societies and standards positioned  
CAN-BUS as the leading serial network system in all vehicles.

•  CAN-BUS provides efficient and dependable communication pathways 
through front and back end context in messaging, error confinement, higher-
layer protocols, and subsystem differentiation.

•  CAN-BUS has revolutionized data collection and analysis in multiple indus-
tries, especially in the agricultural sector.

•  When paired with wired or wireless technologies, CAN is an advantageous 
communication pathway for expanding the reach of data communication 
beyond point source limitations.

•  Challenges for future CAN iterations include increasing bandwidth and secu-
rity measures, while decreasing latency and hardware vulnerabilities
"""


# p = Usb ( 0x0483, 0xa319)
# p = Usb ( 0x04b8, 0x0202)

p = Usb ( 0x0a5f, 0x010e)

p.text ( '\n')
p.text ( text)
p.text ( '\n')
p.cut ()

