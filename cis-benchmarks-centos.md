# Linux System Hardening With CIS Benchmarks 

### It's a great way to improve security posture

CIS Benchmarks are guidelines for various technology groups to safeguard systems against today’s evolving cyber threats. While it is important that you harden your system configuration to improve system's security posture, many compliance programs require it as a mandatory control. 
The PCI DSS requirement 2.2.c states
> Examine policies and interview personnel to verify that system configuration standards are applied when new systems are configured and verified as being in place before a system is installed on the network.

CIS benchmarks are very specific configuration guidelines that can help you harden the system configuration to prevent and detect cyber attacks. 

### Getting started

* CIS provides a tool called CIS-CAT for scanning systems with benchmark files. There is a free version available but it's not scalable, also does not allow custom benchmark files. Nessus and Qualys also provide ways to run CIS benchmarks with similar customizable XML files.
* Benchmark files are XML files consumed by CIS-CAT to run checks specific to a technology (CentOS, Postgres, Tomcat..). The benchmarks are checks based on regular expressions used with `grep` to collect information from the system and configuration files.
* You can locate some very useful material from CIS website regarding each benchmark and it's rational. They've also listed exact commands that are run to check for a specific benchmarks which can be very useful while troubleshooting
* Running a simple CIS benchmark scan on one of your systems should give you long list of failures. Worth mentioning that there are two levels of CIS benchmarks for CentOS, Level 1 and Level 2. First level deals with changes which are easy to make and are very effective towards detection and prevention of an attack. Highly recommended that you work towards achieving at least Level 1.

### They're great but not easy to achieve

Your first scan (if worked correctly) should give you a long list of failures. It leaves us wondering, what the hell I am supposed to do with it? Applying these to any system or an array of systems calls for lot of resources and time, oh forget appying, analysing them is a pain. If you pass it on directly to your Infrastructure team, they would probably ignore it as a joke or best case- it will rust forever as a backlog item.

In the evolving tech industry, we're seeing more and more distributed team being formed for handling specific functions. System hardening naturally falls under the 'Security' umbrella. In large organizations, it would be quite daunting to justify need for making system configuration changes to thousands of servers because a list (like CIS benchmarks) told you so. 

### Prioritization is the key

The CIS benchmark list is long. Why would you overload the infrastructure teams with a long list of unjustified changes on top of their daily workload? We need a structured way to map CIS benchmarks with exploitation techniques in order to prioritize important benchmarks and avoid wasting time on unnecessary changes. CIS benchmarks are not to be followed exactly, you should pick the important ones that apply to security of your systems. The rest of the benchmarks can be either "accepted as risk" by mentioning a rational or  with some compensating controls.

What if we map the CIS controls with a security framework like [MITRE ATT@CK](https://attack.mitre.org/matrices/enterprise/linux/)? If we can map the entire framework to specific CIS benchmarks, we can use the framework to prioritize and justify implementation of CIS benchmarks critical for your security policy.


