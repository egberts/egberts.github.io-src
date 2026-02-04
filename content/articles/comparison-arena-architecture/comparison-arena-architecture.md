Title: Comparison of Arena Architecture in malloc()
Date: 2026-01-20T08:53
Status: published
Tags: comparison, malloc, arena
Category: research
summary: A comparison of arena architecture in malloc().

Memory Allocation
=================

Problems
--------

Limit Memory Allocation (if not necessary)

Multithreaded programs often do not scale because the heap is a
bottleneck.

When multiple threads simultaneously allocate or deallocate memory from
the allocator, the allocator will serialize them. Programs making
intensive use of the allocator actually slow down as the number of
processors increases.

Malloc (libc) is the worst memory allocation API to use.

Programs should avoid, if possible, allocating/deallocating memory too
often and in particular whenever a packet is received.

In the Linux kernel there are available kernel/driver patches for
recycling skbuff (kernel memory used to store incoming/outgoing
packets).

Using PF\_RING (into the driver) for copying packets from the NIC to the
circular buffer without any memory allocation increases the capture
performance (around 10%) and reduces congestion issues.

Design Evolution
================

Basic design of malloc() is to dynamically pre-allocate a pool of memory
from the OS in which applications can then take smaller pieces from.
malloc() is a standard API having a choice of different allocation
algorithms and to mitigate the expensive OS system calls (typically done
at program initialization time) during allocation of its system memory.
The first memory allocation scheme started with a stack-based memory
allocation.

Next came the dynamic-based memory allocation scheme where linked-list
and bucket-heap mechanism are used to divide the private-heap using size
class approach.

Soon, garbage collection algorithm introduced the initial backend of the
memory allocation scheme. Frontend covers the usual `malloc()` API, et
al.

In 2006, a third pool was introduced (after operating system memory pool
and library-based memory pool) called the "arena". Arena is a
jemalloc-term and is intended to deal with different memory types such
as different-speed memory bank or NUMA-architecture, as well as memory
tied to specific to each of the multiple CPU core or even CPU infinity.

Frontend Evolution
------------------

Frontend manages the memory being given to the application.

Within the frontend of the memory allocation system, the evolution went
in the following order:

1. link-list free space
2. heap-bucket size classes (eliminating an object header)
3. (Process) Owner encoding
4. single core local allocation buffers (CLABs)
5. Epoch encoding
6. Large-size class memory block by direct mmap()
7. Hazard pointers (safe memory reclamation for lock-free objects) (M.M. Michael, 2004)
8. Arena memory pool (CPU/core and thread, separately)
9. thread-specific local allocation buffers (TLABs)
10. constant-time modulo synchronization (early return to OS pool, or FreeBSD madvise call)

Backend Evolution
-----------------

Backend of the memory allocation system manages the empty, straggling,
fragmented or no-longer used memory blocks back to the OS (thereby
reducing RSS).

* Pool semantic: Remote f-list encoding, using Treiber stack), (R.K.  Treiber,  1986)
* buddy algorithm
* binary buddy algorithm
* BIPOP Table (span-based allocator)(S. Schneider, 2006) aka local free list and remote free list
* segment queue (Quasi-linearizability, Y. Afek, 2010)
* multi-core distributed queue (A. Haas, 2013)
* k-FIFO queue (T.A. Henzinger, 2013)

Competition
-----------

There are better ones out there that does not worsen as more threads/processes performs memory allocation system calls; they are listed in best-to-good performance order​\[seed with source\]:

Comparison of malloc design
===========================

[jtable]
Allocator,Origin / Maintainer,Thread Safe,Per-Thread Cache,Multi-Arena / Heaps,Lock-Free Fast Path,NUMA Aware,Fragmentation Control,Notes
dlmalloc,Doug Lea,No,No,No,No,Low,Single global heap; basis for many later allocators
ptmalloc2 / ptmalloc3,glibc,Yes,Limited,Yes,No,Medium,glibc default; arena locks cause contention
glibc malloc (current),GNU,Yes,Limited,Yes,No,Medium,Wrapper around ptmalloc with tunables
jemalloc,FreeBSD / Meta,Yes,Yes,Yes,Partial,High,Thread-arena affinity reduces CAS contention
tcmalloc,Google,Yes,Yes,Yes,Partial,Medium-High,Per-CPU caches; central freelists still exist
mimalloc,Microsoft,Yes,Yes,Yes,Yes,High,Designed to minimize atomic ops and false sharing
Hoard,Emery Berger,Yes,Yes,Yes,Partial,Medium,Focus on scalability and false-sharing avoidance
[nedmalloc](https://www.nedprod.com/programs/portable/nedmalloc/),[NEDMALLOC](https://github.com/ned14/nedmalloc),Yes,Yes,Yes,No,Medium,dlmalloc-derived with thread caching
phkmalloc,FreeBSD,Yes,Yes,Yes,No,Medium,Early FreeBSD allocator family
libumem,Solaris,Yes,Yes,Yes,Yes,Medium-High,Solaris allocator with debugging and locality support
mtmalloc,Solaris,Yes,Yes,Yes,Yes,Medium,Solaris multithreaded allocator
snmalloc,Microsoft Research,Yes,Yes,Yes,Yes,High,NUMA-aware, security- and scalability-focused
lockless malloc (research),Academic / Experimental,Varies,Yes,Varies,Yes,Low,Often CAS-heavy; not production ready
[ltalloc](https://alextretyak.ru/ltalloc/),Academic,,,,,
[/jtable]

CAS, Atomic Contention Characteristics
----
CAS / Atomic Contention characteristics
[jtable]
Allocator,Estimated Atomics per alloc/free,Shared Cacheline Risk,CAS Contention Sensitivity,Notes
dlmalloc,High,High,Very High,Global structures and locks dominate
ptmalloc2 / ptmalloc3,Medium-High,High,High,Arena locks cause cacheline bouncing
glibc malloc (current),Medium-High,High,High,Wrapper around ptmalloc
jemalloc,Low,Low,Low,Arena-local metadata; minimal shared CAS
tcmalloc,Low-Medium,Medium,Medium,Per-CPU caches; central freelist CAS
mimalloc,Very Low,Very Low,Very Low,Designed to minimize atomic ops
Hoard,Medium,Medium,Medium,Reduces false sharing but still synchronized
nedmalloc,Medium,Medium,Medium,Thread caches reduce but don’t eliminate CAS
phkmalloc,Medium,Medium,Medium,Older FreeBSD design
libumem,Low,Low,Low,Lock-free fast paths on Solaris
mtmalloc,Low,Low,Low,Per-thread structures reduce atomic sharing
snmalloc,Very Low,Very Low,Very Low,Message-passing model avoids shared CAS
lockless malloc (research),High,High,High,Often CAS-heavy despite no locks
[/jtable]

NUMA, Memory Locality characteristics
---
NUMA / Memory Locality characteristics
[jtable]
Allocator,Explicit NUMA Support,First-Touch Friendly,Cross-NUMA Traffic Risk,Locality Preservation,Notes
dlmalloc,No,Yes,Very High,Poor,Single heap across nodes
ptmalloc2 / ptmalloc3,No,Partial,High,Fair,Arenas not NUMA-bound
glibc malloc (current),No,Partial,High,Fair,Relies on OS placement
jemalloc,Partial,Yes,Medium,Good,Optional NUMA arena tuning
tcmalloc,Limited,Yes,Medium,Fair,CPU caches not NUMA-aware
mimalloc,No,Yes,Low,Very Good,Strong thread locality
Hoard,No,Yes,Medium,Good,Per-processor heaps help
nedmalloc,No,Yes,Medium,Fair,Thread caches but global fallback
phkmalloc,Partial,Yes,Medium,Fair,Early locality optimizations
libumem,Yes,Yes,Low,Very Good,Solaris NUMA policies
mtmalloc,Yes,Yes,Low,Very Good,Designed for NUMA Solaris systems
snmalloc,Yes,Yes,Very Low,Excellent,NUMA-first architecture
lockless malloc (research),No,Varies,High,Poor,Locality rarely addressed
[/jtable]

Benchmark-Oriented Practical Performance
---
Benchmark-Oriented Practical Performance
[jtable]
Allocator,Small Alloc Throughput,Large Alloc Throughput,Latency Under Contention,Memory Overhead,Fragmentation Risk,Notes
dlmalloc,Low,Medium,Poor,Low,High,Not suitable for multithreaded loads
ptmalloc2 / ptmalloc3,Medium,Medium,Poor,Medium,Medium,glibc default
glibc malloc (current),Medium,Medium,Poor,Medium,Medium,Tunable but limited
jemalloc,High,High,Very Good,Medium-Low,Low,Excellent all-around allocator
tcmalloc,Very High,Medium,Good,Medium,Medium,Optimized for small objects
mimalloc,High,High,Excellent,Low,Low,Great latency predictability
Hoard,Medium,Medium,Good,Medium,Low,Designed for scalability
nedmalloc,Medium,Medium,Fair,Medium,Medium,Older but usable
phkmalloc,Medium,Medium,Fair,Medium,Medium,Historical FreeBSD allocator
libumem,High,Medium,Very Good,Medium,Low,Strong debugging support
mtmalloc,High,Medium,Very Good,Medium,Low,Enterprise Solaris workloads
snmalloc,High,High,Excellent,Low,Very Low,Security + scalability focus
lockless malloc (research),Varies,Varies,Poor,Low,High,Often unstable in practice
[/jtable]

Allocator Recommendation
---
Allocator Recommendation
[jtable]
Workload Type,Primary Bottleneck,Key Risks,Recommended Allocator,Why It Fits,Alternatives,Avoid
Highly Contended Multithreaded,Atomic/CAS latency,Cacheline bouncing,jemalloc,Multi-arena + thread affinity minimizes shared CAS,mimalloc,snmalloc,dlmalloc ptmalloc
Low-Latency / Tail-Sensitive,Allocation jitter,Lock convoying,mimalloc,Very low atomic count and predictable fast paths,snmalloc,jemalloc,tcmalloc
NUMA / Multi-Socket Servers,Cross-node memory access,Remote cache ownership,snmalloc,Explicit NUMA awareness and locality control,jemalloc (NUMA tuned),libumem,glibc malloc
Small Object Heavy (RPC / Web),Allocator throughput,Central freelist contention,tcmalloc,Per-CPU caches optimized for small allocs,jemalloc,mimalloc,ptmalloc
Large Object / Mixed Sizes,Fragmentation,TLB pressure,jemalloc,Excellent fragmentation control and extent management,mimalloc,glibc malloc
False-Sharing Sensitive,Cacheline ping-pong,Metadata sharing,Hoard,Designed to avoid false sharing,jemalloc,mimalloc,dlmalloc
Security-Hardened,Use-after-free exploits,Heap corruption,snmalloc,Isolation + security invariants,mimalloc (secure),ptmalloc
Debugging / Leak Detection,Memory misuse visibility,Silent corruption,libumem,Strong runtime diagnostics,jemalloc (profiling),tcmalloc
Embedded / Low Memory,Footprint size,Overhead,dlmalloc,Small and simple if single-threaded,nedmalloc,jemalloc
Real-Time / Deterministic,Unbounded latency,OS interference,mimalloc,Low variance fast paths,snmalloc,jemalloc,tcmalloc
HPC / Scientific NUMA,Memory bandwidth,Remote NUMA hits,snmalloc,NUMA-first design and low CAS traffic,jemalloc + mbind,glibc malloc
Legacy / Compatibility,ABI stability,Toolchain issues,glibc malloc,System default and safest fallback,ptmalloc,
[/jtable]

Decision Chart for Malloc Selection
----

<p align="center">

<div class="m-image">
  <img src="{attach}images/malloc-decision-supertree.png"
    class="m-image"
    alt="Decision Supertree for Malloc Selection"
    max-height=100% max-width=100% />
</div>
</p>

[Graphviz DOT file]({attach}images/malloc-decision-supertree.dot)


* [http://www.phrack.org/issues.html?issue=57&id=8#article]
* [https://sploitfun.wordpress.com/2015/03/04/heap-overflow-using-malloc-maleficarum/]
* [http://phrack.org/issues/66/10.html]

References
==========
* R. J. Maher, Problems of storage allocation in a multiprocessor multiprogrammed system, Communications of the ACM, 4(10):421-422, October 1961
* A fast storage allocator, Kenneth C. Knowlton, Communications of the ACM, 8(10):623-625, October 1965.

* Statistical properties of the buddy system, P.W. Purdom and S. M. Stigler, Journal of the ACM, 17(4):683-697, October 1970
* Statistical investigation of three storage allocation algorithms, P. W. Purdom, S. M. Stigler, and Tat-Ong Cheam, BIT, 11:187-195, 1971.
* A note on an optimal-fit method for dynamic allocation of storage, J. A. Campbell, Computer Journal, 14(1):7-9, February 1971.
* Worst-case analysis of memory allocation algorithms, M. R. Garey, R. L. Graham, and J. D. Ullman, In Fourth Annual ACM Symposium on the Theory of Computing, 1972
* A class of dynamic memory allocation algorithms, D. S. Hirschberg, Communications of the ACM, 16(10):615-618, October 1973
* Dynamic storage allocations of arbitrary sized segments, J. S. Fenton and D. W. Payne, In Proc. IFIPS, pages 344-348, 1974
* [Worst-case of Memory Allocation Algorithms, Garey 1972](https://dl.acm.org/doi/pdf/10.1145/800152.804907)
* A simplified recombination scheme for the Fibonacci buddy system, B. Cranston and R. Thomas, Communications of the ACM, 18(6):331-332, July 1975.
* Buddy systems, J. L. Peterson and T. A. Norman, Communications of the ACM, 20(6):421-431, June 1977.
* Worst case fragmentation of first fit and best fit storage allocation strategies, J. M. Robson, Computer Journal, 20(3):242-244, August 1977.
* Fast-fit: A new hierarchical dynamic storage allocation technique, M. Tadman, Master’s thesis, UC Irvine, Computer Science Dept., 1978.
* The double buddy-system, David S. Wise, Technical Report 79, Computer Science Department, Indiana University, Bloomington, Indiana, December 1978

* Memory fragmentation in buddy methods for dynamic storage allocation, A. G. Bromley, Acta Informatica, 14(2):107-117, August 1980.
* Optimal fit of arbitrary sized segments, Ivor P. Page, Computer Journal, 25(1), January 1982.
* Parallelizing the usual buddy algorithm, A. Gottlieb and J. Wilson, Technical Report System Software Note 37, Courant Institute, New York University, 1982.
* Fast fits: New methods for dynamic storage allocation, C. J. Stephenson, In Proceedings of the Ninth Symposium on Operating Systems Principles, pages 30-32, Bretton Woods, New Hampshire, October 1983. ACM Press. Published as Operating Systems Review 17(5), October 1983.
* On the asymptotic optimality of first-fit storage allocation, E. G. Coffman, Jr., T. T. Kadota, and L. A.  Shepp, IEEE Transactions on Software Engineering, SE-11(2):235-239, February 1985.
* Efficient implementation of the first-fit strategy for dynamic storage alloca-
tion, R. Brent, ACM Transactions on Programming Languages and Systems, July 1989.
* Fast allocation and deallocation of memory based on object lifetimes, David R. Hanson, Software Practice and Experience, 20(1), January 1990.
* [Dynamic Storage Allocation: A Survey and Critical Review](https://www.cs.hmc.edu/~oneill/gc-library/Wilson-Alloc-Survey-1995.pdf), very useful chronological order of malloc(), 1995
* [The Memory Fragmentation Problem: Solved? Johnstone 1997](https://www.cs.tufts.edu/~nr/cs257/archive/paul-wilson/fragmentation.pdf)

* [A Memory Allocator](http://gee.cs.oswego.edu/dl/html/malloc.html), 2000
* [Solaris mtmalloc](https://web.archive.org/web/20111019163341/http://developers.sun.com/solaris/articles/multiproc/multiproc.html) (archived), 2003
* [Anatomy of a Program in Memory](https://manybutfinite.com/post/anatomy-of-a-program-in-memory/), 2009

* [A History of malloc](https://betathoughts.blogspot.com/2010/02/history-of-malloc.html), 2010
* [Heap and allocators](http://www.cs.dartmouth.edu/~sergey/cs108/2015/heaps-and-allocators.txt), 2015
* [Understanding glibc malloc](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc)
* [The Origins of Malloc](https://www.spinellis.gr/blog/20170914/), 2017
* [GrapheneOS hardened\_malloc](https://github.com/GrapheneOS/hardened_malloc), 2019

* [Simulation of High-Performance Memory Allocators, Risco-Martin](https://arxiv.org/pdf/2406.15776), 2024
