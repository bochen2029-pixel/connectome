// cx doctor - the environment probe.  M0 deliverable (spec section 13).
//
// A session that starts on a cold box needs one command that says what is present
// and what is missing, before it builds anything.  Every check here is a fact about
// this machine, never a guess: a device query, a TCP connect, or a file test.

#include "cx/scan.h"

#include <cstdio>
#include <filesystem>
#include <string>
#include <vector>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#endif

namespace cx {
namespace {

struct Check {
    std::string group;
    std::string name;
    bool        ok = false;
    bool        required = false;
    std::string detail;
};

bool port_open(const char* host, int port, int timeout_ms) {
#ifdef _WIN32
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) return false;

    bool ok = false;
    SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (s != INVALID_SOCKET) {
        u_long nonblocking = 1;
        ioctlsocket(s, FIONBIO, &nonblocking);

        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_port   = htons(static_cast<u_short>(port));
        inet_pton(AF_INET, host, &addr.sin_addr);

        connect(s, reinterpret_cast<sockaddr*>(&addr), sizeof(addr));

        fd_set write_set;
        FD_ZERO(&write_set);
        FD_SET(s, &write_set);
        timeval tv{};
        tv.tv_sec  = timeout_ms / 1000;
        tv.tv_usec = (timeout_ms % 1000) * 1000;

        if (select(0, nullptr, &write_set, nullptr, &tv) > 0) {
            int err = 0;
            int len = sizeof(err);
            if (getsockopt(s, SOL_SOCKET, SO_ERROR, reinterpret_cast<char*>(&err), &len) == 0) {
                ok = (err == 0);
            }
        }
        closesocket(s);
    }
    WSACleanup();
    return ok;
#else
    (void)host; (void)port; (void)timeout_ms;
    return false;   // Windows-first; the POSIX probe lands with the Linux port.
#endif
}

std::string human_bytes(std::size_t b) {
    char buf[64];
    const double gib = static_cast<double>(b) / (1024.0 * 1024.0 * 1024.0);
    std::snprintf(buf, sizeof(buf), "%.2f GiB", gib);
    return buf;
}

void add_path_check(std::vector<Check>& out, const char* group, const char* name,
                    const char* path, bool required) {
    const bool present = std::filesystem::exists(path);
    out.push_back(Check{group, name, present, required, present ? path : std::string("missing: ") + path});
}

} // namespace

int doctor(bool json) {
    std::vector<Check> checks;

    // ---- compute ---------------------------------------------------------
    const DeviceInfo dev = cuda_device_info();
    checks.push_back(Check{"compute", "cuda device", dev.present, false,
                           dev.present ? dev.name + "  sm_" + std::to_string(dev.cc_major) +
                                             std::to_string(dev.cc_minor) + "  " +
                                             human_bytes(dev.mem_free) + " free of " +
                                             human_bytes(dev.mem_total)
                                       : dev.name});
    if (dev.present) {
        checks.push_back(Check{"compute", "cuda runtime", dev.runtime > 0, false,
                               "driver " + std::to_string(dev.driver) + ", runtime " +
                                   std::to_string(dev.runtime)});
    }

    // ---- gear one: the local model servers (spec section 3) --------------
    struct PortSpec { const char* name; int port; bool required; };
    const PortSpec ports[] = {
        {"embedding server (llama.cpp)", 8092, true},
        {"vision / OCR server",          8091, false},
        {"cortexd",                      8094, false},
    };
    for (const PortSpec& p : ports) {
        const bool up = port_open("127.0.0.1", p.port, 250);
        checks.push_back(Check{"gear one", p.name, up, p.required,
                               std::string("127.0.0.1:") + std::to_string(p.port) +
                                   (up ? " open" : " closed")});
    }

    // ---- organs called at fixed paths, never imported (spec 10.5) --------
    add_path_check(checks, "organs", "chunker",  "C:/chunker/chunker.py",     true);
    add_path_check(checks, "organs", "intercom", "C:/Intercom/intercom.py",   false);
    add_path_check(checks, "organs", "everywhere", "C:/everywhere",           false);
    add_path_check(checks, "organs", "peek",     "C:/peek/peek.py",           false);
    add_path_check(checks, "organs", "fetcher",  "C:/fetcher",                false);
    add_path_check(checks, "organs", "harness",  "C:/sandbox/deepseek-harness", false);

    // ---- the tape and the store -----------------------------------------
    add_path_check(checks, "corpus", "spec",  "docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md", false);
    add_path_check(checks, "corpus", "store", "store",                                        false);

    int failures = 0;
    for (const Check& c : checks) {
        if (c.required && !c.ok) ++failures;
    }

    if (json) {
        std::printf("{\"version\":\"%s\",\"failures\":%d,\"checks\":[", version_string().c_str(),
                    failures);
        for (std::size_t i = 0; i < checks.size(); ++i) {
            const Check& c = checks[i];
            std::printf("%s{\"group\":\"%s\",\"name\":\"%s\",\"ok\":%s,\"required\":%s,\"detail\":\"%s\"}",
                        i ? "," : "", c.group.c_str(), c.name.c_str(), c.ok ? "true" : "false",
                        c.required ? "true" : "false", c.detail.c_str());
        }
        std::printf("]}\n");
    } else {
        std::printf("connectome %s  -  %s\n\n", version_string().c_str(), kSpec);
        std::string group;
        for (const Check& c : checks) {
            if (c.group != group) {
                group = c.group;
                std::printf("[%s]\n", group.c_str());
            }
            std::printf("  %s %-30s %s\n", c.ok ? "ok  " : (c.required ? "FAIL" : "--  "),
                        c.name.c_str(), c.detail.c_str());
        }
        std::printf("\n%d required check%s failing\n", failures, failures == 1 ? "" : "s");
    }
    return failures == 0 ? 0 : 1;
}

} // namespace cx
