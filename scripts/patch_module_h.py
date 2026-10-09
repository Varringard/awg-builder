import sys

if len(sys.argv) < 2:
    print("Usage: patch_module_h.py <path_to_include/linux/module.h>")
    sys.exit(1)

module_h = sys.argv[1]
with open(module_h, "r") as f:
    content = f.read()

undefs = """
/* Begin Cudy TR3000 struct module alignment */
#undef CONFIG_MODULES_TREE_LOOKUP
#undef CONFIG_STACKTRACE_BUILD_ID
#undef CONFIG_ARCH_USES_CFI_TRAPS
#undef CONFIG_MODULE_SIG
#undef CONFIG_TRACEPOINTS
#undef CONFIG_BPF_EVENTS
#undef CONFIG_DEBUG_INFO_BTF_MODULES
#undef CONFIG_TRACING
#undef CONFIG_EVENT_TRACING
#undef CONFIG_FTRACE_MCOUNT_RECORD
#undef CONFIG_KPROBES
#undef CONFIG_HAVE_STATIC_CALL_INLINE
#undef CONFIG_KUNIT
#undef CONFIG_LIVEPATCH
#undef CONFIG_PRINTK_INDEX
#undef CONFIG_CONSTRUCTORS
#undef CONFIG_FUNCTION_ERROR_INJECTION
#undef CONFIG_DYNAMIC_DEBUG_CORE
/* End Cudy TR3000 struct module alignment */
"""

target = "struct module_memory {"
if target in content:
    content = content.replace(target, undefs + "\n" + target, 1)
    print("Inserted undefs before struct module_memory in " + module_h)
else:
    print("ERROR: struct module_memory not found in " + module_h)
    sys.exit(1)

content = content.replace("#if IS_ENABLED(CONFIG_KUNIT)", "#if 0 /* IS_ENABLED(CONFIG_KUNIT) */")

with open(module_h, "w") as f:
    f.write(content)
print("module.h patched successfully.")