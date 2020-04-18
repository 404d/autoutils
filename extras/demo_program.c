#include <stdio.h>
#include <stdbool.h>

bool is_initialized = false;

void log_msg(char* method, char* message) {
    printf("%s: %s\n", method, message);
}

void someObfuscatedNameACMVNSKECsadfasf() {
    log_msg("init", "Initializing");
    is_initialized = true;
    log_msg("init", "Up and running");
}

void someObfuscatedNameABKLNSKECsadfasf() {
    if (is_initialized)
        log_msg("status", "Ready");
    else
        log_msg("status", "Not ready");
}

void someObfuscatedNameACMVNaslkdfdfasf() {
    log_msg("teardown", "Taking things down");
    is_initialized = false;
    log_msg("teardown", "Done");
}

int main() {
    someObfuscatedNameABKLNSKECsadfasf();
    someObfuscatedNameACMVNSKECsadfasf();
    someObfuscatedNameABKLNSKECsadfasf();
    someObfuscatedNameACMVNaslkdfdfasf();
    someObfuscatedNameABKLNSKECsadfasf();
}
