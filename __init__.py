from binaryninja import log_info, log_debug, log_error, log_warn
from binaryninja.enums import MediumLevelILOperation
from binaryninja.plugin import PluginCommand


def discover_names(func, func_params):
    param = func_params[0]
    paramIndex = func.parameter_vars.vars.index(param)
    identified_functions = {}

    for caller in set(func.callers):
        logged_names = set()

        # Ensure that we only see one method used in this function
        for mlil_inst in caller.mlil.instructions:

            # Calls only
            if mlil_inst.operation != MediumLevelILOperation.MLIL_CALL:
                continue

            # Ensure that we're only acting on our calls
            # FIXME: There must be a better way to find the callee
            if not hasattr(mlil_inst.operands[1], 'constant'):
                continue

            called_func = func.view.get_function_at(mlil_inst.operands[1].constant)
            if called_func != func:
                continue

            call_site_param = caller.get_parameter_at(mlil_inst.address, func.function_type, paramIndex)
            # FIXME: There must be a better way again
            if str(call_site_param) == "<undetermined>":
                call_site_param = None
            logged_names.add(call_site_param)

        if len(logged_names) != 1 or None in logged_names:
            log_warn("Unable to determine method name for function %r: Identified method names: %r" % (caller, logged_names))
            continue

        logged_name_addr = list(logged_names)[0].value
        method_name = func.view.get_string_at(logged_name_addr).value

        if method_name not in identified_functions:
            identified_functions[method_name] = set()

        identified_functions[method_name].add(caller)

    # Eliminate names with multiple callers
    for name, callers in dict(identified_functions).items():
        if len(callers) != 1:
            log_debug("Eliminating name %r with callers %r" % (name, callers))
            del identified_functions[name]

        else:
            identified_functions[name] = list(callers)[0]

    return identified_functions



def do_discover_caller_names(bv, func):
    func_params = [param for param in current_function.parameter_vars if param.name == "method"]
    force = False

    if len(func_params) != 1:
        log_error("Unable to determine method name argument")
        return

    for name, func in check(func, func_params).items():
        # Skip if named correctly
        if func.symbol.name == name:
            continue

        # Skip if we're not forcing and the user has named this already
        if not func.symbol.auto and not force:
            log_debug("Skipped %r due to no auto symbol" % name)
            continue

        log_info("Renaming %r to %r" % (func, name))
        func.view.define_auto_symbol(Symbol(func.symbol.type, func.symbol.address, short_name=name))

PluginCommand.register(
    "Analysis\\Discover caller names by call parameters",
    "Renames all unique callers based on call parameters to the current function",
    do_discover_caller_names,
)
