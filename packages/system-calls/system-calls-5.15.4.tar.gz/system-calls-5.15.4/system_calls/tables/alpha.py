#!/usr/bin/python3

# Content autogenerated. Do not edit.

syscalls_alpha = {
    "_sysctl": 319,
    "accept": 99,
    "accept4": 502,
    "access": 33,
    "acct": 51,
    "add_key": 439,
    "adjtimex": 366,
    "bdflush": 300,
    "bind": 104,
    "bpf": 515,
    "brk": 17,
    "capget": 368,
    "capset": 369,
    "chdir": 12,
    "chmod": 15,
    "chown": 16,
    "chroot": 61,
    "clock_adjtime": 499,
    "clock_getres": 421,
    "clock_gettime": 420,
    "clock_nanosleep": 422,
    "clock_settime": 419,
    "clone": 312,
    "close": 6,
    "close_range": 546,
    "connect": 98,
    "copy_file_range": 519,
    "create_module": 306,
    "delete_module": 308,
    "dipc": 373,
    "dup": 41,
    "dup2": 90,
    "dup3": 487,
    "epoll_create": 407,
    "epoll_create1": 486,
    "epoll_ctl": 408,
    "epoll_pwait": 474,
    "epoll_pwait2": 551,
    "epoll_wait": 409,
    "eventfd": 478,
    "eventfd2": 485,
    "exec_with_loader": 25,
    "execve": 59,
    "execveat": 513,
    "exit": 1,
    "exit_group": 405,
    "faccessat": 462,
    "faccessat2": 549,
    "fadvise64": 413,
    "fallocate": 480,
    "fanotify_init": 494,
    "fanotify_mark": 495,
    "fchdir": 13,
    "fchmod": 124,
    "fchmodat": 461,
    "fchown": 123,
    "fchownat": 453,
    "fcntl": 92,
    "fdatasync": 447,
    "fgetxattr": 387,
    "finit_module": 507,
    "flistxattr": 390,
    "flock": 131,
    "fork": 2,
    "fremovexattr": 393,
    "fsconfig": 541,
    "fsetxattr": 384,
    "fsmount": 542,
    "fsopen": 540,
    "fspick": 543,
    "fstat": 91,
    "fstat64": 427,
    "fstatat64": 455,
    "fstatfs": 329,
    "fstatfs64": 529,
    "fsync": 95,
    "ftruncate": 130,
    "futex": 394,
    "futimesat": 454,
    "get_kernel_syms": 309,
    "get_mempolicy": 430,
    "get_robust_list": 467,
    "getcpu": 473,
    "getcwd": 367,
    "getdents": 305,
    "getdents64": 377,
    "getdtablesize": 89,
    "getegid": 530,
    "geteuid": 531,
    "getgid": 47,
    "getgroups": 79,
    "gethostname": 87,
    "getitimer": 361,
    "getpagesize": 64,
    "getpeername": 141,
    "getpgid": 233,
    "getpgrp": 63,
    "getpid": 20,
    "getppid": 532,
    "getpriority": 100,
    "getrandom": 511,
    "getresgid": 372,
    "getresuid": 344,
    "getrlimit": 144,
    "getrusage": 364,
    "getsid": 234,
    "getsockname": 150,
    "getsockopt": 118,
    "gettid": 378,
    "gettimeofday": 359,
    "getuid": 24,
    "getxattr": 385,
    "getxgid": 47,
    "getxpid": 20,
    "getxuid": 24,
    "init_module": 307,
    "inotify_add_watch": 445,
    "inotify_init": 444,
    "inotify_init1": 489,
    "inotify_rm_watch": 446,
    "io_cancel": 402,
    "io_destroy": 399,
    "io_getevents": 400,
    "io_pgetevents": 523,
    "io_setup": 398,
    "io_submit": 401,
    "io_uring_enter": 536,
    "io_uring_register": 537,
    "io_uring_setup": 535,
    "ioctl": 54,
    "ioprio_get": 443,
    "ioprio_set": 442,
    "kcmp": 506,
    "kexec_load": 448,
    "keyctl": 441,
    "kill": 37,
    "landlock_add_rule": 555,
    "landlock_create_ruleset": 554,
    "landlock_restrict_self": 556,
    "lchown": 208,
    "lgetxattr": 386,
    "link": 9,
    "linkat": 458,
    "listen": 106,
    "listxattr": 388,
    "llistxattr": 389,
    "lookup_dcookie": 406,
    "lremovexattr": 392,
    "lseek": 19,
    "lsetxattr": 383,
    "lstat": 68,
    "lstat64": 426,
    "madvise": 75,
    "mbind": 429,
    "membarrier": 517,
    "memfd_create": 512,
    "migrate_pages": 449,
    "mincore": 375,
    "mkdir": 136,
    "mkdirat": 451,
    "mknod": 14,
    "mknodat": 452,
    "mlock": 314,
    "mlock2": 518,
    "mlockall": 316,
    "mmap": 71,
    "mount": 302,
    "mount_setattr": 552,
    "move_mount": 539,
    "move_pages": 472,
    "mprotect": 74,
    "mq_getsetattr": 437,
    "mq_notify": 436,
    "mq_open": 432,
    "mq_timedreceive": 435,
    "mq_timedsend": 434,
    "mq_unlink": 433,
    "mremap": 341,
    "msgctl": 200,
    "msgget": 201,
    "msgrcv": 202,
    "msgsnd": 203,
    "msync": 217,
    "munlock": 315,
    "munlockall": 317,
    "munmap": 73,
    "name_to_handle_at": 497,
    "nanosleep": 340,
    "nfsservctl": 342,
    "old_adjtimex": 303,
    "oldumount": 321,
    "open": 45,
    "open_by_handle_at": 498,
    "open_tree": 538,
    "openat": 450,
    "openat2": 547,
    "osf_adjtime": 140,
    "osf_afs_syscall": 258,
    "osf_alt_plock": 181,
    "osf_alt_setsid": 188,
    "osf_alt_sigpending": 187,
    "osf_asynch_daemon": 163,
    "osf_audcntl": 252,
    "osf_audgen": 253,
    "osf_chflags": 34,
    "osf_execve": 11,
    "osf_exportfs": 169,
    "osf_fchflags": 35,
    "osf_fdatasync": 261,
    "osf_fpathconf": 248,
    "osf_fstat": 226,
    "osf_fstatfs": 161,
    "osf_fstatfs64": 228,
    "osf_fuser": 243,
    "osf_getaddressconf": 214,
    "osf_getdirentries": 159,
    "osf_getdomainname": 165,
    "osf_getfh": 164,
    "osf_getfsstat": 18,
    "osf_gethostid": 142,
    "osf_getitimer": 86,
    "osf_getlogin": 49,
    "osf_getmnt": 184,
    "osf_getrusage": 117,
    "osf_getsysinfo": 256,
    "osf_gettimeofday": 116,
    "osf_kloadcall": 223,
    "osf_kmodcall": 77,
    "osf_lstat": 225,
    "osf_memcntl": 260,
    "osf_mincore": 78,
    "osf_mount": 21,
    "osf_mremap": 65,
    "osf_msfs_syscall": 240,
    "osf_msleep": 215,
    "osf_mvalid": 213,
    "osf_mwakeup": 216,
    "osf_naccept": 30,
    "osf_nfssvc": 158,
    "osf_ngetpeername": 31,
    "osf_ngetsockname": 32,
    "osf_nrecvfrom": 29,
    "osf_nrecvmsg": 27,
    "osf_nsendmsg": 28,
    "osf_ntp_adjtime": 245,
    "osf_ntp_gettime": 246,
    "osf_old_creat": 8,
    "osf_old_fstat": 62,
    "osf_old_getpgrp": 81,
    "osf_old_killpg": 146,
    "osf_old_lstat": 40,
    "osf_old_open": 5,
    "osf_old_sigaction": 46,
    "osf_old_sigblock": 109,
    "osf_old_sigreturn": 139,
    "osf_old_sigsetmask": 110,
    "osf_old_sigvec": 108,
    "osf_old_stat": 38,
    "osf_old_vadvise": 72,
    "osf_old_vtrace": 115,
    "osf_old_wait": 84,
    "osf_oldquota": 149,
    "osf_pathconf": 247,
    "osf_pid_block": 153,
    "osf_pid_unblock": 154,
    "osf_plock": 107,
    "osf_priocntlset": 237,
    "osf_profil": 44,
    "osf_proplist_syscall": 244,
    "osf_reboot": 55,
    "osf_revoke": 56,
    "osf_sbrk": 69,
    "osf_security": 222,
    "osf_select": 93,
    "osf_set_program_attributes": 43,
    "osf_set_speculative": 239,
    "osf_sethostid": 143,
    "osf_setitimer": 83,
    "osf_setlogin": 50,
    "osf_setsysinfo": 257,
    "osf_settimeofday": 122,
    "osf_shmat": 209,
    "osf_signal": 218,
    "osf_sigprocmask": 48,
    "osf_sigsendset": 238,
    "osf_sigstack": 112,
    "osf_sigwaitprim": 157,
    "osf_sstk": 70,
    "osf_stat": 224,
    "osf_statfs": 160,
    "osf_statfs64": 227,
    "osf_subsys_info": 255,
    "osf_swapctl": 259,
    "osf_swapon": 199,
    "osf_syscall": 0,
    "osf_sysinfo": 241,
    "osf_table": 85,
    "osf_uadmin": 242,
    "osf_usleep_thread": 251,
    "osf_uswitch": 250,
    "osf_utc_adjtime": 220,
    "osf_utc_gettime": 219,
    "osf_utimes": 138,
    "osf_utsname": 207,
    "osf_wait4": 7,
    "osf_waitid": 236,
    "pciconfig_iobase": 376,
    "pciconfig_read": 345,
    "pciconfig_write": 346,
    "perf_event_open": 493,
    "personality": 324,
    "pidfd_getfd": 548,
    "pidfd_open": 544,
    "pidfd_send_signal": 534,
    "pipe": 42,
    "pipe2": 488,
    "pivot_root": 374,
    "pkey_alloc": 525,
    "pkey_free": 526,
    "pkey_mprotect": 524,
    "poll": 94,
    "ppoll": 464,
    "prctl": 348,
    "pread64": 349,
    "preadv": 490,
    "preadv2": 520,
    "prlimit64": 496,
    "process_madvise": 550,
    "process_mrelease": 558,
    "process_vm_readv": 504,
    "process_vm_writev": 505,
    "pselect6": 463,
    "ptrace": 26,
    "pwrite64": 350,
    "pwritev": 491,
    "pwritev2": 521,
    "query_module": 347,
    "quotactl": 148,
    "quotactl_fd": 553,
    "read": 3,
    "readahead": 379,
    "readlink": 58,
    "readlinkat": 460,
    "readv": 120,
    "reboot": 311,
    "recv": 102,
    "recvfrom": 125,
    "recvmmsg": 479,
    "recvmsg": 113,
    "remap_file_pages": 410,
    "removexattr": 391,
    "rename": 128,
    "renameat": 457,
    "renameat2": 510,
    "request_key": 440,
    "restart_syscall": 412,
    "rmdir": 137,
    "rseq": 527,
    "rt_sigaction": 352,
    "rt_sigpending": 354,
    "rt_sigprocmask": 353,
    "rt_sigqueueinfo": 356,
    "rt_sigreturn": 351,
    "rt_sigsuspend": 357,
    "rt_sigtimedwait": 355,
    "rt_tgsigqueueinfo": 492,
    "sched_get_priority_max": 335,
    "sched_get_priority_min": 336,
    "sched_getaffinity": 396,
    "sched_getattr": 509,
    "sched_getparam": 331,
    "sched_getscheduler": 333,
    "sched_rr_get_interval": 337,
    "sched_setaffinity": 395,
    "sched_setattr": 508,
    "sched_setparam": 330,
    "sched_setscheduler": 332,
    "sched_yield": 334,
    "seccomp": 514,
    "select": 358,
    "semctl": 204,
    "semget": 205,
    "semop": 206,
    "semtimedop": 423,
    "send": 101,
    "sendfile": 370,
    "sendmmsg": 503,
    "sendmsg": 114,
    "sendto": 133,
    "set_mempolicy": 431,
    "set_robust_list": 466,
    "set_tid_address": 411,
    "setdomainname": 166,
    "setfsgid": 326,
    "setfsuid": 325,
    "setgid": 132,
    "setgroups": 80,
    "sethae": 301,
    "sethostname": 88,
    "setitimer": 362,
    "setns": 501,
    "setpgid": 39,
    "setpgrp": 82,
    "setpriority": 96,
    "setregid": 127,
    "setresgid": 371,
    "setresuid": 343,
    "setreuid": 126,
    "setrlimit": 145,
    "setsid": 147,
    "setsockopt": 105,
    "settimeofday": 360,
    "setuid": 23,
    "setxattr": 382,
    "shmat": 209,
    "shmctl": 210,
    "shmdt": 211,
    "shmget": 212,
    "shutdown": 134,
    "sigaction": 156,
    "sigaltstack": 235,
    "signalfd": 476,
    "signalfd4": 484,
    "sigpending": 52,
    "sigreturn": 103,
    "sigsuspend": 111,
    "socket": 97,
    "socketpair": 135,
    "splice": 468,
    "stat": 67,
    "stat64": 425,
    "statfs": 328,
    "statfs64": 528,
    "statx": 522,
    "swapoff": 304,
    "swapon": 322,
    "symlink": 57,
    "symlinkat": 459,
    "sync": 36,
    "sync_file_range": 469,
    "syncfs": 500,
    "sysfs": 254,
    "sysinfo": 318,
    "syslog": 310,
    "tee": 470,
    "tgkill": 424,
    "timer_create": 414,
    "timer_delete": 418,
    "timer_getoverrun": 417,
    "timer_gettime": 416,
    "timer_settime": 415,
    "timerfd": 477,
    "timerfd_create": 481,
    "timerfd_gettime": 483,
    "timerfd_settime": 482,
    "times": 323,
    "tkill": 381,
    "truncate": 129,
    "umask": 60,
    "umount": 22,
    "umount2": 22,
    "uname": 339,
    "unlink": 10,
    "unlinkat": 456,
    "unshare": 465,
    "uselib": 313,
    "userfaultfd": 516,
    "ustat": 327,
    "utimensat": 475,
    "utimes": 363,
    "vfork": 66,
    "vhangup": 76,
    "vmsplice": 471,
    "wait4": 365,
    "waitid": 438,
    "write": 4,
    "writev": 121,
}
