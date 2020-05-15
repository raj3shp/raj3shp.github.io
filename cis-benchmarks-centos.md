# Linux System Hardening With CIS Benchmarks 

### It's a great way to improve security posture

CIS Benchmarks are guidelines for various technology groups to safeguard systems against today’s evolving cyber threats. While it is important that you harden your system configuration to improve system's security posture, many compliance programs require it as a mandatory control. 
The PCI DSS requirement 2.2.c states
> Examine policies and interview personnel to verify that system configuration standards are applied when new systems are configured and verified as being in place before a system is installed on the network.

CIS benchmarks are very specific configuration guidelines that can help you harden the system configuration to prevent and detect cyber attacks. 

### They're great but not easy to achieve

Considering CIS benchmarks for CentOS 7, there is a huge list of configuration checks that must be passed to acheive full compliance with the CIS benchmark. Applying these to any system or an array of systems calls for lot of resources and time.

In the evolving tech industry, we're seeing more and more distributed team being formed for handling specific functions. System hardening naturally falls under the 'Security' umbrella. In large organizations, it would be quite daunting to justify need for making system configuration changes to thousands of servers because a list (like CIS benchmarks) told you so. 

### Prioritization is the key

The CIS benchmark list is long. Why would you overload the infrastructure teams with a long list of unjustified changes on top of their daily workload? We need a structured way to map CIS benchmarks with exploitation techniques in order to prioritize important benchmarks and avoid wasting time on unnecessary changes. CIS benchmarks are not to be followed exactly, you should pick the important ones that apply to security of your systems. The rest of the benchmarks can be either "accepted as risk" by mentioning a rational or  with some compensating controls.

What if we map the CIS controls with a security framework like [MITRE ATT@CK](https://attack.mitre.org/matrices/enterprise/linux/)? If we can map the entire framework to specific CIS benchmarks, we can use the framework to prioritize and justify implementation of CIS benchmarks critical for your security policy.


