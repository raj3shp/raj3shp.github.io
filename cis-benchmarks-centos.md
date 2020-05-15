# Doing CIS benchmakrs right



In this article we will focus on -
* Prioritizing benchmarks according to your security policies
* Relating CIS controls with MITRE ATTACK Framework

CIS Benchmarks are guidelines for various technology groups to safeguard systems against today’s evolving cyber threats. While it is important that you harden your systems to improve system's security posture, many compliance programs require it as a mandatory control. 
The PCI DSS requirement 2.2.c states
> Examine policies and interview personnel to verify that system configuration standards are applied when new systems are configured and verified as being in place before a system is installed on the network.

In the evolving tech industry, we're seeing more and more distributed team being formed for handling specific functions. System hardening naturally falls under the 'Security' umbrella. In large organizations, it would be quite daunting to justify need for making system configuration changes to thousands of servers because a list (like CIS benchmarks) told you so. Why would you overload the infrastructure teams with a long list of unjustified changes on top of their daily workload? We need a structured way to map CIS benchmarks with exploitation techniques in order to prioritize important benchmarks and avoid wasting time on unnecessary changes.

What if we map the CIS controls with a security framework like [MITRE ATT@CK](https://attack.mitre.org/matrices/enterprise/linux/)? If we can map the entire framework to specific CIS benchmarks, we can use the framework to prioritize and justify implementation of CIS benchmarks critical for your security policy.

CIS benchmarks are not to be followed exactly, you should pick the important ones that apply to security of your systems. The rest of the benchmarks can be accepted as risk by mentioning a rational preferrably with some compensating controls for that benchmark.

