import sys

if len(sys.argv) < 2:
    print("Usage: patch_module_h.py <path_to_include/linux/module.h>")
    sys.exit(1)

module_h = sys.argv[1]
with open(module_h, "r") as f:
    lines = f.readlines()

disabled_options = [
    "CONFIG_MODULES_TREE_LOOKUP",
    "CONFIG_STACKTRACE_BUILD_ID",
    "CONFIG_ARCH_USES_CFI_TRAPS",
    "CONFIG_MODULE_SIG",
    "CONFIG_TRACEPOINTS",
    "CONFIG_BPF_EVENTS",
    "CONFIG_DEBUG_INFO_BTF_MODULES",
    "CONFIG_TRACING",
    "CONFIG_EVENT_TRACING",
    "CONFIG_FTRACE_MCOUNT_RECORD",
    "CONFIG_KPROBES",
    "CONFIG_HAVE_STATIC_CALL_INLINE",
    "CONFIG_LIVEPATCH",
    "CONFIG_PRINTK_INDEX",
    "CONFIG_CONSTRUCTORS",
    "CONFIG_FUNCTION_ERROR_INJECTION",
    "CONFIG_DYNAMIC_DEBUG_CORE",
]

in_struct = False
new_lines = []

for line in lines:
    if "struct module_memory {" in line or "struct module {" in line:
        in_struct = True

    if in_struct:
        for opt in disabled_options:
            if line.strip() == f"#ifdef {opt}":
                line = f"#if 0 /* {opt} disabled for Cudy */\n"
                break
        if "IS_ENABLED(CONFIG_KUNIT)" in line:
            line = "#if 0 /* CONFIG_KUNIT disabled for Cudy */\n"

    if line.strip() == "#ifdef CONFIG_MODULES_TREE_LOOKUP":
        line = "#if 0 /* CONFIG_MODULES_TREE_LOOKUP disabled for Cudy */\n"

    if in_struct and line.startswith("} ____cacheline_aligned"):
        in_struct = False

    new_lines.append(line)

with open(module_h, "w") as f:
    f.writelines(new_lines)
print("Finished patching module.h for Cudy TR3000 struct module layout.")