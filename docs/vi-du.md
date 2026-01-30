{{Short description|Type of computer communication interface}}
[[File:Dual Core Generic.svg|thumb|Within a [[multi-core processor]], the [[back-side bus]] is often internal, with front-side bus for external communication.]]

The '''front-side bus''' ('''FSB''') is a computer communication interface ([[bus (computing)|bus]]) that was often used in [[Intel]]-chip-based computers during the 1990s and 2000s.  The EV6 bus served the same function for competing AMD CPUs. Both typically carry data between the [[central processing unit]] (CPU) and a memory controller hub, known as the [[Northbridge (computing)|northbridge]].<ref name="pcs">{{cite book |url=https://archive.org/details/upgradingrepair100muel |url-access=registration |title=Upgrading and repairing PCs |author=Scott Mueller |edition=15th |publisher=Que Publishing |year=2003 |isbn=978-0-7897-2974-3 |page=[https://archive.org/details/upgradingrepair100muel/page/314 314]}}</ref>

Depending on the implementation, some computers may also have a [[back-side bus]] that connects the CPU to the [[CPU cache|cache]]. This bus and the cache connected to it are faster than accessing the system memory (or RAM) via the front-side bus. The speed of the front side bus is often used as an important measure of the performance of a computer.

The original front-side bus architecture was replaced by [[HyperTransport]], [[Intel QuickPath Interconnect]], and [[Direct Media Interface]], followed by [[Intel Ultra Path Interconnect]] and AMD's [[Infinity Fabric]].

==History==
The term came into use by Intel Corporation about the time the [[Pentium Pro]] and [[Pentium II]] products were announced, in the 1990s.

"Front side" refers to the external interface from the processor to the rest of the computer system, as opposed to the back side, where the [[back-side bus]] connects the cache (and potentially other CPUs).<ref name="intel">{{cite web |title= Introduction to Intel Architecture: The Basics |author= Todd Langley and Rob Kowalczyk |date= January 2009 |url= ftp://download.intel.com/design/intarch/PAPERS/321087.pdf |publisher= Intel Corporation |work= White paper |archive-url= https://web.archive.org/web/20090712091351/http://download.intel.com:80/design/intarch/papers/321087.pdf |archive-date= 2009-07-12 |url-status= dead |access-date= May 28, 2011 }}</ref>

A front-side bus (FSB) is mostly used on PC-related [[motherboard]]s (including personal computers and servers). They are seldom used in [[embedded system]]s or similar small computers. The FSB design was a performance improvement over the single [[system bus]] designs of the previous decades, but these front-side buses are sometimes referred to as the "system bus".

Front-side buses usually connect the CPU and the rest of the hardware via a [[chipset]], which Intel implemented as a [[Northbridge (computing)|northbridge]] and a [[Southbridge (computing)|southbridge]]. Other buses like the [[Peripheral Component Interconnect]] (PCI), [[Accelerated Graphics Port]] (AGP), and memory buses all connect to the chipset in order for data to flow between the connected devices. These secondary system buses usually run at speeds derived from the front-side bus clock, but are not necessarily [[Synchronization (computer science)|synchronized]] to it.

In response to [[Advanced Micro Devices|AMD]]'s [[Torrenza]] initiative, Intel opened its FSB CPU socket to third party devices.<ref>{{cite news |title= Intel opens up its front side bus to the world+dog: IDF Spring 007 Xilinx heralds the bombshell |url=  http://www.theinquirer.net/inquirer/news/1044635/intel-bus-world-dog |archive-url=  https://web.archive.org/web/20121007164914/http://www.theinquirer.net/inquirer/news/1044635/intel-bus-world-dog |url-status=  unfit |archive-date=  October 7, 2012 |author= Charlie Demerjian |date= April 17, 2007 |work= The Inquirer |access-date= May 28, 2011 }}</ref>
Prior to this announcement, made in Spring 2007 at [[Intel Developer Forum]] in Beijing, Intel had very closely guarded who had access to the FSB, only allowing Intel processors in the CPU socket. The first example was [[field-programmable gate array]] (FPGA) co-processors, a result of collaboration between Intel-[[Xilinx]]-[[Nallatech]]<ref>{{cite news |title= Nallatech Launches Early Access Program for the Industry's First FSB-FPGA Module |date= September 18, 2007 |work= Business Wire news release |publisher= Nallatech |url= http://www.businesswire.com/news/home/20070918006506/en/Nallatech-TM-Launches-Early-Access-Program-Industrys |access-date= June 14, 2011 }}</ref> and Intel-[[Altera]]-XtremeData (which shipped in 2008).<ref>{{cite news |title= XtremeData Offers Stratix III FPGA-Based Intel FSB Module |date= September 18, 2007 |work= Business Wire news release |publisher= Chip Design magazine |url= http://chipdesignmag.com/display.php?articleId=2380 |access-date= June 14, 2011 |archive-url= https://web.archive.org/web/20110723190604/http://chipdesignmag.com/display.php?articleId=2380 |archive-date= July 23, 2011 |url-status= dead }}</ref><ref>{{cite news |title= High fiber diet gives Intel 'regularity' needed to beat AMD |url= https://www.theregister.co.uk/2007/04/17/intel_idf_serverstuff/ |author=  Ashlee Vance |author-link=Ashlee Vance |date= April 17, 2007 |work= The Register |access-date= May 28, 2011 }}</ref><ref>{{cite news |title=XtremeData Begins Shipping 1066 MHz Altera Stratix III FPGA-Based Intel FSB Module |date= June 17, 2008 |work= Business Wire news release |publisher= XtremeData |url= http://www.businesswire.com/news/home/20080617005298/en/XtremeData-Begins-Shipping-1066-MHz-Altera-Stratix  |access-date= June 14, 2011 }}</ref>

==Related component speeds==

[[File:Motherboard diagram.svg|thumb|300px|A typical chipset layout from the Pentium II/III era]]

===CPU===

The [[frequency]] at which a processor (CPU) operates is determined by applying a clock multiplier to the front-side bus (FSB) speed in some cases. For example, a processor running at 3200 [[Megahertz|MHz]] might be using a 400&nbsp;MHz FSB. This means there is an internal [[CPU multiplier|clock multiplier]] setting (also called bus/core ratio) of 8. That is, the CPU is set to run at 8 times the frequency of the front-side bus: 400&nbsp;MHz × 8 = 3200&nbsp;MHz. Different CPU speeds are achieved by varying either the FSB frequency or the CPU multiplier, this is referred to as [[overclocking]] or [[underclocking]].

===Memory===

{{see also | Memory divider}}

Setting an FSB speed is related directly to the speed grade of memory a system must use. The memory bus connects the northbridge and RAM, just as the front-side bus connects the CPU and northbridge. Often, these two buses must operate at the same frequency. Increasing the front-side bus to 450&nbsp;MHz in most cases also means running the memory at 450&nbsp;MHz.

In newer systems, it is possible to see memory ratios of "4:5" and the like. The memory will run 5/4 times as fast as the FSB in this situation, meaning a 400&nbsp;MHz bus can run with the memory at 500&nbsp;MHz. This is often referred to as an 'asynchronous' system. Due to differences in CPU and system architecture, overall system performance can vary in unexpected ways with different FSB-to-memory ratios.

In image, audio, video, gaming, [[Field-programmable gate array|FPGA]] synthesis and scientific applications that perform a small amount of work on each element of a large [[data set]], FSB speed becomes a major performance issue. A slow FSB will cause the CPU to spend significant amounts of time waiting for data to arrive from [[random-access memory|system memory]]. However, if the computations involving each element are more complex, the processor will spend longer performing these; therefore, the FSB will be able to keep pace because the rate at which the memory is accessed is reduced.

===Peripheral buses===

Similar to the memory bus, the PCI and AGP buses can also be run asynchronously from the front-side bus. In older systems, these buses are operated at a set fraction of the front-side bus frequency. This fraction was set by the [[BIOS]]. In newer systems, the PCI, AGP, and [[PCI Express]] peripheral buses often receive their own [[clock signal]]s, which eliminates their dependence on the front-side bus for timing.

===Overclocking===

{{main | Overclocking}}{{Update|part=section|date=September 2025|reason=Methods described are a bit old (c. 2010-style)}}
[[Overclocking]] is the practice of making computer components operate beyond their stock performance levels by manipulating the frequencies at which the component is set to run, and, when necessary, modifying the voltage sent to the component to allow it to operate at these higher frequencies with more stability.

Many motherboards allow the user to manually set the clock multiplier and FSB settings by changing [[jumper (computing)|jumper]]s or BIOS settings. Almost all CPU manufacturers now "lock" a preset multiplier setting into the chip. It is possible to unlock some locked CPUs; for instance, some AMD [[Athlon]] processors can be unlocked by connecting [[electrical contact]]s across points on the CPU's surface.  Some other processors from AMD and Intel are unlocked from the factory and labeled as an "enthusiast-grade" processors by end users and retailers because of this feature.  For all processors, increasing the FSB speed can be done to boost processing speed by reducing [[latency (engineering)|latency]] between CPU and the northbridge.

This practice pushes components beyond their specifications and may cause erratic behavior, overheating or premature failure. Even if the computer appears to run normally, problems may appear under a heavy load. Most [[Personal computer|PC]]s purchased from retailers or manufacturers, such as [[Hewlett-Packard]] or [[Dell]], do not allow the user to change the multiplier or FSB settings due to the probability of erratic behavior or failure.  Motherboards purchased separately to build a custom machine are more likely to allow the user to edit the multiplier and FSB settings in the PC's BIOS.

==Evolution==

The front-side bus had the advantage of high flexibility and low cost when it was first designed. Simple [[symmetric multiprocessor]]s place a number of CPUs on a shared FSB, though performance could not scale linearly due to bandwidth [[wikt:bottleneck|bottlenecks]].

The front-side bus was used in all [[Intel Atom]], [[Celeron]], [[Intel P5 (microarchitecture)|Pentium]], [[Core 2]], and [[Xeon]] processor models through about 2008<ref>{{cite web | url=https://www.anandtech.com/show/2458 | archive-url=https://web.archive.org/web/20100713115156/http://www.anandtech.com/show/2458 | url-status=dead | archive-date=July 13, 2010 | title=Intel X38 Tango – is High FSB Overclocking Worth It? }}</ref> and was eliminated in 2009.<ref>{{cite web | url=https://www.guru3d.com/review/core-i7-975-review/page-4/ | title=Core i7 975 review (Page 4) | date=2 June 2009 }}</ref> Originally, this bus was a central connecting point for all system devices and the CPU.

The potential of a faster CPU is wasted if it cannot fetch instructions and data as quickly as it can execute them. The CPU may spend significant time idle while waiting to read or write data in main memory, and high-performance processors therefore require high bandwidth and low latency access to memory. The front-side bus was criticized by [[AMD]] as being an old and slow technology that limits system performance.<ref>{{cite web |title= AMD HyperTransport Bus: Transport Your Application to Hyper Performance |date= September 29, 2003 |author= Allan McNaughton |publisher= AMD |url= http://developer.amd.com/documentation/articles/Pages/929200370.aspx |access-date= June 14, 2011 |archive-url= https://web.archive.org/web/20120325070619/http://developer.amd.com/documentation/articles/Pages/929200370.aspx |archive-date= March 25, 2012 |url-status= dead }}</ref>

More modern designs use point-to-point and serial connections like AMD's [[HyperTransport]] and Intel's [[Direct Media Interface|DMI 2.0]] or [[Intel QuickPath Interconnect|QuickPath Interconnect]] (QPI). These implementations remove the traditional [[Northbridge (computing)|northbridge]] in favor of a direct link from the CPU to the system memory, high-speed peripherals, and the [[Platform Controller Hub]], [[Southbridge (computing)|southbridge]] or I/O controller.<ref name="QPI">{{cite web |title= An Introduction to the Intel QuickPath Interconnect |date= January 30, 2009 |publisher= Intel Corporation |url= http://www.intel.com/technology/quickpath/introduction.pdf |access-date= June 14, 2011 }}</ref><ref>{{cite web | url=https://arstechnica.com/gadgets/2009/09/intel-launches-all-new-pc-architecture-with-core-i5i7-cpus/ | title=Intel launches all-new PC architecture with Core i5/I7 CPUs | date=8 September 2009 }}</ref><ref>{{cite web | url=https://www.guru3d.com/review/core-i7-975-review/page-4/ | title=Core i7 975 review (Page 4) | date=2 June 2009 }}</ref>

In a traditional architecture, the front-side bus served as the immediate data link between the CPU and all other devices in the system, including main memory. In HyperTransport- and QPI-based systems, system memory is accessed independently by means of a [[memory controller]] integrated into the CPU, leaving the bandwidth on the HyperTransport or QPI link for other uses. This increases the complexity of the CPU design but offers greater throughput as well as superior scaling in multiprocessor systems.

==Transfer rates==

The [[Bandwidth (computing)|bandwidth]] or maximum theoretical throughput of the front-side bus is determined by the product of the width of its data path, its [[Clock rate|clock frequency]] (cycles per second) and the number of data transfers it performs per clock cycle. For example, a 64-[[bit]] (8-[[byte]]) wide FSB operating at a frequency of 100&nbsp;MHz that performs 4 transfers per cycle has a bandwidth of 3200 [[megabytes per second]] (MB/s):

:8 bytes/transfer × 100 MHz × 4 transfers/cycle = 3200 MB/s

The number of transfers per [[Cycles per instruction|clock cycle]] depends on the technology used. For example, [[GTL+]] performs 1 transfer/cycle, [[Alpha_21264#External_interface|EV6]] 2 transfers/cycle, and [[AGTL+]] 4 transfers/cycle. Intel calls the technique of four transfers per cycle [[Quad Data Rate|Quad Pumping]].

Many manufacturers publish the frequency of the front-side bus in MHz, but marketing materials often list the theoretical effective signaling rate (which is commonly called [[Transfer (computing)|megatransfer]]s per second or MT/s). For example, if a motherboard (or processor) has its bus set at 200&nbsp;MHz and performs 4 transfers per clock cycle, the FSB is rated at 800 MT/s.

The specifications of several generations of popular processors are indicated below.

===Intel processors===

{|class="wikitable"
! CPU !! FSB frequency<br/> (MHz) !! Transfers<br/> per cycle !! Bus width !! Transfer rate<br/> (MB/s)
|-
| [http://cpu-data.info/index.php?gr=135&lng=1 Pentium] || 50–66 || 1 || 64-bit || 400–528
|-
| [http://www.cpu-collection.de/?tn=0&l0=co&l1=Intel&l2=Pentium+OverDrive Pentium Overdrive] || 25–66 || 1 || 32 or 64-bit || 200–528
|-
| [http://ark.intel.com/products/family/2024 Pentium Pro] || 60 / 66 || 1 || 64-bit || 480–528
|-
| [http://cpu-data.info/index.php?gr=135&lng=1 Pentium MMX] || 60 / 66 || 1 || 64-bit || 480–528
|-
| [http://cpu-data.info/index.php?gr=137&lng=1 Pentium MMX Overdrive] || 50 / 60 / 66 || 1 || 64-bit || 400–528
|-
| [http://ark.intel.com/products/family/583 Pentium II] || 66 / 100 || 1 || 64-bit || 528 / 800
|-
| [http://ark.intel.com/products/family/2023 Pentium II Xeon] || 100 || 1 || 64-bit || 800
|-
| [http://www.cpu-world.com/CPUs/Pentium-II/Intel-Pentium%20II%20Overdrive%20333%20-%20PODP66X333%20%28UBPODP66X333%29.html Pentium II Overdrive] || 60 / 66 || 1 || 64-bit || 480–528
|-
| [http://ark.intel.com/products/family/590 Pentium III] || 100 / 133 || 1 || 64-bit || 800 / 1064
|-
| [http://ark.intel.com/products/family/590 Pentium III Xeon] || 100 / 133 || 1 || 64-bit || 800 / 1064
|-
| [http://cpu-data.info/index.php?gr=113&lng=1 Pentium III-M] || 100 / 133 || 1 || 64-bit || 800 / 1064
|-
| [http://ark.intel.com/products/family/581 Pentium 4] || 100 / 133 || 4 || 64-bit || 3200–4256
|-
| [http://cpu-data.info/index.php?gr=117&lng=1 Pentium 4-M] || 100 || 4 || 64-bit || 3200
|-
| [http://ark.intel.com/products/family/581 Pentium 4 HT] || 133 / 200 || 4 || 64-bit || 4256 / 6400
|-
| [http://ark.intel.com/products/family/581 Pentium 4 HT Extreme Edition] || 200 / 266 || 4 || 64-bit || 6400 / 8512
|-
| [http://ark.intel.com/products/family/7944 Pentium D] || 133 / 200 || 4 || 64-bit || 4256–6400
|-
| [http://cpu-data.info/index.php?gr=123&lng=1 Pentium Extreme Edition] || 200 / 266 || 4 || 64-bit || 6400 / 8512
|-
| [http://cpu-data.info/index.php?gr=124&lng=1 Pentium M] || 100 / 133 || 4 || 64-bit || 3200 / 4256
|-
| [http://cpu-data.info/index.php?gr=122&lng=1 Pentium Dual-Core] || 200 / 266 || 4 || 64-bit || 6400 / 8512
|-
| [http://cpu-data.info/index.php?gr=140&lng=1 Pentium Dual-Core Mobile] || 133–200 || 4 || 64-bit || 6400–8512
|-
| [http://ark.intel.com/products/family/288 Celeron] || 66–200 || 1–4 || 64-bit || 528–6400
|-
| [http://ark.intel.com/products/family/43401 Celeron Mobile] || 133–200 || 1–4 || 64-bit || 4256–6400
|-
| [http://ark.intel.com/products/family/5263 Celeron D] || 133 || 4 || 64-bit || 4256
|-
| [http://ark.intel.com/products/family/3799 Celeron M] || 66–200 || 1–4 || 64-bit || 528–6400
|-
| [http://cpu-data.info/index.php?gr=102&lng=1 Celeron Dual-Core] || 200 || 4 || 64-bit || 6400
|-
| [http://cpu-data.info/index.php?gr=142&lng=1 Celeron Dual-Core Mobile] || 133–200 || 4 || 64-bit || 4256–6400
|-
| [http://cpu-data.info/index.php?gr=150&lng=1 Itanium] || 133 || 2 || 64-bit || 2133
|-
| [http://www.cpu-world.com/CPUs/Itanium_2/index.html Itanium 2] || 200–333 || 2 || 128-bit || 6400–10666
|-
| [http://www.cpu-world.com/CPUs/Xeon/index.html Xeon] || 100–400 || 4 || 64-bit || 3200–12800
|-
| [http://ark.intel.com/products/family/18995 Core Solo] || 133 / 166 || 4 || 64-bit || 4256 / 5312
|-
| [http://ark.intel.com/products/family/22731 Core Duo] || 133 / 166 || 4 || 64-bit || 4256 / 5312
|-
| [http://ark.intel.com/products/family/32257 Core 2 Solo] || 133–200 || 4 || 64-bit || 4256–6400
|-
| [http://ark.intel.com/products/family/26547 Core 2 Duo] || 200–333 || 4 || 64-bit || 6400–10656
|-
| [http://ark.intel.com/products/family/26548 Core 2 Duo Mobile] || 133–266 || 4 || 64-bit || 4256–8512
|-
| [http://ark.intel.com/products/family/28398 Core 2 Quad] || 266 / 333 || 4 || 64-bit || 8512 / 10656
|-
| [http://ark.intel.com/products/family/37361 Core 2 Quad Mobile] || 266 || 4 || 64-bit || 8512
|-
| [http://ark.intel.com/products/family/34522 Core 2 Extreme] || 266–400 || 4 || 64-bit || 8512–12800
|-
| [http://ark.intel.com/products/family/34520 Core 2 Extreme Mobile] || 200 / 266 || 4 || 64-bit || 6400 / 8512
|-
| [http://ark.intel.com/products/family/29035 Atom] || 100–166 || 4 || 64-bit || 3200–5312
|}

===AMD processors===

{|class="wikitable"
! CPU !! FSB frequency<br/> (MHz) !! Transfers<br/> per cycle !! Bus width !! Transfer rate<br/> (MB/s)
|-
| [http://cpu-data.info/index.php?gr=13&lng=1 K5] || 50–66 || 1 || 64-bit || 400–528
|-
| [http://cpu-data.info/index.php?gr=14&lng=1 K6] || 66 || 1 || 64-bit || 528
|-
| [http://cpu-data.info/index.php?gr=15&lng=1 K6-II] || 66–100 || 1 || 64-bit || 528–800
|-
| [http://cpu-data.info/index.php?gr=16&lng=1 K6-III] || 66 / 100 || 1 || 64-bit || 528–800
|-
| [http://cpu-data.info/index.php?gr=1&lng=1 Athlon] || 100 / 133 || 2 || 64-bit || 1600–2128
|-
| [http://cpu-data.info/index.php?gr=8&lng=1 Athlon XP] || 100 / 133 / 166 / 200 || 2 || 64-bit || 1600–3200
|-
| [http://cpu-data.info/index.php?gr=7&lng=1 Athlon MP] || 100 / 133 || 2 || 64-bit || 1600–2128
|-
| [http://www.cpu-world.com/CPUs/K7/TYPE-Mobile%20Athlon%204.html Mobile Athlon 4] || 100 || 2 || 64-bit || 1600
|-
| [http://cpu-data.info/index.php?gr=9&lng=1 Athlon XP-M] || 100 / 133 || 2 || 64-bit || 1600–2128
|-
| [http://cpu-data.info/index.php?gr=10&lng=1 Duron] || 100 / 133 || 2 || 64-bit || 1600–2128
|-
| [http://cpu-data.info/index.php?gr=24&lng=1 Sempron] || 166 / 200 || 2 || 64-bit || 2656–3200
|}

==References==
{{reflist}}

{{Computer-bus}}

{{DEFAULTSORT:Front-Side Bus}}
[[Category:Computer buses]]
[[Category:Motherboard]]
