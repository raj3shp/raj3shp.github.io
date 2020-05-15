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

Your first scan (if worked correctly) should give you a long list of failures. It leaves us wondering, what the hell I am supposed to do with it? Applying these to any server or a pool of servers will require lot of resources and time, oh forget appying, triaging them is a pain. If you pass it on directly to your Infrastructure team, they would probably ignore it as a joke or best case- it will rust forever as a backlog item.

In the evolving tech industry, we're seeing more and more distributed team being formed for handling specific functions. System hardening naturally falls under the 'Security' umbrella. In large organizations, it would be quite daunting to justify need for making system configuration changes to thousands of servers because a list (like CIS benchmarks) told you so.

### Prioritization is the key

For an organization running thousands of CentOS servers with different services and applications, it's almost impossible to come up with a single 'configuration template' that applies to all servers. You must prioritize and implement the changes in stages. Asset risk scoring can help in identifying which systems to harden first.

The CIS benchmark themself don't have any prioritization. We need a structured way to map CIS benchmarks with exploitation techniques in order to prioritize important benchmarks that achieve security now rather than wasting time in unnecessary checklists. CIS benchmarks are not to be followed exactly, you should pick the important ones that apply to security of your systems. The rest of the benchmarks can be either "accepted as risk" with a rational or with compensating controls.

Prioritization depends a lot on context and the security stratergy/policy for a given organization.



