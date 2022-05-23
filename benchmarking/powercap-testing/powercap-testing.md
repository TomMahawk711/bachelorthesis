## My story of testing powercap-set

### Prerequisites

This source [[1]](https://github.com/powercap/powercap#prerequisites) states that CONFIG_POWERCAP and CONFIG_INTEL_RAPL should be enabled and the following command as to be entered, to get powercap working:

```shell
modprobe intel_rapl
```

In my understanding modprobe adds or loads modules to the Linux Kernel?
I am not certain that CONFIG_POWERCAP and CONFIG_INTEL_RAPL are enabled, but if they would not be, I could not see the intel-rapl folders (one for each zone and package) in following directory [[4]](https://askubuntu.com/questions/1148528/how-to-enable-kernel-configs-config-powercap-and-config-intel-rapl-in-ubuntu):

```
/sys/class/powercap
```

I can see these folders, so I would assume CONFIG_POWERCAP and CONFIG_INTEL_RAPL are enabled.



### Trying to powercap with powercap-set

trying to powercap with a tool named powercap-set [[2](https://manpages.ubuntu.com/manpages/focal/man1/powercap-set.1.html), [3](https://www.kernel.org/doc/html/latest/power/powercap/powercap.html)], using it like this:

```shell
sudo powercap-set -p intel-rapl -z 0 -e 1
sudo powercap-set -p intel-rapl -z 0:0 -e 1
sudo powercap-set -p intel-rapl -z 0 -c 0 -l 24000000
sudo powercap-set -p intel-rapl -z 0 -c 1 -l 24000000
sudo powercap-set -p intel-rapl -z 0:0 -c 0 -l 24000000
```

The first two commands enable control at zone level (`-z 0` -> package0; `-z 0:0` -> package0:zone0 (core)).
The next three commands set the power_limit for different constraints and zones. -l defines the power limit in uW.
I set it for every relevant package/zone and constraint, just to be sure.

Using ```powercap-info -p intel-rapl``` and reading out the limits before and after these commands, confirms the new values are set to my specified value (looking at power_limit_uw), 
but my CPU is ignoring them and is using the same amount of power as before when running a benchmark. :/
I tried this with setting just one of the constraint of a zone/package as well, but without success.
I used a Monte-Carlo-Pi-Approximation as a benchmark.



### Verifying with energy measurements

measured power with perf:

```shell
sudo perf stat -e power/energy-cores/
```

A process gets started which measures the consumed energy until the process is terminated, 
afterwards it shows the consumed energy in Joules or Ws respectively and the time passed in seconds.

Measuring with perf the energy consumption does not change at all after setting new limits with powercap-set as mentioned before. :(
The energy consumption DOES change when limiting the CPUs frequency with cpufreq-set. [[5]](https://linux.die.net/man/1/cpufreq-set) :)
So perf does not measure just a whole lot of bullsh*t.



## Sources

[1] - https://github.com/powercap/powercap#prerequisites
[2] - https://manpages.ubuntu.com/manpages/focal/man1/powercap-set.1.html
[3] - https://www.kernel.org/doc/html/latest/power/powercap/powercap.html
[4] - (sketchy source) https://askubuntu.com/questions/1148528/how-to-enable-kernel-configs-config-powercap-and-config-intel-rapl-in-ubuntu
[5] - https://linux.die.net/man/1/cpufreq-set



## Appendix

To summarize my pain:

I ran the benchmark and measured the consumed energy in a separate terminal with:

```shell
sudo perf stat -e power/energy-cores/
```

waited 5 seconds...

did `ctrl + c`

measured about 280 Joules -> approximately 56 watts of power consumption

checked the current limits with:

```shell
powercap-info -p intel-rapl
```

entered the following commands:

```shell
modprobe intel_rapl
sudo powercap-set -p intel-rapl -z 0 -e 1
sudo powercap-set -p intel-rapl -z 0:0 -e 1
sudo powercap-set -p intel-rapl -z 0 -c 0 -l 24000000
sudo powercap-set -p intel-rapl -z 0 -c 1 -l 24000000
sudo powercap-set -p intel-rapl -z 0:0 -c 0 -l 24000000
```

verified new set values with output from:

```shell
powercap-info -p intel-rapl
```

I ran the benchmark and measured the consumed energy in a separate terminal:

```shell
sudo perf stat -e power/energy-cores/
```

waited 5 seconds...

did `ctrl + c`

measured about 280 Joules again -> expected less than half of that (resulting in 24 watts of power consumption)

restarting computer to reset these values

doing a sanity check for measurement with perf by limiting the CPUs frequency (expecting lower energy consumption)

perf measured a lower energy consumption `¯\_(ツ)_/¯`

