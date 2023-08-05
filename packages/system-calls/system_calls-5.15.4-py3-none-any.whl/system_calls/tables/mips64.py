#!/usr/bin/python3

# Content autogenerated. Do not edit.

syscalls_mips64 = {
    "_newselect": 5022,
    "_sysctl": 5152,
    "accept": 5042,
    "accept4": 5293,
    "access": 5020,
    "acct": 5158,
    "add_key": 5239,
    "adjtimex": 5154,
    "alarm": 5037,
    "bind": 5048,
    "bpf": 5315,
    "brk": 5012,
    "cachectl": 5198,
    "cacheflush": 5197,
    "capget": 5123,
    "capset": 5124,
    "chdir": 5078,
    "chmod": 5088,
    "chown": 5090,
    "chroot": 5156,
    "clock_adjtime": 5300,
    "clock_getres": 5223,
    "clock_gettime": 5222,
    "clock_nanosleep": 5224,
    "clock_settime": 5221,
    "clone": 5055,
    "clone3": 5435,
    "close": 5003,
    "close_range": 5436,
    "connect": 5041,
    "copy_file_range": 5320,
    "creat": 5083,
    "create_module": 5167,
    "delete_module": 5169,
    "dup": 5031,
    "dup2": 5032,
    "dup3": 5286,
    "epoll_create": 5207,
    "epoll_create1": 5285,
    "epoll_ctl": 5208,
    "epoll_pwait": 5272,
    "epoll_pwait2": 5441,
    "epoll_wait": 5209,
    "eventfd": 5278,
    "eventfd2": 5284,
    "execve": 5057,
    "execveat": 5316,
    "exit": 5058,
    "exit_group": 5205,
    "faccessat": 5259,
    "faccessat2": 5439,
    "fadvise64": 5215,
    "fallocate": 5279,
    "fanotify_init": 5295,
    "fanotify_mark": 5296,
    "fchdir": 5079,
    "fchmod": 5089,
    "fchmodat": 5258,
    "fchown": 5091,
    "fchownat": 5250,
    "fcntl": 5070,
    "fdatasync": 5073,
    "fgetxattr": 5185,
    "finit_module": 5307,
    "flistxattr": 5188,
    "flock": 5071,
    "fork": 5056,
    "fremovexattr": 5191,
    "fsconfig": 5431,
    "fsetxattr": 5182,
    "fsmount": 5432,
    "fsopen": 5430,
    "fspick": 5433,
    "fstat": 5005,
    "fstatfs": 5135,
    "fsync": 5072,
    "ftruncate": 5075,
    "futex": 5194,
    "futimesat": 5251,
    "get_kernel_syms": 5170,
    "get_mempolicy": 5228,
    "get_robust_list": 5269,
    "getcpu": 5271,
    "getcwd": 5077,
    "getdents": 5076,
    "getdents64": 5308,
    "getegid": 5106,
    "geteuid": 5105,
    "getgid": 5102,
    "getgroups": 5113,
    "getitimer": 5035,
    "getpeername": 5051,
    "getpgid": 5119,
    "getpgrp": 5109,
    "getpid": 5038,
    "getpmsg": 5174,
    "getppid": 5108,
    "getpriority": 5137,
    "getrandom": 5313,
    "getresgid": 5118,
    "getresuid": 5116,
    "getrlimit": 5095,
    "getrusage": 5096,
    "getsid": 5122,
    "getsockname": 5050,
    "getsockopt": 5054,
    "gettid": 5178,
    "gettimeofday": 5094,
    "getuid": 5100,
    "getxattr": 5183,
    "init_module": 5168,
    "inotify_add_watch": 5244,
    "inotify_init": 5243,
    "inotify_init1": 5288,
    "inotify_rm_watch": 5245,
    "io_cancel": 5204,
    "io_destroy": 5201,
    "io_getevents": 5202,
    "io_pgetevents": 5328,
    "io_setup": 5200,
    "io_submit": 5203,
    "io_uring_enter": 5426,
    "io_uring_register": 5427,
    "io_uring_setup": 5425,
    "ioctl": 5015,
    "ioprio_get": 5274,
    "ioprio_set": 5273,
    "kcmp": 5306,
    "kexec_load": 5270,
    "keyctl": 5241,
    "kill": 5060,
    "landlock_add_rule": 5445,
    "landlock_create_ruleset": 5444,
    "landlock_restrict_self": 5446,
    "lchown": 5092,
    "lgetxattr": 5184,
    "link": 5084,
    "linkat": 5255,
    "listen": 5049,
    "listxattr": 5186,
    "llistxattr": 5187,
    "lookup_dcookie": 5206,
    "lremovexattr": 5190,
    "lseek": 5008,
    "lsetxattr": 5181,
    "lstat": 5006,
    "madvise": 5027,
    "mbind": 5227,
    "membarrier": 5318,
    "memfd_create": 5314,
    "migrate_pages": 5246,
    "mincore": 5026,
    "mkdir": 5081,
    "mkdirat": 5248,
    "mknod": 5131,
    "mknodat": 5249,
    "mlock": 5146,
    "mlock2": 5319,
    "mlockall": 5148,
    "mmap": 5009,
    "mount": 5160,
    "mount_setattr": 5442,
    "move_mount": 5429,
    "move_pages": 5267,
    "mprotect": 5010,
    "mq_getsetattr": 5235,
    "mq_notify": 5234,
    "mq_open": 5230,
    "mq_timedreceive": 5233,
    "mq_timedsend": 5232,
    "mq_unlink": 5231,
    "mremap": 5024,
    "msgctl": 5069,
    "msgget": 5066,
    "msgrcv": 5068,
    "msgsnd": 5067,
    "msync": 5025,
    "munlock": 5147,
    "munlockall": 5149,
    "munmap": 5011,
    "name_to_handle_at": 5298,
    "nanosleep": 5034,
    "newfstatat": 5252,
    "nfsservctl": 5173,
    "open": 5002,
    "open_by_handle_at": 5299,
    "open_tree": 5428,
    "openat": 5247,
    "openat2": 5437,
    "pause": 5033,
    "perf_event_open": 5292,
    "personality": 5132,
    "pidfd_getfd": 5438,
    "pidfd_open": 5434,
    "pidfd_send_signal": 5424,
    "pipe": 5021,
    "pipe2": 5287,
    "pivot_root": 5151,
    "pkey_alloc": 5324,
    "pkey_free": 5325,
    "pkey_mprotect": 5323,
    "poll": 5007,
    "ppoll": 5261,
    "prctl": 5153,
    "pread64": 5016,
    "preadv": 5289,
    "preadv2": 5321,
    "prlimit64": 5297,
    "process_madvise": 5440,
    "process_mrelease": 5448,
    "process_vm_readv": 5304,
    "process_vm_writev": 5305,
    "pselect6": 5260,
    "ptrace": 5099,
    "pwrite64": 5017,
    "pwritev": 5290,
    "pwritev2": 5322,
    "query_module": 5171,
    "quotactl": 5172,
    "quotactl_fd": 5443,
    "read": 5000,
    "readahead": 5179,
    "readlink": 5087,
    "readlinkat": 5257,
    "readv": 5018,
    "reboot": 5164,
    "recvfrom": 5044,
    "recvmmsg": 5294,
    "recvmsg": 5046,
    "remap_file_pages": 5210,
    "removexattr": 5189,
    "rename": 5080,
    "renameat": 5254,
    "renameat2": 5311,
    "request_key": 5240,
    "restart_syscall": 5213,
    "rmdir": 5082,
    "rseq": 5327,
    "rt_sigaction": 5013,
    "rt_sigpending": 5125,
    "rt_sigprocmask": 5014,
    "rt_sigqueueinfo": 5127,
    "rt_sigreturn": 5211,
    "rt_sigsuspend": 5128,
    "rt_sigtimedwait": 5126,
    "rt_tgsigqueueinfo": 5291,
    "sched_get_priority_max": 5143,
    "sched_get_priority_min": 5144,
    "sched_getaffinity": 5196,
    "sched_getattr": 5310,
    "sched_getparam": 5140,
    "sched_getscheduler": 5142,
    "sched_rr_get_interval": 5145,
    "sched_setaffinity": 5195,
    "sched_setattr": 5309,
    "sched_setparam": 5139,
    "sched_setscheduler": 5141,
    "sched_yield": 5023,
    "seccomp": 5312,
    "semctl": 5064,
    "semget": 5062,
    "semop": 5063,
    "semtimedop": 5214,
    "sendfile": 5039,
    "sendmmsg": 5302,
    "sendmsg": 5045,
    "sendto": 5043,
    "set_mempolicy": 5229,
    "set_robust_list": 5268,
    "set_thread_area": 5242,
    "set_tid_address": 5212,
    "setdomainname": 5166,
    "setfsgid": 5121,
    "setfsuid": 5120,
    "setgid": 5104,
    "setgroups": 5114,
    "sethostname": 5165,
    "setitimer": 5036,
    "setns": 5303,
    "setpgid": 5107,
    "setpriority": 5138,
    "setregid": 5112,
    "setresgid": 5117,
    "setresuid": 5115,
    "setreuid": 5111,
    "setrlimit": 5155,
    "setsid": 5110,
    "setsockopt": 5053,
    "settimeofday": 5159,
    "setuid": 5103,
    "setxattr": 5180,
    "shmat": 5029,
    "shmctl": 5030,
    "shmdt": 5065,
    "shmget": 5028,
    "shutdown": 5047,
    "sigaltstack": 5129,
    "signalfd": 5276,
    "signalfd4": 5283,
    "socket": 5040,
    "socketpair": 5052,
    "splice": 5263,
    "stat": 5004,
    "statfs": 5134,
    "statx": 5326,
    "swapoff": 5163,
    "swapon": 5162,
    "symlink": 5086,
    "symlinkat": 5256,
    "sync": 5157,
    "sync_file_range": 5264,
    "syncfs": 5301,
    "sysfs": 5136,
    "sysinfo": 5097,
    "syslog": 5101,
    "sysmips": 5199,
    "tee": 5265,
    "tgkill": 5225,
    "timer_create": 5216,
    "timer_delete": 5220,
    "timer_getoverrun": 5219,
    "timer_gettime": 5218,
    "timer_settime": 5217,
    "timerfd": 5277,
    "timerfd_create": 5280,
    "timerfd_gettime": 5281,
    "timerfd_settime": 5282,
    "times": 5098,
    "tkill": 5192,
    "truncate": 5074,
    "umask": 5093,
    "umount2": 5161,
    "uname": 5061,
    "unlink": 5085,
    "unlinkat": 5253,
    "unshare": 5262,
    "userfaultfd": 5317,
    "ustat": 5133,
    "utime": 5130,
    "utimensat": 5275,
    "utimes": 5226,
    "vhangup": 5150,
    "vmsplice": 5266,
    "wait4": 5059,
    "waitid": 5237,
    "write": 5001,
    "writev": 5019,
}
