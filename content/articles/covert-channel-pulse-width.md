title: Pulse-Width Covert Channel
date: 2004-02-01 01:03
updated: 2020-03-11 11:21
status: published
tags: pulse-width, covert channel, modulation, BER, TCP, algorithm
category: research
summary: How to communicate across without changing one bit in payload.

Historical Timeline
===================
I was in a large satellite project working on the [post-Vegas-variant]({filename}tcp-evolution/tcp-evolution.md) of TCP network protocol.

We were struggling with not only single-bit loss of the TCP channel, but those multi-bit and burst-bits data loss that is commonly found in a typical satellite links.

While we did formulate a fix for the burst-bits loss (TCP-SACK), the small thing tugged at the back of my mind about my prior work on 52-byte ATM site-to-site telephone hook-up that SONET payload offers.

There were delays in the site-to-site phone calls between ATM technicians (STILL).  And the variance of those delays is clustered in 4 time-interval groups ... neatly.  The analogue scope showed this four dirty "humps", so that is an unexpected pattern.  I asked for a digital trace from an ATM technician using a HP digital scope and downloaded it via HPIB interface.

Once I plotted these four time-delay groups, I converted it to a series of zeroes and ones.   And then rastered it on a 80x25 ANSI-colored screen, low and behold, a visual pattern was discerned.  Entropy was too low to be encrypted.

I never did get to completely decode the sequence as this ATM project was out-competed by Fujitsu ATM switch and my access to the proprietary data was then terminated.

An Idea Is Born
===============
Fast-forward to 2004, the Internet is at full-speed.  Much effort were put into encryption, digest, hash, and MAC; but not the hiding data in plain sight.  While I'm not the first (nor the last), but someone has to look into this a bit more.  [Barr Group](https://barrgroup.com/embedded-systems/how-to/pwm-pulse-width-modulation) did a first stab at this in 2001 but it was for motor control; PWM just hasn't been transcended across different technological domains yet.

Some might say hiding in plain sight is "security through obscurity".  I
maintain that this is "security through noise".  And feel that this will pretty
well lead to further work in area of quantum communication channels.

All of our data communication is done in the open (whether its encrypted or
not), it's open due to the fact that packet data has been sent ... openly for
anyone to pick up (encrypted or not).

What about the alternative to open data communication?  Is there such a thing?  An idea of hiding data within the data packet didn't take hold very well: too many different kinds of intrusion detection system can catch that.  What about the spatial timing between packets as a data carrier medium?  Is that even an option?

The basic idea is to encode information in a form of the group of different time duration between packets.   Sure, the latency of the application would be impacted, but this here is the Internet (and it's getting faster, and faster).

Defensive Stance
================

What would be a good defensive mechanism for such communication channel that
utilizes encoding timing interval between packets?

Well, that's an easy one: a specially-designed "waterfall" router that introduces sporadic but randomized packet delay in between each packets.  Even though "waterfall" is symphomatic of a DMZ bastion gateway, it remains to be the best kind of router in which to introduce such defensive mechanism into.

Offensive Countermeasure
========================

Assuming that such introduction of "waterfall" router is in place, what kind of
countermeasure can be deployed into such timing-based encoding channel?

That's even easier (said, than done):  soft-decision, interleaving non-block (continuous) error-correction coding was the selection that I've made back then.  Much later on, I've determined that we can supplant this with [Extended Binary Golay code](https://en.wikipedia.org/wiki/Binary_Golay_code) for 24-bits.

Work Done
=========

About 2 decades later, this guy already started down this path afer I've moved on; he calls it "[Steagonagraphic Packets](https://vimist.github.io/2019/01/30/Steganographic-Packets.html)".  But that's just the preliminary.

Post Analysis
=============

Took some time to figure out which kind of TCP channel is best suited for this
PWM-CC approach.

Multiple-Hop Compensator
------------------------

The biggest issue is the external variance of inter-packet delays introduced by
routers at each IP hop.  During my studies of a specific Nth hop in real
Internet, the variances are small and greatly shifts over longer period of time
(greater than its usually-short message transmission cycle).  This too can be
compensated for not just at a specific hop but for all hops that a TCP
connection traverses across.

Final Analysis
--------------

It is really easy to make the encoder (that introduces the carefully-crafted
data-encoded packet-delays).  It's only a couple of dozen lines of code.

The hard part is the analogue component to the decoding.  But that's the fun
part of having worked on this [Pulse-Width Modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation) Covert Channel approach.


References
==========
* [Vimist](https://vimist.github.io/2019/01/30/Steganographic-Packets.html)
* [Introduction to Pulse Width](https://barrgroup.com/embedded-systems/how-to/pwm-pulse-width-modulation)
* [Pulse-Width Modulation (Wikipedia)](https://en.wikipedia.org/wiki/Pulse-width_modulation)
