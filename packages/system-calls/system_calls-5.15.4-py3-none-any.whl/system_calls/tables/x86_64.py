#!/usr/bin/python3

# Content autogenerated. Do not edit.

syscalls_x86_64 = {
    "_sysctl": 156,
    "accept": 43,
    "accept4": 288,
    "access": 21,
    "acct": 163,
    "add_key": 248,
    "adjtimex": 159,
    "alarm": 37,
    "arch_prctl": 158,
    "bind": 49,
    "bpf": 321,
    "brk": 12,
    "capget": 125,
    "capset": 126,
    "chdir": 80,
    "chmod": 90,
    "chown": 92,
    "chroot": 161,
    "clock_adjtime": 305,
    "clock_getres": 229,
    "clock_gettime": 228,
    "clock_nanosleep": 230,
    "clock_settime": 227,
    "clone": 56,
    "clone3": 435,
    "close": 3,
    "close_range": 436,
    "connect": 42,
    "copy_file_range": 326,
    "creat": 85,
    "create_module": 174,
    "delete_module": 176,
    "dup": 32,
    "dup2": 33,
    "dup3": 292,
    "epoll_create": 213,
    "epoll_create1": 291,
    "epoll_ctl": 233,
    "epoll_ctl_old": 214,
    "epoll_pwait": 281,
    "epoll_pwait2": 441,
    "epoll_wait": 232,
    "epoll_wait_old": 215,
    "eventfd": 284,
    "eventfd2": 290,
    "execve": 59,
    "execveat": 322,
    "exit": 60,
    "exit_group": 231,
    "faccessat": 269,
    "faccessat2": 439,
    "fadvise64": 221,
    "fallocate": 285,
    "fanotify_init": 300,
    "fanotify_mark": 301,
    "fchdir": 81,
    "fchmod": 91,
    "fchmodat": 268,
    "fchown": 93,
    "fchownat": 260,
    "fcntl": 72,
    "fdatasync": 75,
    "fgetxattr": 193,
    "finit_module": 313,
    "flistxattr": 196,
    "flock": 73,
    "fork": 57,
    "fremovexattr": 199,
    "fsconfig": 431,
    "fsetxattr": 190,
    "fsmount": 432,
    "fsopen": 430,
    "fspick": 433,
    "fstat": 5,
    "fstatfs": 138,
    "fsync": 74,
    "ftruncate": 77,
    "futex": 202,
    "futimesat": 261,
    "get_kernel_syms": 177,
    "get_mempolicy": 239,
    "get_robust_list": 274,
    "get_thread_area": 211,
    "getcpu": 309,
    "getcwd": 79,
    "getdents": 78,
    "getdents64": 217,
    "getegid": 108,
    "geteuid": 107,
    "getgid": 104,
    "getgroups": 115,
    "getitimer": 36,
    "getpeername": 52,
    "getpgid": 121,
    "getpgrp": 111,
    "getpid": 39,
    "getpmsg": 181,
    "getppid": 110,
    "getpriority": 140,
    "getrandom": 318,
    "getresgid": 120,
    "getresuid": 118,
    "getrlimit": 97,
    "getrusage": 98,
    "getsid": 124,
    "getsockname": 51,
    "getsockopt": 55,
    "gettid": 186,
    "gettimeofday": 96,
    "getuid": 102,
    "getxattr": 191,
    "init_module": 175,
    "inotify_add_watch": 254,
    "inotify_init": 253,
    "inotify_init1": 294,
    "inotify_rm_watch": 255,
    "io_cancel": 210,
    "io_destroy": 207,
    "io_getevents": 208,
    "io_pgetevents": 333,
    "io_setup": 206,
    "io_submit": 209,
    "io_uring_enter": 426,
    "io_uring_register": 427,
    "io_uring_setup": 425,
    "ioctl": 16,
    "ioperm": 173,
    "iopl": 172,
    "ioprio_get": 252,
    "ioprio_set": 251,
    "kcmp": 312,
    "kexec_file_load": 320,
    "kexec_load": 246,
    "keyctl": 250,
    "kill": 62,
    "landlock_add_rule": 445,
    "landlock_create_ruleset": 444,
    "landlock_restrict_self": 446,
    "lchown": 94,
    "lgetxattr": 192,
    "link": 86,
    "linkat": 265,
    "listen": 50,
    "listxattr": 194,
    "llistxattr": 195,
    "lookup_dcookie": 212,
    "lremovexattr": 198,
    "lseek": 8,
    "lsetxattr": 189,
    "lstat": 6,
    "madvise": 28,
    "mbind": 237,
    "membarrier": 324,
    "memfd_create": 319,
    "memfd_secret": 447,
    "migrate_pages": 256,
    "mincore": 27,
    "mkdir": 83,
    "mkdirat": 258,
    "mknod": 133,
    "mknodat": 259,
    "mlock": 149,
    "mlock2": 325,
    "mlockall": 151,
    "mmap": 9,
    "modify_ldt": 154,
    "mount": 165,
    "mount_setattr": 442,
    "move_mount": 429,
    "move_pages": 279,
    "mprotect": 10,
    "mq_getsetattr": 245,
    "mq_notify": 244,
    "mq_open": 240,
    "mq_timedreceive": 243,
    "mq_timedsend": 242,
    "mq_unlink": 241,
    "mremap": 25,
    "msgctl": 71,
    "msgget": 68,
    "msgrcv": 70,
    "msgsnd": 69,
    "msync": 26,
    "munlock": 150,
    "munlockall": 152,
    "munmap": 11,
    "name_to_handle_at": 303,
    "nanosleep": 35,
    "newfstatat": 262,
    "nfsservctl": 180,
    "open": 2,
    "open_by_handle_at": 304,
    "open_tree": 428,
    "openat": 257,
    "openat2": 437,
    "pause": 34,
    "perf_event_open": 298,
    "personality": 135,
    "pidfd_getfd": 438,
    "pidfd_open": 434,
    "pidfd_send_signal": 424,
    "pipe": 22,
    "pipe2": 293,
    "pivot_root": 155,
    "pkey_alloc": 330,
    "pkey_free": 331,
    "pkey_mprotect": 329,
    "poll": 7,
    "ppoll": 271,
    "prctl": 157,
    "pread64": 17,
    "preadv": 295,
    "preadv2": 327,
    "prlimit64": 302,
    "process_madvise": 440,
    "process_mrelease": 448,
    "process_vm_readv": 310,
    "process_vm_writev": 311,
    "pselect6": 270,
    "ptrace": 101,
    "pwrite64": 18,
    "pwritev": 296,
    "pwritev2": 328,
    "query_module": 178,
    "quotactl": 179,
    "quotactl_fd": 443,
    "read": 0,
    "readahead": 187,
    "readlink": 89,
    "readlinkat": 267,
    "readv": 19,
    "reboot": 169,
    "recvfrom": 45,
    "recvmmsg": 299,
    "recvmsg": 47,
    "remap_file_pages": 216,
    "removexattr": 197,
    "rename": 82,
    "renameat": 264,
    "renameat2": 316,
    "request_key": 249,
    "restart_syscall": 219,
    "rmdir": 84,
    "rseq": 334,
    "rt_sigaction": 13,
    "rt_sigpending": 127,
    "rt_sigprocmask": 14,
    "rt_sigqueueinfo": 129,
    "rt_sigreturn": 15,
    "rt_sigsuspend": 130,
    "rt_sigtimedwait": 128,
    "rt_tgsigqueueinfo": 297,
    "sched_get_priority_max": 146,
    "sched_get_priority_min": 147,
    "sched_getaffinity": 204,
    "sched_getattr": 315,
    "sched_getparam": 143,
    "sched_getscheduler": 145,
    "sched_rr_get_interval": 148,
    "sched_setaffinity": 203,
    "sched_setattr": 314,
    "sched_setparam": 142,
    "sched_setscheduler": 144,
    "sched_yield": 24,
    "seccomp": 317,
    "select": 23,
    "semctl": 66,
    "semget": 64,
    "semop": 65,
    "semtimedop": 220,
    "sendfile": 40,
    "sendmmsg": 307,
    "sendmsg": 46,
    "sendto": 44,
    "set_mempolicy": 238,
    "set_robust_list": 273,
    "set_thread_area": 205,
    "set_tid_address": 218,
    "setdomainname": 171,
    "setfsgid": 123,
    "setfsuid": 122,
    "setgid": 106,
    "setgroups": 116,
    "sethostname": 170,
    "setitimer": 38,
    "setns": 308,
    "setpgid": 109,
    "setpriority": 141,
    "setregid": 114,
    "setresgid": 119,
    "setresuid": 117,
    "setreuid": 113,
    "setrlimit": 160,
    "setsid": 112,
    "setsockopt": 54,
    "settimeofday": 164,
    "setuid": 105,
    "setxattr": 188,
    "shmat": 30,
    "shmctl": 31,
    "shmdt": 67,
    "shmget": 29,
    "shutdown": 48,
    "sigaltstack": 131,
    "signalfd": 282,
    "signalfd4": 289,
    "socket": 41,
    "socketpair": 53,
    "splice": 275,
    "stat": 4,
    "statfs": 137,
    "statx": 332,
    "swapoff": 168,
    "swapon": 167,
    "symlink": 88,
    "symlinkat": 266,
    "sync": 162,
    "sync_file_range": 277,
    "syncfs": 306,
    "sysfs": 139,
    "sysinfo": 99,
    "syslog": 103,
    "tee": 276,
    "tgkill": 234,
    "time": 201,
    "timer_create": 222,
    "timer_delete": 226,
    "timer_getoverrun": 225,
    "timer_gettime": 224,
    "timer_settime": 223,
    "timerfd_create": 283,
    "timerfd_gettime": 287,
    "timerfd_settime": 286,
    "times": 100,
    "tkill": 200,
    "truncate": 76,
    "umask": 95,
    "umount2": 166,
    "uname": 63,
    "unlink": 87,
    "unlinkat": 263,
    "unshare": 272,
    "uselib": 134,
    "userfaultfd": 323,
    "ustat": 136,
    "utime": 132,
    "utimensat": 280,
    "utimes": 235,
    "vfork": 58,
    "vhangup": 153,
    "vmsplice": 278,
    "wait4": 61,
    "waitid": 247,
    "write": 1,
    "writev": 20,
}
