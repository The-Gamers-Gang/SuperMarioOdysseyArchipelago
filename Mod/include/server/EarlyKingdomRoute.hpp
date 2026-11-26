#pragma once
#include <array>
#include <cstdint>
#include <cstring>

// World IDs from the moon quota packet. This logic has no Switch dependencies.
namespace EarlyKingdomRoute {
using Order = std::array<std::uint8_t, 3>;
constexpr int Cap = 0, Cascade = 1, Sand = 2, Wooded = 3, Lake = 4;
inline bool valid(const Order& order) {
    unsigned mask = 0;
    for (const auto id : order) {
        if (id != Cascade && id != Sand && id != Lake) return false;
        mask |= 1u << id;
    }
    return mask == ((1u << Cascade) | (1u << Sand) | (1u << Lake));
}
inline const char* home(int id) {
    switch (id) {
        case Cascade: return "WaterfallWorldHomeStage";
        case Sand: return "SandWorldHomeStage";
        case Lake: return "LakeWorldHomeStage";
        case Wooded: return "ForestWorldHomeStage";
        default: return nullptr;
    }
}
inline bool is(const char* actual, const char* expected) {
    return actual && expected && std::strcmp(actual, expected) == 0;
}
inline int next(const Order& order, int from, const char* nativeTarget) {
    if (!valid(order)) return -1;
    if (from == Cap && is(nativeTarget, home(Cascade))) return order[0];
    if (!( (from == Cascade && is(nativeTarget, home(Sand))) ||
           (from == Sand && (is(nativeTarget, home(Lake)) || is(nativeTarget, home(Wooded)))) ||
           (from == Lake && is(nativeTarget, home(Wooded))) ))
        return -1;
    for (std::size_t i = 0; i < order.size(); ++i)
        if (order[i] == from)
            return i + 1 < order.size() ? order[i + 1] : Wooded;
    return -1;
}
} // namespace EarlyKingdomRoute
